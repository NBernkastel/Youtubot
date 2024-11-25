import json
from datetime import datetime, timedelta

import google.auth

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from oauthlib.oauth2 import OAuth2Token

from config import SCOPES, REDIRECT_URL
from src.db.models import Channels
from src.utils.repository import AbstractRepository


class YoutubeService:

    def __init__(self, repo: AbstractRepository):
        self.repo = repo

    async def get_authenticated_service(self, uid=None, channel_name=None, youtube_credits=None, creds_analytic=None,
                                        creds_data=None, auth=False):
        channel = None
        if channel_name and uid:
            channel: Channels = await self.repo.get_one(
                [Channels.user_id == uid, Channels.channel_name == channel_name])
        if channel:
            creds_analytic = Credentials.from_authorized_user_info(json.loads(channel.youtube_analytic_token),
                                                                   [SCOPES[0]])
            creds_data = Credentials.from_authorized_user_info(json.loads(channel.youtube_data_token), [SCOPES[1]])
        if auth or not creds_analytic or not creds_analytic.valid:
            if not auth:
                if (creds_analytic and creds_analytic.expired and creds_analytic.refresh_token) or (
                        creds_data and creds_data.expired and creds_data.refresh_token):
                    creds_analytic.refresh(google.auth.transport.requests.Request())
                    creds_data.refresh(google.auth.transport.requests.Request())
                    await self.repo.update_one([Channels.user_id == uid, Channels.channel_name == channel_name],
                                               {'youtube_analytic_token': creds_analytic.to_json(),
                                                'youtube_data_token': creds_data.to_json()})
            else:
                youtube = build("youtube", "v3", credentials=creds_data)
                response = youtube.channels().list(
                    part="snippet",
                    mine=True
                ).execute()
                channel_url = None
                for item in response.get("items", []):
                    channel_name = item["snippet"]["title"]
                    channel_id = item["id"]
                    channel_url = f"https://www.youtube.com/channel/{channel_id}"
                await self.repo.add_one(
                    {'user_id': uid, 'channel_name': channel_name, 'channel_url': channel_url,
                     'youtube_credits': youtube_credits,
                     'youtube_analytic_token': creds_analytic.to_json(),
                     'youtube_data_token': creds_data.to_json()})

        return (build("youtubeAnalytics", "v2", credentials=creds_analytic),
                build("youtube", "v3", credentials=creds_data))

    async def get_views_by_date(self, start_date, end_date, uid, channel_name):
        youtube_analytics = await self.get_authenticated_service(uid, channel_name)
        response = youtube_analytics[0].reports().query(
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            metrics="views",
            dimensions="day"
        ).execute()
        views_summ = []
        for row in response.get("rows", []):
            date, views = row
            views_summ.append([date, views])
        return views_summ

    async def get_analytic_login_url(self, youtube_credits):
        flow_analytic = InstalledAppFlow.from_client_config(json.loads(youtube_credits), [SCOPES[0]])
        flow_analytic.redirect_uri = REDIRECT_URL
        analytic_auth_url, _ = flow_analytic.authorization_url(prompt='consent')
        return analytic_auth_url, flow_analytic

    async def get_data_login_url(self, youtube_credits):
        flow_data = InstalledAppFlow.from_client_config(json.loads(youtube_credits), [SCOPES[1]])
        flow_data.redirect_uri = REDIRECT_URL
        data_auth_url, _ = flow_data.authorization_url(prompt='consent')
        return data_auth_url, flow_data

    async def res_analytic_token(self, code, flow_analytic):
        flow_analytic.fetch_token(code=code)
        creds_analytic = flow_analytic.credentials
        return creds_analytic

    async def res_data_token(self, code, flow_data):
        flow_data.fetch_token(code=code)
        creds_data = flow_data.credentials
        return creds_data

    async def get_subscribers_gained_by_date(self, start_date, end_date, uid, channel_name):
        youtube_analytics = await self.get_authenticated_service(uid, channel_name)
        response = youtube_analytics[0].reports().query(
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            metrics="subscribersGained",
            dimensions="day"
        ).execute()
        subs = []
        subs_sum = 0
        for row in response.get("rows", []):
            date, subscribers_gained = row
            subs.append([str(date), subscribers_gained])
            subs_sum += subscribers_gained
        return subs, subs_sum

    async def get_average_view_duration_by_date(self, start_date, end_date, uid, channel_name):
        youtube_analytics = await self.get_authenticated_service(uid, channel_name)
        response = youtube_analytics[0].reports().query(
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            metrics="averageViewDuration",
            dimensions="day"
        ).execute()
        durations = []
        for row in response.get("rows", []):
            date, avg_view_duration = row
            avg_view_duration_minutes = round(avg_view_duration / 60, 2)
            durations.append([date, avg_view_duration_minutes])
        return durations

    async def get_average_view_percentage_by_date(self, start_date, end_date, uid, channel_name):
        youtube_analytics = await self.get_authenticated_service(uid, channel_name)
        response = youtube_analytics[0].reports().query(
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            metrics="averageViewPercentage",
            dimensions="day"
        ).execute()
        percents = []
        for row in response.get("rows", []):
            date, avg_view_percentage = row
            percents.append([date, round(avg_view_percentage, 2)])
        return percents

    async def get_channel_id(self, youtube):
        response = youtube.channels().list(
            part="id",
            mine=True
        ).execute()
        return response["items"][0]["id"]

    async def get_video_count_by_date(self, start_date, end_date, uid, channel_name):
        youtube = await self.get_authenticated_service(uid, channel_name)
        channel_id = await self.get_channel_id(youtube[1])
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        videos_published = []
        request = youtube[1].search().list(
            part="snippet",
            channelId=channel_id,
            publishedAfter=start_date_dt.isoformat() + "Z",
            publishedBefore=end_date_dt.isoformat() + "Z",
            type="video",
            maxResults=50
        )
        while request:
            response = request.execute()
            for item in response.get("items", []):
                video_id = 'https://www.youtube.com/watch?v='+item["id"]["videoId"]
                published_at = item["snippet"]["publishedAt"]
                videos_published.append([
                    video_id,
                    datetime.fromisoformat(published_at)
                ])
            request = youtube[1].search().list_next(request, response)

        return videos_published

    async def get_video_views_by_date(self, start_date, end_date, uid, channel_name):
        youtube = await self.get_authenticated_service(uid, channel_name)
        channel_id = await self.get_channel_id(youtube[1])
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        videos_info = []
        request = youtube[1].search().list(
            part="snippet",
            channelId=channel_id,
            publishedAfter=start_date_dt.isoformat() + "Z",
            publishedBefore=end_date_dt.isoformat() + "Z",
            type="video",
            maxResults=50
        )
        video_ids = []
        while request:
            response = request.execute()
            for item in response.get("items", []):
                video_id = item["id"]["videoId"]
                video_ids.append(video_id)
            request = youtube[1].search().list_next(request, response)
        for i in range(0, len(video_ids), 50):
            batch_ids = video_ids[i:i + 50]
            stats_request = youtube[1].videos().list(
                part="statistics,snippet",
                id=",".join(batch_ids)
            )
            stats_response = stats_request.execute()
            for video in stats_response.get("items", []):
                video_id = f"https://www.youtube.com/watch?v={video['id']}"
                views = int(video["statistics"].get("viewCount", 0))
                published_at = video["snippet"]["publishedAt"]
                videos_info.append([
                    video_id,
                    views,
                    datetime.fromisoformat(published_at.replace("Z", "+00:00"))
                ])

        return videos_info