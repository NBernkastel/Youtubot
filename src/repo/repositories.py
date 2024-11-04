from src.db.models import Users, Channels
from src.utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = Users


class ChannelRepository(SQLAlchemyRepository):
    model = Channels