import requests
import threading
import time


class Thread(threading.Thread):
    def __init__(self, get, url, data, name):
        threading.Thread.__init__(self)
        self.url = url
        self.get = get
        self.data = data
        self.name = name

    def run(self):
        for i in range(5):
            start = time.time()
            if self.get:
                r = requests.get(f"http://127.0.0.1:5000/{self.url}")
            else:
                r = requests.post(f"http://127.0.0.1:5000/{self.url}", data=f"{self.data}")
            end = time.time()
            dur = end - start
            print(f"{self.name} {dur} {r.text}\n")


if __name__ == '__main__':
    t1 = Thread(True, "get-leader-address", "", "t1")
    t2 = Thread(False, "set-leader-address", "1.1.1.1", "t2")
    t3 = Thread(False, "set-address", "fn,1.2.3.4", "t3")
    t4 = Thread(False, "get-address", "fn1", "t4")
    t5 = Thread(False, "add-node", "2.2.2.2,12,11,qwertz", "t5")
    t6 = Thread(False, "add-fn", "fn11,2.2.2.2", "t6")
    t7 = Thread(False, "get-alternatives", "fn11", "t7")
    t8 = Thread(True, "get-all-nodes", "", "t8")

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
