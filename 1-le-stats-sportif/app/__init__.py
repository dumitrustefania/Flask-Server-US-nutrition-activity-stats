from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from app.requests_solver import RequestsSolver

webserver = Flask(__name__)

webserver.tasks_runner = ThreadPool(webserver)
webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")
webserver.requests_solver = RequestsSolver(webserver)

webserver.tasks_runner.start()

webserver.job_counter = 1
webserver.job_status = {}

from app import routes
