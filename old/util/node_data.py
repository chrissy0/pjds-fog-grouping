leader_name_string = "c-vm-1"
# leader_ip_string = "34.141.42.138"
leader_ip_string = "35.234.77.74"
# leader_secret_string = "tO8eV7ce1Xmnb1mLKjotq1EfBiMlhKnqpPrggLmxbD9h5BNYVq0gRc8Wcz1UTUB"
leader_secret_string = "u1JeSXGlbSJ14kLCPqkYSd2ZUhEjLP88OJeOumZrQpMp9Pe0yVwFG7kthyXNOa3"
group_nodes_list = [
    # {
    #     "name": "c-vm-2",
    #     "ip": "34.141.42.138",
    #     "secret": "C9PqbCFeDwM86TilqilfoPqm4he0RONlTVFmFEuhjrHDB1vLkw8GAi2w2hX6yeJ"
    # },
    # {
    #     "name": "c-vm-3",
    #     "ip": "35.234.98.158",
    #     "secret": "MX6qfzRSi5UzvPDii3Z4H1sgQWBxcnxApgUE0NpyUkh59LNri6HlefIxmu8EpXb"
    # },
    {
        "name": "c-vm-4",
        "ip": "34.89.225.105",
        "secret": "9TVFkvvpCbOAbUL7iueJ9skC3dhMlYI27fZjKDrrPdwa3k7oEOZRqxxV0BBvB0p"
    },
    {
        "name": "c-vm-5",
        "ip": "35.234.127.204",
        "secret": "BD1EEVVhCdSJ3Ie8Ylda7ANyWpThRBmdu07iCjayUx1vXw9GW8ce0OwLoZcmKFM"
    },
    # {
    #     "name": "c-vm-6",
    #     "ip": "34.141.87.143",
    #     "secret": "SZFmqbT51MdKljTUk7jiMmfmJzoqzv3NIq81zpovUK9a0UVMH0VUUFxKRTuPJ4b"
    # },
    # {
    #     "name": "c-vm-7",
    #     "ip": "35.234.116.231",
    #     "secret": "MyhySoanORiw2QnIL3Z04gMSWmUGyOq6p9TNd3IybDUDfigpN1A6aVLtDWoh5Tp"
    # },
    # {
    #     "name": "c-vm-8",
    #     "ip": "34.141.8.189",
    #     "secret": "9NnDFhUwZoHmZpUIMjU4YI7qLqsugb7lwbnI7BEovVsAifwcW79UVP27AvBSNd6"
    # }
]


def leader_name():
    return leader_name_string


def leader_ip():
    return leader_ip_string


def leader_secret():
    return leader_secret_string


def group_nodes():
    return group_nodes_list

