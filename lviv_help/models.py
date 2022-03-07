from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from . settings import dev_db_settings as db_settings

DeclarativeBase = declarative_base()
engine  = create_engine(URL.create(**db_settings))


class RoomRequest(DeclarativeBase):
    __tablename__ = 'room_requests'

    id = Column(Integer, primary_key=True)
    contacts = Column('contacts', String)
    peoples_count = Column('peoples_count', Integer)
    how_long_in_lviv = Column('how_long_in_lviv', String)
    opened = Column('days_in_room', Boolean, unique=False, default=True)

    def __repr__(self):
        return "".format(self.id)
