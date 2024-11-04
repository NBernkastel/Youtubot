from src.repo.repositories import ChannelRepository
from src.services.youtube_service import YoutubeService


def youtube_service_fabric():
    return YoutubeService(ChannelRepository())
