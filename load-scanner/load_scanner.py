import requests
import psutil
import time

SQLITE_PORT = 5000


def get_leader_address():
    req = requests.get(f"http://localhost:{SQLITE_PORT}/get-leader-address")
    return req.text


def compute_cpu():
    return psutil.getloadavg()[0] / psutil.cpu_count() * 100


def compute_memory():
    mem = psutil.virtual_memory()
    return round(1 - mem.available / mem.total, 2)


if __name__ == '__main__':
    leader = get_leader_address()
    if len(leader) != 0:
        ip = requests.get('https://api.ipify.org').text
        f = open("/var/lib/faasd/secrets/basic-auth-password", "r")
        faasd_secret = f.read()
        requests.post(f"http://{leader}:{SQLITE_PORT}/add-node",
                      data=f"{ip},{compute_cpu()},{compute_memory()},{faasd_secret}")
        f.close()
        while True:
            time.sleep(10)
            leader = get_leader_address()
            r = requests.post(f"http://{leader}:{SQLITE_PORT}/update-node", data=f"{ip},{compute_cpu()},{compute_memory()}")
