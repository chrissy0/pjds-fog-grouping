leader_name_string = "some-name"
leader_ip_string = "some-ip"
leader_secret_string = "some-secret"
group_nodes_list = [
    {
        "name": "some-name",
        "ip": "some-ip",
        "secret": "some-secret"
    },
    {
        "name": "some-name",
        "ip": "some-ip",
        "secret": "some-secret"
    },
    {
        "name": "some-name",
        "ip": "some-ip",
        "secret": "some-secret"
    }
]


def leader_name():
    return leader_name_string


def leader_ip():
    return leader_ip_string


def leader_secret():
    return leader_secret_string


def group_nodes():
    return group_nodes_list

