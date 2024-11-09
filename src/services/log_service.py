from src.db.models import Logs
from src.utils.repository import AbstractRepository


class LogService:

    def __init__(self, repo: AbstractRepository):
        self.repo = repo

    async def create_log(self, data: dict):
        await self.repo.add_one(data)

    async def get_logs(self, uid):
        return await self.repo.get_all_by_filter([Logs.user_id == uid])
