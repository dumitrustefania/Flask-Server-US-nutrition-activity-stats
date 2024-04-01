import logging
import os
import time
from logging.handlers import RotatingFileHandler

from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from app.requests_solver import RequestsSolver

webserver = Flask(__name__)

webserver.logger = logging.getLogger(__name__)
logging.getLogger('werkzeug').disabled = True

logging.Formatter.converter = time.gmtime

os.makedirs("logging", exist_ok=True)
logging.basicConfig(handlers=[RotatingFileHandler('logging/webserver.log',
                                                  maxBytes=100000000, 
                                                  backupCount=10)],
                    level=logging.INFO,
                    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
                    datefmt='%d-%b-%y %H:%M:%S')

webserver.logger.info("Webserver initialized")

webserver.tasks_runner = ThreadPool(webserver)
webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")
webserver.requests_solver = RequestsSolver(webserver)

webserver.tasks_runner.start()

webserver.job_counter = 1
webserver.job_status = {}

from app import routes
