"""
Initialize the webserver.
"""

import logging
import os
import time
from logging.handlers import RotatingFileHandler

import pandas as pd
from flask import Flask
from app.task_runner import ThreadPool
from app.requests_solver import RequestsSolver

webserver = Flask(__name__)

# Create the logger for the webserver
webserver.logger = logging.getLogger(__name__)
# Disable werkzeug (flask) logs
logging.getLogger("werkzeug").disabled = True

# Format log messages to include the time in GMT
logging.Formatter.converter = time.gmtime

# Configure the logger to use a RotatingFileHandler and a specific format
os.makedirs("logging", exist_ok=True)
logging.basicConfig(
    handlers=[RotatingFileHandler("logging/webserver.log", maxBytes=1000000, backupCount=10)],
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)

webserver.logger.info("Webserver initialized")

webserver.tasks_runner = ThreadPool(webserver)
webserver.data = pd.read_csv("./nutrition_activity_obesity_usa_subset.csv")
webserver.requests_solver = RequestsSolver(webserver)

webserver.job_counter = 1
webserver.job_status = {}

from app import routes
