from flask import Flask, request, render_template, redirect, session, url_for
from . models import engine, RoomRequest, DeclarativeBase
from sqlalchemy.orm import sessionmaker
# from . settings import logger

DeclarativeBase.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
app = Flask(__name__, template_folder='templates')


@app.route("/",  methods = ["get", "post"])
def need_room():
    if request.method == 'POST':
        content = request.form    
        new_room_request = RoomRequest(**content)
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
def del_request():
    content = request.form
    request_id = content.get("id")
    db_session = Session()
    room_request = db_session.query(RoomRequest).filter(RoomRequest.id == request_id).one()
    room_request.opened = False
    db_session.commit()
    return redirect(url_for("need_room"))
