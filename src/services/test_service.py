from src.repo.repositories import UserRepository
from src.schemas.test_schema import UserCreate
from src.utils.repository import AbstractRepository

"""
В данном файле описываются и инициализируются сервисы для fabric репозитория
"""


class UserService:

    def __init__(self, repo: AbstractRepository):
        self.repo = repo

    async def create_user(self, data: UserCreate):
        await self.repo.add_one(data)
