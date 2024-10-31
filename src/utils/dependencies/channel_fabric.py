from src.services.channel_service import ChannelService
from src.repo.repositories import ChannelRepository


def channel_service_fabric():
    return ChannelService(ChannelRepository())
