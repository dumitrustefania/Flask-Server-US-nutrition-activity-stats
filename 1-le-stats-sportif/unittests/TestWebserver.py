import unittest
class TestWebserver(unittest.TestCase):
    def setUp(self):
        # os.system("rm -rf results/*")
        pass

    # def test_states_mean(self):
    #     output_dir = f"tests/{endpoint}/output/"
    #     input_dir = f"tests/{endpoint}/input/"
    #     input_files = os.listdir(input_dir)

    #     test_suite_score = 10
    #     test_score = test_suite_score / len(input_files)
    #     local_score = 0

    #     for input_file in input_files:
    #         # Get the index from in-idx.json
    #         # The idx is between a dash (-) and a dot (.)
    #         idx = input_file.split('-')[1]
    #         idx = int(idx.split('.')[0])

    #         with open(f"{input_dir}/{input_file}", "r") as fin:
    #             # Data to be sent in the POST request
    #             req_data = json.load(fin)

    #         with open(f"{output_dir}/out-{idx}.json", "r") as fout:
    #             ref_result = json.load(fout)
            
    #         with self.subTest():
    #             # Sending a POST request to the Flask endpoint
    #             res = requests.post(f"http://127.0.0.1:5000/api/{endpoint}", json=req_data)

    #             job_id = res.json()
    #             # print(f'job-res is {job_id}')
    #             job_id = job_id["job_id"]

    #             self.check_res_timeout(
    #                 res_callable = lambda: requests.get(f"http://127.0.0.1:5000/api/get_results/{job_id}"),
    #                 ref_result = ref_result,
    #                 timeout_sec = 1)
                
    #             local_score += test_score
    #     total_score += min(round(local_score), test_suite_score)
