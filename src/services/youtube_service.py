import os
import google.auth

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Путь к файлу учетных данных OAuth
CLIENT_SECRETS_FILE = "client_secret_11173779781-iftv5tnihjs1ac61ssovqv4nhl2g9j51.apps.googleusercontent.com.json"

# Области, которые необходимы для доступа к YouTube API
SCOPES = ["https://www.googleapis.com/auth/yt-analytics.readonly"]


class YoutubeService:

    async def get_authenticated_service():
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(google.auth.transport.requests.Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return build("youtubeAnalytics", "v2", credentials=creds)

    async def get_views_by_date(start_date, end_date):
        youtube_analytics = await YoutubeService.get_authenticated_service()

        # Запрашиваем просмотры по датам
        response = youtube_analytics.reports().query(
            ids="channel==MINE",  # Для получения данных вашего канала
            startDate=start_date,
            endDate=end_date,
            metrics="views",
            dimensions="day"
        ).execute()

        # Выводим количество просмотров по каждой дате
        print("Views by Date:")
        for row in response.get("rows", []):
            date, views = row
            print(f"{date}: {views}")
