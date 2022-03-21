from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from . settings import dev_db_settings as db_settings

DeclarativeBase = declarative_base()
# engine  = create_engine(URL.create(**db_settings))
engine = create_engine(f'postgresql://{db_settings.get("username")}:{db_settings.get("password")}@{db_settings.get("host")}:{db_settings.get("port")}/{db_settings.get("database")}') 


class RoomRequest(DeclarativeBase):
    __tablename__ = 'room_requests'

    id = Column(Integer, primary_key=True)
    contacts = Column('contacts', String)
    timestamp = Column('timestamp', String)
    peoples_count = Column('peoples_count', Integer)
    how_long_in_lviv = Column('how_long_in_lviv', String)
    opened = Column('days_in_room', Boolean, unique=False, default=True)

    def __repr__(self):
        return "".format(self.id)


class SupplyRequest(DeclarativeBase):
    __tablename__ = 'supply_requests'

    id = Column(Integer, primary_key=True)
    timestamp = Column('timestamp', String)
    contacts = Column('contacts', String)
    subject = Column('peoples_count', String)
    opened = Column('days_in_room', Boolean, unique=False, default=True)

    def __repr__(self):
        return "".format(self.id)
