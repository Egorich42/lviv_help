from lviv_help.views import app
from lviv_help.settings import create_logger


log = create_logger(__name__)

if __name__ == "__main__":
	log.info('START APP')
	app.config['SECRET_KEY'] = "Your_secret_string"
	app.run(debug=True, host='127.0.0.1', port=4998)
