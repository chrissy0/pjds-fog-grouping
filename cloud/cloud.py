from math import sin, cos, sqrt, atan2, radians

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
    location = {
        "lon": request.form["lon"],
        "lat": request.form["lat"]
    }
    # Overwrites old entries
    clusters[ip] = {
        "port": port,
        "location": location
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


if __name__ == '__main__':
    app.run(host="0.0.0.0")
