# EXAMPLE
from src.utils.dependencies.user_service import user_service_fabric
import asyncio

response = user_service_fabric()
testing = {"chat_id": 123, "text": "test"}

if __name__ == "__main__":
    asyncio.run(response.create_user(testing))
