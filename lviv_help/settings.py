# import dotenv
import os
import logging  
import logging.config  
import json
# from pythonjsonlogger import jsonlogger

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
	# dotenv.load_dotenv(".env")
	dev_db_settings = {"drivername": 'postgresql+psycopg2',
						"database": os.environ["DBNAME"],
						"username": os.environ["USERNAME"],
						"password": os.environ["PASSWORD"],
						"host": os.environ["HOST"]}

except Exception as e:
	raise Exception("File .env is not found")

# #Logging setings
# logger_settings_filename = "logging_config.json"
# current_dir = os.path.dirname(os.path.abspath(__file__))
# path_to_logfile = f"{current_dir}/{logger_settings_filename}"

# with open(path_to_logfile, 'r') as logger_config:  
#     config_dict = json.load(logger_config)  
  
# logging.config.dictConfig(config_dict)  
# logger = logging.getLogger(__name__)  
# logger.info('Logging started')

