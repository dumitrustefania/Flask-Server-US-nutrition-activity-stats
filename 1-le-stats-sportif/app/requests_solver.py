from app import webserver
import pandas as pd
import os
import json

class RequestsSolver:
    def __init__(self, data):
        self.data = data

    def states_mean(self, job_id: int, request_args: dict):
        question = request_args["question"]

        print(f"states_mean: job_id: {job_id}, question: {question}")

        filtered_data = self.data[self.data["Question"] == question]
        state_avg = filtered_data.groupby("LocationDesc")["Data_Value"].mean()
        state_avg_sorted = state_avg.sort_values()

        os.makedirs("results", exist_ok=True)
        with open(f"results/{job_id}.out", "w", encoding="utf-8") as f:
            f.write(json.dumps(state_avg_sorted.to_dict()))
    
        webserver.job_status[job_id] = "done"

    def state_mean(self, job_id: int, request_args: dict):
        question = request_args["question"]
        state = request_args["state"]

        print(f"states_mean: job_id: {job_id}, question: {question}, state: {state}")

        filtered_data = self.data[(self.data["Question"] == question) & (self.data["LocationDesc"] == state)]
        state_avg = filtered_data["Data_Value"].mean()
        print(state_avg)

        os.makedirs("results", exist_ok=True)
        with open(f"results/{job_id}.out", "w", encoding="utf-8") as f:
            f.write(json.dumps({state: state_avg}))
    
        webserver.job_status[job_id] = "done"

