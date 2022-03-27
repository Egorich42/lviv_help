import psycopg2
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class DatabaseError(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(msg)

    def __repr__(self):
        return f'Database Error: {self.msg}'


class Database:
    def __init__(self, connection_string):
        self.engine = self.init_engine(connection_string)
        self.engine.pool_timeout = 60
        self.Session = sessionmaker(bind=self.engine)

    def __del__(self):
        self.engine.dispose()

    @staticmethod
    def init_engine(connection_string):
        try:
            engine = create_engine(connection_string, connect_args={"sslmode": "disable"})
            engine.connect()
            return engine
        except psycopg2.OperationalError as e:
            raise DatabaseError(f'Error with the connection to the database: {str(e)}')


DeclarativeBase = declarative_base()


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
