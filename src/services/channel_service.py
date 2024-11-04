from src.db.models import Channels
from src.utils.repository import AbstractRepository


class ChannelService:

    def __init__(self, repo: AbstractRepository):
        self.repo = repo

    async def add_channel(self, data: dict):
        await self.repo.add_one(data)

    async def get_all_user_channels(self, uid: int):
        return await self.repo.get_all_by_filter([Channels.user_id == uid])
