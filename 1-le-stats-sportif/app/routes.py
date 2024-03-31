import os
import json

from app import webserver
from flask import request, jsonify

def submit_request(callable, request):
    if request.method == 'POST':
        # Get request data
        data = request.json
        print(f"Got request {data}")

        # Register job. Don't wait for task to finish
        job_id = webserver.job_counter
        webserver.job_status[job_id] = "running"
        webserver.tasks_runner.submit(callable, job_id, data)

        # Increment job_id counter
        webserver.job_counter += 1

        # Return associated job_id
        return jsonify({"job_id": job_id})
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    job_id = int(job_id)
    print(f"JobID is {job_id}")

    # Check if job_id is valid
    if job_id >= 1 and job_id < webserver.job_counter:        
        # Check if job_id is done and return the result
        if webserver.job_status[job_id] == "done":
            with open(f"results/job_id_{job_id}.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"Datele din fisier sunt: {data}")
                return jsonify({"status": "done", "data": data})
        else:
            return jsonify({"status": "running"})
    else:
        return jsonify({"status": "error", "reason": "Invalid job_id"})

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    return submit_request(webserver.requests_solver.states_mean, request)

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    return submit_request(webserver.requests_solver.state_mean, request)


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    return submit_request(webserver.requests_solver.best5, request)

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    return submit_request(webserver.requests_solver.worst5, request)

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    return submit_request(webserver.requests_solver.global_mean, request)

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    return submit_request(webserver.requests_solver.diff_from_mean, request)


@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    return submit_request(webserver.requests_solver.state_diff_from_mean, request)

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
   return submit_request(webserver.requests_solver.mean_by_category, request)

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    return submit_request(webserver.requests_solver.state_mean_by_category, request)

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def shutdown():
    webserver.tasks_runner.shutdown()
    return jsonify({"status": "done"})

@webserver.route('/api/jobs', methods=['GET'])
def get_jobs():
    statuses = [{"job_id_" + str(job_id): status} for job_id, status in webserver.job_status.items()]
    return jsonify({"status": "done", "data": statuses})

@webserver.route('/api/num_jobs', methods=['GET'])
def get_num_jobs():
    count = 0
    for val in webserver.job_status.values():
        if val == "running":
            count += 1

    return jsonify({"status": "done", "data": count})
    
# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
