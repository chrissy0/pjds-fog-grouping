import requests
import json
import pickle
import datetime as dt
import time



measurements = [[], []]

counter = 1
while(True):
    try:
        response = requests.get(f"http://34.105.244.35:5002/get-node-info")
        measurement1 = (dt.datetime.now(), json.loads(response.text)["node_info"])
        measurements[0].append(measurement1)
        print(f"1 --- {measurement1}")
    except:
        pass

    pickle.dump(measurements,
                open(f"{dt.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}_{counter:04d}.p", "wb"))
    time.sleep(10)
    counter += 1