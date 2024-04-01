import os
import json

class RequestsSolver:
    def __init__(self, webserver):
        self.webserver = webserver
        self.data = webserver.data_ingestor.data
    
    def states_mean(self, question):
        filtered_data = self.data[self.data["Question"] == question]
        state_avg = filtered_data.groupby("LocationDesc")["Data_Value"].mean()
        state_avg_sorted = state_avg.sort_values()
        return state_avg_sorted.to_dict()
    
    def state_mean(self, question, state):
        filtered_data = self.data[(self.data["Question"] == question) & (self.data["LocationDesc"] == state)]
        state_avg = filtered_data["Data_Value"].mean()
        return {state: state_avg}
   
    def best5(self, question):
        states_avg = self.states_mean(question)
        if question in self.webserver.data_ingestor.questions_best_is_min:
            return dict(list(states_avg.items())[:5])
        else:
            return dict(list(states_avg.items())[-5:])

    def worst5(self, question):
        states_avg = self.states_mean(question)
        if question in self.webserver.data_ingestor.questions_best_is_max:
            return dict(list(states_avg.items())[:5])
        else:
            return dict(list(states_avg.items())[-5:])
        
    def global_mean(self, question):
        filtered_data = self.data[self.data["Question"] == question]
        global_avg = filtered_data["Data_Value"].mean()

        return {"global_mean": global_avg}

    def diff_from_mean(self, question):
        states_avg = self.states_mean(question)
        global_avg = self.global_mean(question)["global_mean"]
        return {state: global_avg - state_avg for state, state_avg in states_avg.items()}
        
    def state_diff_from_mean(self, question, state):
        state_avg = self.state_mean(question, state)[state]
        global_avg = self.global_mean(question)["global_mean"]
        return {state: global_avg - state_avg}

    def mean_by_category(self, question):
        filtered_data = self.data[self.data["Question"] == question]
        states_categories_avg = filtered_data.groupby(["LocationDesc", "StratificationCategory1", "Stratification1"])["Data_Value"].mean()
        return {str(key): value for key, value in states_categories_avg.to_dict().items()}

    def state_mean_by_category(self, question, state):
        filtered_data = self.data[(self.data["Question"] == question) & (self.data["LocationDesc"] == state)]
        states_categories_avg = filtered_data.groupby(["StratificationCategory1", "Stratification1"])["Data_Value"].mean()
        return {state: {str(key): value for key, value in states_categories_avg.to_dict().items()}}

    def write_result(self, result, job_id, status = "done"):
        os.makedirs("results", exist_ok=True)
        with open(f"results/job_id_{job_id}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(result))

        self.webserver.job_status[job_id] = status

    def question_solver(self, endpoint, job_id: int, request_args: dict):
        if ("question" not in request_args.keys()) or (request_args["question"] not in self.webserver.data_ingestor.questions):
            self.write_result({"error_message": "Invalid input"}, job_id, "error")
            return
        
        question = request_args["question"]
        result = endpoint(question)
        self.write_result(result, job_id)

    def question_and_state_solver(self, endpoint, job_id: int, request_args: dict):
        if ("question" not in request_args.keys()) or (request_args["question"] not in self.webserver.data_ingestor.questions):
            self.write_result({"error_message": "Invalid input"}, job_id, "error")
            return
        
        if ("state" not in request_args.keys()) or (request_args["state"] not in self.webserver.data_ingestor.states):
            self.write_result({"error_message": "Invalid input"}, job_id, "error")
            return

        question = request_args["question"]
        state = request_args["state"]
        result = endpoint(question, state)
        self.write_result(result, job_id)