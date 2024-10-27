from src.services.test_service import UserService
from src.repo.repositories import UserRepository
"""
В данном файле описываются и инициализируются сервисы для fabric репозитория
"""

def user_service_fabric():
    return UserService(UserRepository())
