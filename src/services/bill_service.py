from src.utils.repository import AbstractRepository


class BillService:

    def __init__(self, repo: AbstractRepository):
        self.repo = repo

    async def add_bill(self, data: dict):
        await self.repo.add_one(data)
