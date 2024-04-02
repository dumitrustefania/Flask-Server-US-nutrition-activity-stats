"""
Unit tests for the webserver
"""

import unittest
import json
from time import sleep
import requests

from app import requests_solver
from unittests import constants

class TestWebserver(unittest.TestCase):
    """
    Test class
    """

    def test_states_mean(self):
        """
        Test the states_mean helper function
        """
        result = requests_solver.states_mean(constants.mock_df1, "Question1")
        self.assertEqual(result, {"State1": 127.5, "State2": 18.5})

    def test_state_mean(self):
        """
        Test the state_mean helper function
        """
        result = requests_solver.state_mean(constants.mock_df1, "Question1", "State1")
        self.assertEqual(result, {"State1": 127.5})

    def test_best5(self):
        """
        Test the best5 helper function
        """
        result = requests_solver.best5(constants.mock_df2, "Question1")
        self.assertEqual(
            result,
            {
                "State1": 127.5,
                "State3": 292.5,
                "State4": 332.5,
                "State5": 187.5,
                "State6": 149.0,
            },
        )

    def test_worst5(self):
        """
        Test the worst5 helper function
        """
        result = requests_solver.worst5(constants.mock_df2, "Question1")
        self.assertEqual(
            result,
            {
                "State1": 127.5,
                "State3": 292.5,
                "State2": 18.5,
                "State5": 187.5,
                "State6": 149.0,
            },
        )

    def test_global_mean(self):
        """
        Test the global_mean helper function
        """
        result = requests_solver.global_mean(constants.mock_df1, "Question1")
        self.assertEqual(result, {"global_mean": 73})

    def test_diff_from_mean(self):
        """
        Test the diff_from_mean helper function
        """
        result = requests_solver.diff_from_mean(constants.mock_df1, "Question1")
        self.assertEqual(result, {"State1": -54.5, "State2": 54.5})

    def test_state_diff_from_mean(self):
        """
        Test the state_diff_from_mean helper function
        """
        result = requests_solver.state_diff_from_mean(
            constants.mock_df1, "Question1", "State1"
        )
        self.assertEqual(result, {"State1": -54.5})

    def test_mean_by_category(self):
        """
        Test the mean_by_category helper function
        """
        result = requests_solver.mean_by_category(constants.mock_df3, "Question1")
        self.assertEqual(
            result,
            {
                "('State1', 'Category1', 'SubCategory1')": 127.5,
                "('State1', 'Category1', 'SubCategory2')": 10.0,
                "('State1', 'Category2', 'SubCategory3')": 12.0,
                "('State2', 'Category1', 'SubCategory1')": 249.0,
                "('State2', 'Category1', 'SubCategory2')": 3.0,
            },
        )

    def test_state_mean_by_category(self):
        """
        Test the state_mean_by_category helper function
        """
        result = requests_solver.state_mean_by_category(
            constants.mock_df3, "Question1", "State1"
        )
        self.assertEqual(
            result,
            {
                "State1": {
                    "('Category1', 'SubCategory1')": 127.5,
                    "('Category1', 'SubCategory2')": 10.0,
                    "('Category2', 'SubCategory3')": 12.0,
                }
            },
        )

    def test_invalid_job_id(self):
        """
        Test the behavior of the webserver when an invalid job_id is provided
        """
        with self.subTest():
            res = requests.get("http://127.0.0.1:5000/api/get_results/100001", timeout=10)
            self.assertEqual(res.status_code, 500)
            self.assertEqual(res.json(), {"status": "error", "reason": "Invalid job_id"})

    def test_bad_request1(self):
        """
        Test the behavior of the webserver when a request without the proper
        payload keys is provided
        """
        with self.subTest():
            bad_req_data = {"not-question": constants.mock_question}
            req = requests.post("http://127.0.0.1:5000/api/states_mean",
                                json=bad_req_data, timeout=10)
            self.assertEqual(req.status_code, 200)
            job_id = req.json()["job_id"]

            res = requests.get(f"http://127.0.0.1:5000/api/get_results/{job_id}", timeout=10)
            self.assertEqual(res.status_code, 400)
            self.assertEqual(
                res.json(), {"status": "error", "data": {"error_message": "Invalid input"}}
            )

    def test_bad_request2(self):
        """
        Test the behavior of the webserver when a request with an invalid
        question payload is provided
        """
        with self.subTest():
            bad_req_data = {"question": "Something not in the data"}
            req = requests.post("http://127.0.0.1:5000/api/states_mean",
                                json=bad_req_data, timeout=10)
            self.assertEqual(req.status_code, 200)
            job_id = req.json()["job_id"]

            res = requests.get(f"http://127.0.0.1:5000/api/get_results/{job_id}", timeout=10)
            self.assertEqual(res.status_code, 400)
            self.assertEqual(
                res.json(), {"status": "error", "data": {"error_message": "Invalid input"}}
            )

    def test_jobs(self):
        """
        Test the functionality of the /api/jobs endpoint
        """
        with self.subTest():
            # Get the initial status of jobs
            res = requests.get("http://127.0.0.1:5000/api/jobs", timeout=10)
            self.assertEqual(res.status_code, 200)
            jobs = res.json()["data"]

            # Submit 2 more requests
            req_data = {"question": constants.mock_question}

            req1 = requests.post("http://127.0.0.1:5000/api/states_mean", json=req_data, timeout=10)
            self.assertEqual(req1.status_code, 200)
            job_id1 = req1.json()["job_id"]

            req2 = requests.post("http://127.0.0.1:5000/api/best5", json=req_data, timeout=10)
            self.assertEqual(req2.status_code, 200)

            job_id2 = req2.json()["job_id"]

            sleep(1)
            res = requests.get("http://127.0.0.1:5000/api/jobs")
            self.assertEqual(res.status_code, 200)

            # Check that the new jobs are in the list
            jobs.append({f"job_id_{job_id1}": "done"})
            jobs.append({f"job_id_{job_id2}": "done"})
            self.assertEqual(res.json(), {"status": "done", "data": jobs})

    def test_zgraceful_shutdown_and_num_jobs(self):
        """
        Test the functionality of the /api/graceful_shutdown and /api/num_jobs endpoints
        """
        with self.subTest():
            # Create 1 more request
            req_data = json.dumps({"question": constants.mock_question})
            req = requests.post("http://127.0.0.1:5000/api/states_mean", json=req_data, timeout=10)
            self.assertEqual(req.status_code, 200)

            # Ask for shutdown
            res = requests.get("http://127.0.0.1:5000/api/graceful_shutdown", timeout=10)
            self.assertEqual(res.status_code, 200)

            sleep(1)
            # After some time, the number of running jobs should be 0
            res = requests.get("http://127.0.0.1:5000/api/num_jobs", timeout=10)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json(), {"status": "done", "data": 0})
