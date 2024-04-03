Name: Dumitru Bianca Stefania

Group: 332CA

# Homework #1 ASC - Le Stats Sportif

## Solution explanation

The Flask webserver uses a ThreadPoolExecutor object to help execute requests asynchronously. Each request that requires parsing the CSV file receives a job ID and the thread pool handles the execution in the background, by submitting the computing task to one of the worker threads. I also used a callback function (that gets called whenever a thread finishes a task) to verify whether any exception was raised during the execution. To do so, I used the preexisting ```add_done_callback``` method on the previously submitted future. The functionality that handles the thread pool is located in *app/task_runner.py*.

The status of all jobs is kept in a dictionary datastructure in the webserver and is used whenever a user requests information about a specific job or about all jobs. Initially, when a job is created, it receives the *running* status, which can then change to *done* or *error*, when the worker thread finishes executing the corresponding task.

In order to compute the answers for the requests, I used the **pandas** library, which I found very easy to understand and work with. All the helpers for computing the requests based on the CSV are placed in *requests_solver.py*. In order to separate concerns, avoid duplicate code and make the helper functions as easy as possible to test, I used a method called *solver* that is used to check the input, call the helpers and write the result to the file corresponding to the job ID.

In the *routes.py* file, I added the routes for *graceful_shutdown*, *num_jobs* and *get_jobs*, which were straightforward to implement.

I think the homework was very useful, as it was my first attempt at working with a Flask server. I also created my first python unit tests, which are quite different to some other unit tests I used to write in Go. I feel like I didn't learn much about parallel programming, as the ThreadPoolExecutor did everything for me :).

I think my implementation is a good one, although I think that some sort of caching for the requests would make sense in a real-life application. Also, I believe that more tests could be added in the unit testing module, such as making requests with the bad method, etc.

### Logging

For logging, I used the recommended configuration and I logged every request received and the payload, error encoundered by the application or responses I sent back.

### Unit tests

In the unit tests, I tested the functionality of the helper functions that compute answers based on mocked data. Additionally, I tested the functionality of the webserver when:
* a POST request with bad input is received
* a call to /api/get_results is made with an invalid job ID
* a call to /api/jobs is made after previously creating 2 other job-generating requests
* a call to /api/graceful_shutdown is made, followed by an /api/num_jobs call

# Implementation

I implemented all aspects specified in the assignment. There are no extra functionalities.

The most difficult thing for me was understanding how to work with the server, by making sure to provide it with proper JSON responses and status codes. I also remembered how to use Postman.

## Resources
* ThreadPoolExecutor [lab](https://ocw.cs.pub.ro/courses/asc/laboratoare/03), [online guide](https://superfastpython.com/threadpoolexecutor-in-python/), [add_done_callback documentation](https://docs.python.org/3/library/asyncio-future.html#asyncio.Future.add_done_callback)
* Pandas - [read CSV](https://www.w3schools.com/python/pandas/pandas_csv.asp), [filter values in a dataframe](https://www.educative.io/answers/how-to-filter-pandas-dataframe-by-column-value)
* Homework forum

## How to run
* To start the webserver, run ```make run_server```
* To start the checker, run ```make run_tests```
* To start the unit tests, run ```make run_unit_tests``` or ```python3 -m unittest -v ./unittests/test_webserver.py```
  
Tests must be run after the server is running.