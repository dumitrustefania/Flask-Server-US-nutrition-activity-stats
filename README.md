
# Flask Server - US sport stats
 March 2024

## Overview

Implement a multi-threaded Python Flask server to handle CSV-based requests and provide nutritional and physical activity statistics for US states (2011-2022). Key endpoints include:

* /api/states_mean: Average values per state, sorted.
* /api/state_mean: Average values for a specific state.
* /api/best5 and /api/worst5: Top/bottom 5 states based on average values.
* /api/global_mean: Overall average values.
* /api/diff_from_mean and /api/state_diff_from_mean: Differences from global average.
* /api/mean_by_category and /api/state_mean_by_category: Averages by category.
* /api/graceful_shutdown: Gracefully stop the server.
* /api/jobs and /api/num_jobs: Job status and count.
* /api/get_results/<job_id>: Retrieve results by job ID.

Server should manage job queues and return results asynchronously.

## Implementation

The Flask webserver uses a ThreadPoolExecutor object to help execute requests asynchronously. Each request that requires parsing the CSV file receives a job ID and the thread pool handles the execution in the background, by submitting the computing task to one of the worker threads. I also used a callback function (that gets called whenever a thread finishes a task) to verify whether any exception was raised during the execution. To do so, I used the preexisting ```add_done_callback``` method on the previously submitted future. The functionality that handles the thread pool is located in *app/task_runner.py*.

The status of all jobs is kept in a dictionary datastructure in the webserver and is used whenever a user requests information about a specific job or about all jobs. Initially, when a job is created, it receives the *running* status, which can then change to *done* or *error*, when the worker thread finishes executing the corresponding task.

In order to compute the answers for the requests, I used the **pandas** library. All the helpers for computing the requests based on the CSV are placed in *requests_solver.py*. In order to separate concerns, avoid duplicate code and make the helper functions as easy as possible to test, I used a method called *solver* that is used to check the input, call the helpers and write the result to the file corresponding to the job ID.

In the *routes.py* file, I added the routes for *graceful_shutdown*, *num_jobs* and *get_jobs*, which were straightforward to implement.

### Logging

For logging, I used the recommended configuration and I logged every request received and the payload, error encoundered by the application or responses I sent back.

### Unit tests

In the unit tests, I tested the functionality of the helper functions that compute answers based on mocked data. Additionally, I tested the functionality of the webserver when:
* a POST request with bad input is received
* a call to /api/get_results is made with an invalid job ID
* a call to /api/jobs is made after previously creating 2 other job-generating requests
* a call to /api/graceful_shutdown is made, followed by an /api/num_jobs call

## Resources
* ThreadPoolExecutor [lab](https://ocw.cs.pub.ro/courses/asc/laboratoare/03), [online guide](https://superfastpython.com/threadpoolexecutor-in-python/), [add_done_callback documentation](https://docs.python.org/3/library/asyncio-future.html#asyncio.Future.add_done_callback)
* Pandas - [read CSV](https://www.w3schools.com/python/pandas/pandas_csv.asp), [filter values in a dataframe](https://www.educative.io/answers/how-to-filter-pandas-dataframe-by-column-value)

## How to run
* To start the webserver, run ```make run_server```
* To start the checker, run ```make run_tests```
* To start the unit tests, run ```make run_unit_tests``` or ```python3 -m unittest -v ./unittests/test_webserver.py```
  
Tests must be run after the server is running.
