from flask import Flask, request, render_template, redirect, session, url_for
from . models import engine, RoomRequest, SupplyRequest, DeclarativeBase
from sqlalchemy.orm import sessionmaker
from datetime import datetime
# from . settings import logger

DeclarativeBase.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
app = Flask(__name__, template_folder='templates')

def get_timestamp():
    now = datetime.now()
    timestamp = now.strftime("%m/%d/%Y, %H:%M")
    return timestamp

@app.route("/",  methods = ["get", "post"])
def need_room():
    if request.method == 'POST':
        content = request.form    
        new_room_request = RoomRequest(**content)
        new_room_request.timestamp = get_timestamp() 
        db_session = Session()
        db_session.add(new_room_request)
        db_session.commit()
        return redirect(url_for("need_room"))
    else:
        try:
            db_session = Session()
            room_requests_query = db_session.query(RoomRequest).all()
            room_requests = [room_request for room_request in room_requests_query]
            return render_template('helps/rooms.html', room_requests=room_requests)
        except Exception as e:
            error_message = "Something went wrong"
            log_message = f"{error_message}: {e}"
            # logger.error(log_message)
            return render_template('error_page.html',error_message=error_message)


@app.route("/del_room_request",  methods = ["post"])
def del_room_request():
    content = request.form
    room_request_id = content.get("id")
    db_session = Session()
    room_request = db_session.query(RoomRequest).filter(RoomRequest.id == room_request_id).one()
    room_request.opened = False
    db_session.commit()
    return redirect(url_for("need_room"))


@app.route("/supply",  methods = ["get", "post"])
def need_supply():
    if request.method == 'POST':
        content = request.form    
        new_supply_request = SupplyRequest(**content)
        new_supply_request.timestamp = get_timestamp() 
        db_session = Session()
        db_session.add(new_supply_request)
        db_session.commit()
        return redirect(url_for("need_supply"))
    else:
        try:
            db_session = Session()
            supply_requests_query = db_session.query(SupplyRequest).all()
            supply_requests = [supply_request for supply_request in supply_requests_query]
            return render_template('helps/supply.html', supply_requests=supply_requests)
        except Exception as e:
            error_message = "Something went wrong"
            log_message = f"{error_message}: {e}"
            print(log_message)
            # logger.error(log_message)
            return render_template('error_page.html',error_message=error_message)


@app.route("/del_supply_request",  methods = ["post"])
def del_supply_request():
    content = request.form
    supply_id = content.get("id")
    db_session = Session()
    supply_request = db_session.query(SupplyRequest).filter(SupplyRequest.id == supply_id).one()
    supply_request.opened = False
    db_session.commit()
    return redirect(url_for("need_supply"))
