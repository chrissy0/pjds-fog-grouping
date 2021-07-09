import requests
import psutil
import time

SQLITE_PORT = 5000


def get_leader_address():
    res = requests.get(f"http://localhost:{SQLITE_PORT}/get-leader-address")
    return res.text


if __name__ == '__main__':
    ip = requests.get('https://api.ipify.org').text
    while True:
        leader = get_leader_address()
        cpu_usage = psutil.getloadavg()[0] / psutil.cpu_count() * 100
        mem = psutil.virtual_memory()
        memory_usage = round(1 - mem.available / mem.total, 2)
        res = requests.post(f"http://{leader}:{SQLITE_PORT}/update-node", data=f"{ip},{cpu_usage},{memory_usage}")
        time.sleep(10)
