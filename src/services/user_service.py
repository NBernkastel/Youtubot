from src.repo.repositories import UserRepository
from src.schemas.test_schema import UserCreate
from src.utils.repository import AbstractRepository

class UserService:

    def __init__(self, repo: AbstractRepository):
        self.repo = repo

    async def create_user(self, data: dict):
        await self.repo.add_one(data)
