import psycopg2
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.exc import SQLAlchemyError
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

    def get_number_of_requests(self, table_class):
        if not DeclarativeBase.__subclasscheck__(table_class):
            raise DatabaseError(f'Table {table_class.__name__} does not exists')
        session = self.Session()
        try:
            return session.query(table_class).filter(table_class.opened).count()
        except SQLAlchemyError as e:
            raise DatabaseError(f'Error while counting requests: {str(e)}')
        finally:
            session.close()

    def get_room_requests(self):
        session = self.Session()
        try:
            return session.query(RoomRequest).filter(RoomRequest.opened).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f'Error while getting room requests: {str(e)}')
        finally:
            session.close()

    def set_room_request(self, room_request):
        session = self.Session()
        try:
            session.add(room_request)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError(f'Error while adding new room request: {str(e)}')
        finally:
            session.close()

    def get_supply_requests(self):
        session = self.Session()
        try:
            return session.query(SupplyRequest).filter(SupplyRequest.opened).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f'Error while getting supply requests: {str(e)}')
        finally:
            session.close()

    def set_supply_request(self, supply_request):
        session = self.Session()
        try:
            session.add(supply_request)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError(f'Error while adding new supply request: {str(e)}')
        finally:
            session.close()

    def remove_room_request(self, request_id):
        session = self.Session()
        try:
            room_request = session.query(RoomRequest).filter(RoomRequest.id == request_id).one()
            room_request.opened = False
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError(f'Error while removing room request with id {request_id}: {str(e)}')
        finally:
            session.close()

    def remove_supply_request(self, request_id):
        session = self.Session()
        try:
            room_request = session.query(SupplyRequest).filter(SupplyRequest.id == request_id).one()
            room_request.opened = False
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError(f'Error while removing supply request with id {request_id}: {str(e)}')
        finally:
            session.close()


DeclarativeBase = declarative_base()


class RoomRequest(DeclarativeBase):
    __tablename__ = 'room_requests'

    id = Column(Integer, primary_key=True)
    contacts = Column('contacts', String)                                   # application's contact (Elena, +7XXX...)
    timestamp = Column('timestamp', String)
    peoples_count = Column('peoples_count', Integer)                        # how many people?
    how_long_in_lviv = Column('how_long_in_lviv', String)                   # how long in lviv?
    opened = Column('days_in_room', Boolean, unique=False, default=True)    # is the application opened?

    def __repr__(self):
        return ''.format(self.id)


class SupplyRequest(DeclarativeBase):
    __tablename__ = 'supply_requests'

    id = Column(Integer, primary_key=True)
    timestamp = Column('timestamp', String)
    contacts = Column('contacts', String)           # application's contact (Elena, +7XXX...)
    subject = Column('peoples_count', String)       # application's comment
    opened = Column('days_in_room', Boolean, unique=False, default=True)    # is the application opened?

    def __repr__(self):
        return ''.format(self.id)
