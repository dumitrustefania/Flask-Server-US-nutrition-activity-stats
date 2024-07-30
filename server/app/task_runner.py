"""
Module that contains the thread pool class
"""

import os
from concurrent.futures import ThreadPoolExecutor
from functools import partial

class ThreadPool:
    """
    Class that incorporates a thread pool executor
    Accepts requests from the web server and submits them to the thread pool
    """
    def __init__(self, webserver):
        self.webserver = webserver

        # Check if environment variable TP_NUM_OF_THREADS is defined
        num_of_threads = os.getenv("TP_NUM_OF_THREADS")
        # If TP_NUM_OF_THREADS is not defined, the number of threads to
        # be used by the thread pool is equal to the number of CPUs of the system
        if num_of_threads is None:
            num_of_threads = os.cpu_count()

        self.thread_pool = ThreadPoolExecutor(max_workers=num_of_threads)

    def shutdown(self):
        """
        Shutdown the thread pool
        """
        self.thread_pool.shutdown()

    def handle_future_result(self, job_id: int, future):
        """
        Method to be called whenever a job is completed by a thread
        Checks whether the future was completed successfully or encountered an exception
        """
        try:
            future.result()
            self.webserver.logger.info(f"Task with job id {job_id} completed successfully")
        except Exception as exception:
            self.webserver.job_status[job_id] = "error"
            self.webserver.requests_solver.write_result({"error_message": str(exception)}, job_id)
            self.webserver.logger.info(
                "Task with job id %s failed with exception: %s", job_id, exception
            )

    def submit(self, endpoint, job_id, request_args, has_state):
        """
        Submit a job to the thread pool executor
        """
        future = self.thread_pool.submit(self.webserver.requests_solver.solver, endpoint, job_id, request_args, has_state)
        self.webserver.logger.info(f"Task with job id {job_id} submitted")

        future.add_done_callback(partial(self.handle_future_result, job_id))
