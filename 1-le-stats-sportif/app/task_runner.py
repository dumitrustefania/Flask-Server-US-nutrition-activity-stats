from queue import Queue
from threading import Thread, Event
import time
import os
from concurrent.futures import ThreadPoolExecutor 

class ThreadPool:
    def __init__(self):
        # Check if environment variable TP_NUM_OF_THREADS is defined
        self.num_of_threads = os.getenv("TP_NUM_OF_THREADS")
        # If TP_NUM_OF_THREADS is not defined, the number of threads to
        # be used by the thread pool is equal to the number of CPUs of the system
        if self.num_of_threads is None:
            self.num_of_threads = os.cpu_count()
        
        self.thread_pool = None
   
    def start(self):
        self.thread_pool = ThreadPoolExecutor(max_workers=self.num_of_threads)
    
    def shutdown(self):
        self.thread_pool.shutdown()

    def submit(self, callable, job_id, request_args):
        # print(job_id, request_args)
        # print(f"Submitting task to thread pool")
        return self.thread_pool.submit(callable, job_id, request_args)
    
    