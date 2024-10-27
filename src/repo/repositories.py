from src.db.models import User
from src.utils.repository import SQLAlchemyRepository

"""
В данном файле описываются модели поведения для fabric репозитория
"""


class UserRepository(SQLAlchemyRepository):
    model = User
