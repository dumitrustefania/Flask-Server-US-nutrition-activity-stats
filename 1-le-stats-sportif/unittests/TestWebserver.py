import unittest
import requests

from time import sleep
from app import requests_solver
from unittests import constants
import json

class TestWebserver(unittest.TestCase):
    def test_states_mean(self):
        result = requests_solver.states_mean(constants.mock_df1, "Question1")
        self.assertEqual(result, {'State1': 127.5, 'State2': 18.5})

    def test_state_mean(self):
        result = requests_solver.state_mean(constants.mock_df1, "Question1", "State1")
        self.assertEqual(result, {'State1': 127.5})
    
    def test_best5(self):
        result = requests_solver.best5(constants.mock_df2, "Question1")
        self.assertEqual(result, {'State1': 127.5, 'State3': 292.5, 'State4': 332.5, 'State5': 187.5, 'State6': 149.0})

    def test_worst5(self):
        result = requests_solver.worst5(constants.mock_df2, "Question1")
        self.assertEqual(result, {'State1': 127.5, 'State3': 292.5, 'State2': 18.5, 'State5': 187.5, 'State6': 149.0})

    def test_global_mean(self):
        result = requests_solver.global_mean(constants.mock_df1, "Question1")
        self.assertEqual(result, {'global_mean': 73})

    def test_diff_from_mean(self):
        result = requests_solver.diff_from_mean(constants.mock_df1, "Question1")
        self.assertEqual(result, {'State1': -54.5, 'State2': 54.5})

    def test_state_diff_from_mean(self):
        result = requests_solver.state_diff_from_mean(constants.mock_df1, "Question1", "State1")
        self.assertEqual(result, {'State1': -54.5})

    def test_mean_by_category(self):
        result = requests_solver.mean_by_category(constants.mock_df3, "Question1")
        self.assertEqual(result, {"('State1', 'Category1', 'SubCategory1')": 127.5,
                                  "('State1', 'Category1', 'SubCategory2')": 10.0,
                                  "('State1', 'Category2', 'SubCategory3')": 12.0,
                                  "('State2', 'Category1', 'SubCategory1')": 249.0,
                                  "('State2', 'Category1', 'SubCategory2')": 3.0})
        
    def test_state_mean_by_category(self):
        result = requests_solver.state_mean_by_category(constants.mock_df3, "Question1", "State1")
        self.assertEqual(result, {'State1': {"('Category1', 'SubCategory1')": 127.5,
                                            "('Category1', 'SubCategory2')": 10.0,
                                            "('Category2', 'SubCategory3')": 12.0}})
    
    def test_invalid_job_id(self):
        res = requests.get(f"http://127.0.0.1:5000/api/get_results/100001")
        self.assertEqual(res.status_code, 500)
        self.assertEqual(res.json(), {"status": "error", "reason": "Invalid job_id"})

    def test_bad_request1(self):
        bad_req_data = {"not-question": constants.mock_question}
        req = requests.post("http://127.0.0.1:5000/api/states_mean", json=bad_req_data)
        self.assertEqual(req.status_code, 200)
        job_id = req.json()["job_id"]

        res = requests.get(f"http://127.0.0.1:5000/api/get_results/{job_id}")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json(), {"status": "error", "data": {"error_message": "Invalid input"}})

    def test_bad_request2(self):
        bad_req_data = {"question": "Something not in the data"}
        req = requests.post("http://127.0.0.1:5000/api/states_mean", json=bad_req_data)
        self.assertEqual(req.status_code, 200)
        job_id = req.json()["job_id"]

        res = requests.get(f"http://127.0.0.1:5000/api/get_results/{job_id}")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json(), {"status": "error", "data": {"error_message": "Invalid input"}})

    def test_jobs(self):
        with self.subTest():
            res = requests.get("http://127.0.0.1:5000/api/jobs")
            self.assertEqual(res.status_code, 200)
            jobs = res.json()["data"]

            req_data = {"question": constants.mock_question}

            req1 = requests.post("http://127.0.0.1:5000/api/states_mean", json=req_data)
            self.assertEqual(req1.status_code, 200)
            job_id1 = req1.json()["job_id"]

            req2 = requests.post("http://127.0.0.1:5000/api/best5", json=req_data)
            self.assertEqual(req2.status_code, 200)

            job_id2 = req2.json()["job_id"]
            
            sleep(1)
            res = requests.get("http://127.0.0.1:5000/api/jobs")
            self.assertEqual(res.status_code, 200)
            jobs.append({f"job_id_{job_id1}": "done"})
            jobs.append({f"job_id_{job_id2}": "done"})
            self.assertEqual(res.json(), {"status": "done", "data": jobs})

    def test_zgraceful_shutdown_and_num_jobs(self):
        with self.subTest():
            req_data = json.dumps({"question": constants.mock_question})

            req = requests.post("http://127.0.0.1:5000/api/states_mean", json=req_data)
            self.assertEqual(req.status_code, 200)

            res = requests.get("http://127.0.0.1:5000/api/graceful_shutdown")
            self.assertEqual(res.status_code, 200)

            sleep(1)
            res = requests.get("http://127.0.0.1:5000/api/num_jobs")
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json(), {"status": "done" , "data": 0})
