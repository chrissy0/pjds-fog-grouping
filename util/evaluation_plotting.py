import pickle
import json

test_results = pickle.load(open("test_results_2021_07_18_22_21_59.p", "rb"))
print(json.dumps(test_results, indent=4))