from node_rest import NodeRest
from threading import Thread

# starts rest APIs on given ports
from_port = 5000
to_port = 5010
for port in range(from_port, to_port + 1):
    node_rest = NodeRest(port)
    thread = Thread(target=node_rest.run)
    thread.start()
