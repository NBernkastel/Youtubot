from src.repo.repositories import LogRepository
from src.services.log_service import LogService


def log_service_fabric():
    return LogService(LogRepository())
