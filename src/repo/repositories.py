from src.db.models import Users, Channels, Logs, Bills
from src.utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = Users


class ChannelRepository(SQLAlchemyRepository):
    model = Channels


class LogRepository(SQLAlchemyRepository):
    model = Logs


class BillRepository(SQLAlchemyRepository):
    model = Bills