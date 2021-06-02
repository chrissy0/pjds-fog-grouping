from flask import Flask, request
import json
from node import Node


class NodeRest:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    node = None
    is_leader = False
    group_id = None

    def run(self):
        api = Flask(__name__)

        @api.route('/init', methods=['POST'])
        def init_node():
            if self.node is not None:
                return {
                           "message": "Node has already been initialized."
                       }, 500
            body = json.loads(request.data)
            self.node = Node(body["cpu_power"], body["storage_byte"], body["ram_byte"], body["latitude"], body["longitude"])
            return "", 200


        @api.route('/update_location', methods=['POST'])
        def update_location():
            if self.node is None:
                return {
                           "message": "Node has not been initialized, yet."
                       }, 500
            body = json.loads(request.data)
            self.node.update_location(body["latitude"], body["longitude"])
            return "", 200


        @api.route('/info', methods=['GET'])
        def get_info():
            if self.node is None:
                return {
                           "message": "Node has not been initialized, yet."
                       }, 500
            return json.dumps(self.node.get_info())


        @api.route('/node_id', methods=['GET'])
        def get_node_id():
            if self.node is None:
                return {
                           "message": "Node has not been initialized, yet."
                       }, 500
            return self.node.get_info()["id"]


        @api.route('/set_peers', methods=['POST'])
        def set_peers():
            if self.node is None:
                return {
                           "message": "Node has not been initialized, yet."
                       }, 500
            body = json.loads(request.data)
            self.node.set_peers(body)
            print(f"peers: {self.node.peers}")
            return "", 200


        api.run(port=self.port)
