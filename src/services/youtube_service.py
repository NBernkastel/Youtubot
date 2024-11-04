import json
import google.auth

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import SCOPES
from src.db.models import Channels
from src.utils.repository import AbstractRepository


class YoutubeService:

    def __init__(self, repo: AbstractRepository):
        self.repo = repo

    async def get_authenticated_service(self, uid, channel_name, youtube_credits=None):
        creds = None
        channel: Channels = await self.repo.get_one([Channels.user_id == uid, Channels.channel_name == channel_name])
        if channel:
            creds = Credentials.from_authorized_user_info(json.loads(channel.youtube_token), SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(google.auth.transport.requests.Request())
            else:
                flow = InstalledAppFlow.from_client_config(json.loads(youtube_credits), SCOPES)
                creds = flow.run_local_server(port=0)
            await self.repo.add_one(
                {'user_id': uid, 'channel_name': channel_name, 'youtube_credits': youtube_credits,
                 'youtube_token': creds.to_json()})

        return build("youtubeAnalytics", "v2", credentials=creds)

    async def get_views_by_date(self, start_date, end_date, uid, channel_name):
        youtube_analytics = await self.get_authenticated_service(uid, channel_name)
        response = youtube_analytics.reports().query(
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            metrics="views",
            dimensions="day"
        ).execute()
        views_summ = 0
        for row in response.get("rows", []):
            date, views = row
            views_summ += views
        return views_summ

    async def get_subscribers_gained_by_date(self, start_date, end_date, uid, channel_name):
        youtube_analytics = await self.get_authenticated_service(uid, channel_name)
        response = youtube_analytics.reports().query(
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            metrics="subscribersGained",
            dimensions="day"
        ).execute()
        subs = 0
        for row in response.get("rows", []):
            date, subscribers_gained = row
            subs += subscribers_gained
        return subs

    async def get_average_view_duration_by_date(self, start_date, end_date, uid, channel_name):
        youtube_analytics = await self.get_authenticated_service(uid, channel_name)
        response = youtube_analytics.reports().query(
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
            durations.append(avg_view_duration_minutes)
        avg = sum(durations) / len(durations)
        return round(avg, 2)

    async def get_average_view_percentage_by_date(self, start_date, end_date, uid, channel_name):
        youtube_analytics = await self.get_authenticated_service(uid, channel_name)
        response = youtube_analytics.reports().query(
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            metrics="averageViewPercentage",
            dimensions="day"
        ).execute()
        percents = []
        for row in response.get("rows", []):
            date, avg_view_percentage = row
            percents.append(avg_view_percentage)
        avg = sum(percents) / len(percents)
        return round(avg, 2)
