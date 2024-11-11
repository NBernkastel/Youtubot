from src.db.models import Users
from src.utils.repository import AbstractRepository


class UserService:

    def __init__(self, repo: AbstractRepository):
        self.repo = repo

    async def create_user(self, data: dict):
        await self.repo.add_one(data)

    async def get_user_by_id(self, uid: int):
        return await self.repo.get_one([Users.chat_id == uid])

    async def update_user(self, uid: int, data: dict):
        await self.repo.update_one([Users.chat_id == uid], data)

    async def get_all_users(self):
        return await self.repo.get_all_by_filter()
