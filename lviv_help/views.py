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

        try:
            sql_db.set_room_request(new_room_request)
        except DatabaseError as e:
            log.warning(str(e))
        return redirect(url_for("need_room"))

    if request.method == 'GET':
        try:
            number_of_requests = sql_db.get_number_of_requests(RoomRequest)
            room_requests = sql_db.get_room_requests()
            return render_template('helps/rooms.html', room_requests=room_requests, number_of_requests=number_of_requests)
        except DatabaseError as e:
            log.warning(str(e))
            return render_template('error_page.html', error_message='Something went wrong')


@app.route('/del_room_request', methods=['POST'])
def del_room_request():
    if room_request_id := request.form.get('id', None):
        try:
            sql_db.remove_room_request(room_request_id)
            log.info(f'Room request {room_request_id} closed')
        except DatabaseError as e:
            log.warning(str(e))
    return redirect(url_for("need_room"))


@app.route('/supply', methods=['GET', 'POST'])
def need_supply():
    if request.method == 'POST':
        new_supply_request = SupplyRequest(**{
            'contacts': sanitize(request.form.get('contacts', '')),  # application's contact (Elena, +7XXX...)
            'subject': sanitize(request.form.get('subject', '')),    # application's comment
            'timestamp': get_timestamp()
        })

        try:
            sql_db.set_supply_request(new_supply_request)
        except DatabaseError as e:
            log.warning(str(e))
        return redirect(url_for("need_supply"))

    if request.method == 'GET':
        try:
            number_of_requests = sql_db.get_number_of_requests(SupplyRequest)
            supply_requests = sql_db.get_supply_requests()
            return render_template('helps/supply.html',
                                   supply_requests=supply_requests,
                                   number_of_requests=number_of_requests)
        except DatabaseError as e:
            log.warning(str(e))


@app.route('/del_supply_request', methods=["POST"])
def del_supply_request():
    if supply_request_id := request.form.get('id', None):
        try:
            sql_db.remove_supply_request(supply_request_id)
            log.info(f'Supply request {supply_request_id} closed')
        except DatabaseError as e:
            log.warning(str(e))
    return redirect(url_for("need_supply"))
