from math import sin, cos, sqrt, atan2, radians
import json

import requests
from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

clusters = {}


def calculate_distance(location1, location2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(float(location1["lat"]))
    lon1 = radians(float(location1["lon"]))
    lat2 = radians(float(location2["lat"]))
    lon2 = radians(float(location2["lon"]))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance


def response_object(message=None, code=200):
    res = {"response": clusters}
    if message:
        res["message"] = message
    return res, code


@app.route('/register-cluster', methods=['POST'])
def register_cluster():
    ip = request.form["ip"]
    port = request.form["port"]
    openfaas_ip = request.form["openfaas_ip"]
    openfaas_secret = request.form["openfaas_secret"]
    location = {
        "lon": request.form["lon"],
        "lat": request.form["lat"]
    }
    # Overwrites old entries
    clusters[ip] = {
        "port": port,
        "location": location,
        "openfaas_ip": openfaas_ip,
        "openfaas_secret": openfaas_secret,
    }
    return response_object(f"Added cluster '{ip}:{port}'.")


@app.route('/deregister-cluster', methods=['DELETE'])
def deregister_cluster():
    ip = request.form["ip"]
    # Overwrites old entries
    try:
        del clusters[ip]
        return response_object(f"Deleted cluster ip '{ip}'.")
    except KeyError:
        return response_object(f"Cluster ip '{ip}' is already non-existent and cannot be deleted.", 409)


@app.route('/reset', methods=['DELETE'])
def reset():
    global clusters
    clusters = {}
    return response_object(f"Cloud was reset (all clusters were deregistered).")


@app.route('/cluster-suggestions', methods=['POST'])
def cluster_suggestions():
    request_source_ip = request.form["ip"]
    max_number_of_requested_clusters = int(request.form["limit"])

    if request_source_ip not in clusters:
        return response_object(f"Source ip is not known, thus surrounding clusters cannot be suggested.", 409)

    source_location = clusters[request_source_ip]["location"]

    clusters_incl_distance = list(map(lambda cluster: {
        "ip": cluster,
        "port": clusters[cluster]["port"],
        "distance": calculate_distance(source_location, clusters[cluster]["location"])
    }, clusters))
    clusters_incl_distance = filter(lambda cluster: cluster["ip"] != request_source_ip, clusters_incl_distance)
    clusters_incl_distance = sorted(clusters_incl_distance, key=lambda k: k['distance'])

    return jsonify({
        "closest_clusters": clusters_incl_distance[:max_number_of_requested_clusters]
    })


def deploy_function(target_ip, function_name, registry_url):
    cluster = clusters[target_ip]
    url = f"http://admin:{cluster['openfaas_secret']}@{cluster['openfaas_ip']}:8080/system/functions"

    headers = {
        'Content-Type': 'application/json'
    }

    # Deploy Function
    payload = json.dumps({
        "service": function_name,
        "network": "func_functions",
        "image": registry_url,
        "readOnlyRootFilesystem": True
    })

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code != 202:
        response = requests.request("PUT", url, headers=headers, data=payload)
    if response.status_code != 202:
        return False, function_name
    return True, None


@app.route('/deploy-functions', methods=['POST'])
def deploy_functions():
    deploy_request = request.get_json()
    target_ip = deploy_request["ip"]
    if target_ip not in clusters.keys():
        return response_object(f"Target cluster is unknown, has it been registered, yet?", 409)
    function_list = deploy_request["functions"]
    not_deployed = []
    for function in function_list:
        successful, failed_function_name = deploy_function(target_ip, function["name"], function["registry_url"])
        if not successful:
            not_deployed.append(failed_function_name)
    if len(not_deployed) != 0:
        return response_object(f"The following functions were not deployed: {not_deployed}", 409)
    return response_object("Deployed all functions.")


@app.route('/ping', methods=['GET'])
def ping_pong():
    return response_object("pong")


@app.errorhandler(Exception)
def exception_handler(error):
    return f"Error: {repr(error)}"


if __name__ == '__main__':
    app.run(host="0.0.0.0")
