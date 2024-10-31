from src.utils.repository import AbstractRepository


class ChannelService:

    def __init__(self, repo: AbstractRepository):
        self.repo = repo

    async def add_channel(self, data: dict):
        await self.repo.add_one(data)
