"""
Helper functions to solve the POST requests made to the webserver
"""

import os
import json
from app import constants

def states_mean(data, question):
    """
    Compute the average value for a question for each state
    """
    filtered_data = data[data["Question"] == question]
    state_avg = filtered_data.groupby("LocationDesc")["Data_Value"].mean()
    state_avg_sorted = state_avg.sort_values()
    return state_avg_sorted.to_dict()

def state_mean(data, question, state):
    """
    Compute the average value for a question for a specific state
    """
    filtered_data = data[(data["Question"] == question) & (data["LocationDesc"] == state)]
    state_avg = filtered_data["Data_Value"].mean()
    return {state: state_avg}

def best5(data, question):
    """
    Compute the 5 states with the best average value for a question
    """
    states_avg = states_mean(data, question)
    if question in constants.QUESTIONS_BEST_IS_MIN:
        return dict(list(states_avg.items())[:5])

    return dict(list(states_avg.items())[-5:])

def worst5(data, question):
    """
    Compute the 5 states with the worst average value for a question
    """
    states_avg = states_mean(data, question)
    if question not in constants.QUESTIONS_BEST_IS_MIN:
        return dict(list(states_avg.items())[:5])

    return dict(list(states_avg.items())[-5:])

def global_mean(data, question):
    """
    Compute the global average value for a question
    """
    filtered_data = data[data["Question"] == question]
    global_avg = filtered_data["Data_Value"].mean()
    return {"global_mean": global_avg}

def diff_from_mean(data, question):
    """
    Compute the difference between the global average value and the average value for each state
    """
    states_avg = states_mean(data, question)
    global_avg = global_mean(data, question)["global_mean"]
    return {state: global_avg - state_avg for state, state_avg in states_avg.items()}

def state_diff_from_mean(data, question, state):
    """
    Compute the difference between the global average value and
    the average value for a specific state
    """
    state_avg = state_mean(data, question, state)[state]
    global_avg = global_mean(data, question)["global_mean"]
    return {state: global_avg - state_avg}

def mean_by_category(data, question):
    """
    Compute the average value for a question for each state and each subcategory in a category
    """
    filtered_data = data[data["Question"] == question]
    states_categories_avg = filtered_data.groupby(
        ["LocationDesc", "StratificationCategory1", "Stratification1"]
    )["Data_Value"].mean()
    return {str(key): value for key, value in states_categories_avg.to_dict().items()}

def state_mean_by_category(data, question, state):
    """
    Compute the average value for a question for a specific state and each subcategory in a category
    """
    filtered_data = data[(data["Question"] == question) & (data["LocationDesc"] == state)]
    states_categories_avg = filtered_data.groupby(
        ["StratificationCategory1", "Stratification1"]
    )["Data_Value"].mean()
    return {state: {str(key): value for key, value in states_categories_avg.to_dict().items()}}

class RequestsSolver:
    """
    Helper class to solve the POST requests made to the webserver
    """
    def __init__(self, webserver):
        self.webserver = webserver

    def write_result(self, result, job_id, status = "done"):
        """
        Given the result in the form of a dictionary and the status for the processed action,
        write them to a JSON file named after the job_id
        """
        os.makedirs("results", exist_ok=True)
        with open(f"results/job_id_{job_id}.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(result))

        self.webserver.job_status[job_id] = status

    def solver(self, endpoint, job_id, request_args, has_state = False):
        """
        Helper function for the requests that require a question and a state as input
        Checks the validity of the input and delegates the computation to the endpoint function
        """
        result = {}

        if ("question" not in request_args.keys()) or (
            request_args["question"] not in constants.QUESTIONS):
            self.write_result({"error_message": "Invalid input"}, job_id, "error")
            return
        question = request_args["question"]

        if has_state is True:
            if ("state" not in request_args.keys()) or (
                request_args["state"] not in constants.STATES):
                self.write_result({"error_message": "Invalid input"}, job_id, "error")
                return

            state = request_args["state"]

            result = endpoint(self.webserver.data, question, state)
        else:
            result = endpoint(self.webserver.data, question)

        self.write_result(result, job_id)
