from src.db.models import Users
from src.utils.repository import AbstractRepository


class UserService:

    def __init__(self, repo: AbstractRepository):
        self.repo = repo

    async def create_user(self, data: dict):
        await self.repo.add_one(data)

    async def get_user_by_id(self, uid: int):
        return await self.repo.get_one([Users.chat_id == uid])
