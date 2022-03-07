from lviv_help import views
from lviv_help.views import app

if __name__ == "__main__":
	app.config['SECRET_KEY'] = "Your_secret_string"
	app.run(debug=True, host='0.0.0.0', port=4998)



# gunicorn --bind 127.0.0.1:4998 run:gunicorn_app

# gunicorn --bind 0.0.0.0:4998 app:app
