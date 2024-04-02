"""
Module that contains routes for the webserver
"""
import json

from flask import request, jsonify
from app import webserver, requests_solver

def submit_request(solver, endpoint, req):
    """
    Submit a post request to the thread pool
    """
    if request.method == 'POST':
        # Get request data
        data = req.json
        webserver.logger.info("Request data: %s", data)

        # Assign a job id
        job_id = webserver.job_counter
        webserver.logger.info("Job id assigned: %s", job_id)

        # Register the job to the thread pool. Don't wait for task to finish
        webserver.job_status[job_id] = "running"
        webserver.tasks_runner.submit(solver, endpoint, job_id, data)

        # Increment job_id counter
        webserver.job_counter += 1

        # Return associated job_id
        return jsonify({"job_id": job_id}), 200

    # Method other than POST not allowed
    webserver.logger.error("Method not allowed - POST request expected. Got  %s", request.method)
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """
    Route to get the response for a job
    """
    webserver.logger.info("Route /api/get_results/%s called", job_id)
    job_id = int(job_id)

    # Check if job_id is valid
    if 1 <= job_id < webserver.job_counter:
        # Check the status for the job_id
        status = webserver.job_status.get(job_id)
        webserver.logger.info("Status for job_id_%s is %s", job_id, status)

        if status in ("done", "error"):
            # Read the result from the output file
            with open(f"results/job_id_{job_id}.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                webserver.logger.info("Data for job_id_%s: %s", job_id, data)

                # Return a relevant status code
                if status == "error":
                    code = 400
                else:
                    code = 200

                return jsonify({"status": status, "data": data}), code
        elif status == "running":
            return jsonify({"status": status}), 200

    webserver.logger.error("Invalid job_id: %s", job_id)
    return jsonify({"status": "error", "reason": "Invalid job_id"}), 500

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """
    Route to get the average value for a question for each state
    """
    webserver.logger.info("Route /api/states_mean called")
    return submit_request(
        webserver.requests_solver.question_solver,
        requests_solver.states_mean,
        request)

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """
    Route to get the average value for a question for a specific state
    """
    webserver.logger.info("Route /api/state_mean called")
    return submit_request(
        webserver.requests_solver.question_and_state_solver,
        requests_solver.state_mean,
        request,)

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """
    Route to get the 5 states with the best average value for a question
    """
    webserver.logger.info("Route /api/best5 called")
    return submit_request(
        webserver.requests_solver.question_solver,
        requests_solver.best5,
        request)

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """
    Route to get the 5 states with the worst average value for a question
    """
    webserver.logger.info("Route /api/worst5 called")
    return submit_request(
        webserver.requests_solver.question_solver,
        requests_solver.worst5,
        request)

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """
    Route to get the global average value for a question
    """
    webserver.logger.info("Route /api/global_mean called")
    return submit_request(
        webserver.requests_solver.question_solver,
        requests_solver.global_mean,
        request)

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """
    Route to get the difference between the global average value and
    the average value for each state
    """
    webserver.logger.info("Route /api/diff_from_mean called")
    return submit_request(
        webserver.requests_solver.question_solver,
        requests_solver.diff_from_mean,
        request)

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """
    Route to get the difference between the global average value and
    the average value for a specific state
    """
    webserver.logger.info("Route /api/state_diff_from_mean called")
    return submit_request(
        webserver.requests_solver.question_and_state_solver,
        requests_solver.state_diff_from_mean,
        request)

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """
    Route to get the average value for a question for each state and each subcategory in a category
    """
    webserver.logger.info("Route /api/mean_by_category called")
    return submit_request(
        webserver.requests_solver.question_solver,
        requests_solver.mean_by_category,
        request)

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """
    Route to get the average value for a question for a specific state
    and each subcategory in a category
    """
    webserver.logger.info("Route /api/state_mean_by_category called")
    return submit_request(
        webserver.requests_solver.question_and_state_solver,
        requests_solver.state_mean_by_category,
        request)

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def shutdown():
    """
    Route to shutdown the thread pool, which should not accept any more tasks
    """
    webserver.logger.info("Graceful shutdown initiated")
    webserver.tasks_runner.shutdown()
    return jsonify({"status": "done"}), 200

@webserver.route('/api/jobs', methods=['GET'])
def get_jobs():
    """
    Route to get the status for all submitted jobs
    """
    webserver.logger.info("Route /api/jobs called")
    statuses = [
        {"job_id_" + str(job_id): status}
        for job_id, status in webserver.job_status.items()
    ]
    webserver.logger.info("Jobs' statuses: %s", statuses)
    return jsonify({"status": "done", "data": statuses}), 200

@webserver.route('/api/num_jobs', methods=['GET'])
def get_num_jobs():
    """
    Route to get the number of running jobs
    """
    webserver.logger.info("Route /api/num_jobs called")
    count = 0
    for val in webserver.job_status.values():
        if val == "running":
            count += 1

    webserver.logger.info("Number of running jobs: %s", count)
    return jsonify({"status": "done", "data": count}), 200

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    """
    Route to display a welcome message and the defined routes
    """
    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    """
    Get all defined routes in the webserver
    """
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
