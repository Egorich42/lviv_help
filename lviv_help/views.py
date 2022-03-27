import os
import html
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError
from .db import RoomRequest, SupplyRequest, DeclarativeBase, DatabaseError, Database
from .settings import create_logger

log = create_logger(__name__)

conn_str = os.environ.get('POSTGRES_URL', '')

try:
    sql_db = Database(conn_str)
    DeclarativeBase.metadata.create_all(sql_db.engine)
    log.info('Connection to the database have done successfully')
except KeyError:
    log.error('No database env variables')
    exit(1)
except DatabaseError as e:
    log.error(str(e))
    exit(1)

app = Flask(__name__, template_folder='templates')


def get_timestamp():
    return datetime.now().strftime("%m/%d/%Y, %H:%M")


def sanitize(s):
    if not isinstance(s, str):
        s = str(s)
    return html.escape(s)


@app.route('/', methods=['GET', 'POST'])
def need_room():
    if request.method == 'POST':
        new_room_request = RoomRequest(**{
            'contacts': sanitize(request.form.get('contacts', '')),
            'how_long_in_lviv': sanitize(request.form.get('how_long_in_lviv', '')),
            'peoples_count': sanitize(request.form.get('peoples_count', '0')),
            'timestamp': get_timestamp(),
            'opened': True
        })

        session = sql_db.Session()
        try:
            session.add(new_room_request)
            session.commit()
        except SQLAlchemyError as e:
            log.warning(f'Database error setting package: {e}')
            session.rollback()
        finally:
            session.close()

        return redirect(url_for("need_room"))

    session = sql_db.Session()
    try:
        room_requests = session.query(RoomRequest).all()
        return render_template('helps/rooms.html', room_requests=room_requests)
    except SQLAlchemyError as e:
        log.warning(f'Database error setting package: {e}')
        return render_template('error_page.html', error_message='Something went wrong')
    finally:
        session.close()


@app.route('/del_room_request', methods=['POST'])
def del_room_request():
    content = request.form
    room_request_id = content.get('id', None)

    if room_request_id:
        session = sql_db.Session()
        try:
            room_request = session.query(RoomRequest).filter(RoomRequest.id == room_request_id).one()
            room_request.opened = False
            session.commit()
        except SQLAlchemyError as e:
            log.warning(f'Database error setting package: {e}')
            session.rollback()
        finally:
            session.close()
        log.info(f'Room request {room_request_id} closed')
    return redirect(url_for("need_room"))


@app.route('/supply', methods=['GET', 'POST'])
def need_supply():
    if request.method == 'POST':
        new_supply_request = SupplyRequest(**{
            'contacts': sanitize(request.form.get('contacts', '')),
            'peoples_count': sanitize(request.form.get('peoples_count', '0')),
            'timestamp': get_timestamp()
        })

        session = sql_db.Session()
        try:
            session.add(new_supply_request)
            session.commit()
        except SQLAlchemyError as e:
            log.warning(f'Database error setting package: {e}')
            session.rollback()
        finally:
            session.close()
        return redirect(url_for("need_supply"))

    session = sql_db.Session()
    try:
        supply_requests = session.query(SupplyRequest).all()
        return render_template('helps/supply.html', supply_requests=supply_requests)
    except SQLAlchemyError as e:
        log.warning("Database error setting package: %s", e)
    finally:
        session.close()


@app.route('/del_supply_request', methods=["POST"])
def del_supply_request():
    supply_request_id = request.form.get('id', None)
    if supply_request_id:
        session = sql_db.Session()
        try:
            supply_request = session.query(SupplyRequest).filter(SupplyRequest.id == supply_request_id).one()
            supply_request.opened = False
            session.commit()
        except SQLAlchemyError as e:
            log.warning(f'Database error setting package: {e}')
        finally:
            session.close()
        log.info(f'Supply request {supply_request_id} closed')
    return redirect(url_for("need_supply"))
