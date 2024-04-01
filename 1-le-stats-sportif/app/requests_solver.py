import os
import json

class RequestsSolver:
    def __init__(self, webserver):
        self.webserver = webserver
        self.data = webserver.data_ingestor.data

    def write_result(self, result, job_id, status = "done"):
        os.makedirs("results", exist_ok=True)
        with open(f"results/job_id_{job_id}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(result))

        self.webserver.job_status[job_id] = status

    def get_input_question(self, request_args):
        if ("question" not in request_args.keys()) or (request_args["question"] not in self.webserver.data_ingestor.questions):
            return None
        
        return request_args["question"]
    
    def get_input_state(self, request_args):
        if ("state" not in request_args.keys()) or (request_args["state"] not in self.webserver.data_ingestor.states):
            return None

        return request_args["state"]
    
    def states_mean(self, job_id: int, request_args: dict):
        question = self.get_input_question(request_args)
        if question is None:
            self.write_result({"error_message": "Invalid input"}, job_id, "error")
            return
        
        filtered_data = self.data[self.data["Question"] == question]
        state_avg = filtered_data.groupby("LocationDesc")["Data_Value"].mean()
        state_avg_sorted = state_avg.sort_values()
        result = state_avg_sorted.to_dict()
        
        self.write_result(result, job_id)
    
    def state_mean(self, job_id: int, request_args: dict):
        question = self.get_input_question(request_args)
        state = self.get_input_state(request_args)
        if question is None or state is None:
            self.write_result({"error_message": "Invalid input"}, job_id, "error")
            return
        
        filtered_data = self.data[(self.data["Question"] == question) & (self.data["LocationDesc"] == state)]
        state_avg = filtered_data["Data_Value"].mean()
        result = {state: state_avg}

        self.write_result(result, job_id)

    def best5(self, job_id: int, request_args: dict):
        question = self.get_input_question(request_args)
        if question is None:
            self.write_result({"error_message": "Invalid input"}, job_id, "error")
            return

        filtered_data = self.data[self.data["Question"] == question]
        state_avg = filtered_data.groupby("LocationDesc")["Data_Value"].mean()
        
        if question in self.webserver.data_ingestor.questions_best_is_min:
            state_avg_sorted = state_avg.sort_values()
        else:
            state_avg_sorted = state_avg.sort_values(ascending=False)

        result = dict(list(state_avg_sorted.to_dict().items())[:5])

        self.write_result(result, job_id)

    def worst5(self, job_id: int, request_args: dict):
        question = self.get_input_question(request_args)
        if question is None:
            self.write_result({"error_message": "Invalid input"}, job_id, "error")
            return
        
        filtered_data = self.data[self.data["Question"] == question]
        state_avg = filtered_data.groupby("LocationDesc")["Data_Value"].mean()
        
        if question in self.webserver.data_ingestor.questions_best_is_min:
            state_avg_sorted = state_avg.sort_values(ascending=False)
        else:
            state_avg_sorted = state_avg.sort_values()

        result = dict(list(state_avg_sorted.to_dict().items())[:5])

        self.write_result(result, job_id)

    def global_mean(self, job_id: int, request_args: dict):
        question = self.get_input_question(request_args)
        if question is None:
            self.write_result({"error_message": "Invalid input"}, job_id, "error")
            return
        
        filtered_data = self.data[self.data["Question"] == question]
        global_avg = filtered_data["Data_Value"].mean()

        result = {"global_mean": global_avg}

        self.write_result(result, job_id)

    def diff_from_mean(self, job_id: int, request_args: dict):
        question = self.get_input_question(request_args)
        if question is None:
            self.write_result({"error_message": "Invalid input"}, job_id, "error")
            return

        filtered_data = self.data[self.data["Question"] == question]
        global_avg = filtered_data["Data_Value"].mean()
        states_avg = filtered_data.groupby("LocationDesc")["Data_Value"].mean()
        result = {state: global_avg - state_avg for state, state_avg in states_avg.to_dict().items()}
        
        self.write_result(result, job_id)

    def state_diff_from_mean(self, job_id: int, request_args: dict):
        question = self.get_input_question(request_args)
        state = self.get_input_state(request_args)
        if question is None or state is None:
            self.write_result({"error_message": "Invalid input"}, job_id, "error")
            return
        
        question_filtered_data = self.data[self.data["Question"] == question]
        global_avg = question_filtered_data["Data_Value"].mean()

        question_and_state_filtered_data = question_filtered_data[question_filtered_data["LocationDesc"] == state]
        state_avg = question_and_state_filtered_data["Data_Value"].mean()

        result = {state: global_avg - state_avg}
        
        self.write_result(result, job_id)

    def mean_by_category(self, job_id: int, request_args: dict):
        question = self.get_input_question(request_args)
        if question is None:
            self.write_result({"error_message": "Invalid input"}, job_id, "error")
            return

        filtered_data = self.data[self.data["Question"] == question]
        states_categories_avg = filtered_data.groupby(["LocationDesc", "StratificationCategory1", "Stratification1"])["Data_Value"].mean()
        result = {str(key): value for key, value in states_categories_avg.to_dict().items()}

        self.write_result(result, job_id)

    def state_mean_by_category(self, job_id: int, request_args: dict):
        question = self.get_input_question(request_args)
        state = self.get_input_state(request_args)
        if question is None or state is None:
            self.write_result({"error_message": "Invalid input"}, job_id, "error")
            return

        filtered_data = self.data[(self.data["Question"] == question) & (self.data["LocationDesc"] == state)]
        states_categories_avg = filtered_data.groupby(["StratificationCategory1", "Stratification1"])["Data_Value"].mean()
        result = {state: {str(key): value for key, value in states_categories_avg.to_dict().items()}}

        self.write_result(result, job_id)