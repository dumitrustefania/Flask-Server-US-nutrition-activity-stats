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

        question_filtered_data = self.data[self.data["Question"] == question]
        state_avg = question_filtered_data.groupby("LocationDesc")["Data_Value"].mean()
        state_avg_sorted = state_avg.sort_values()

        os.makedirs("results", exist_ok=True)
        with open(f"results/{job_id}.out", "w", encoding="utf-8") as f:
            f.write(json.dumps(state_avg_sorted.to_dict()))
    
        webserver.job_status[job_id] = "done"

