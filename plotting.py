import matplotlib.pyplot as plt


def plot_nodes(node_info_list):
    x = list(map(lambda info: info["location"]["longitude"], node_info_list))
    y = list(map(lambda info: info["location"]["latitude"], node_info_list))

    plt.scatter(x, y, marker="x")
    plt.xlabel("longitude")
    plt.ylabel("latitude")
    plt.show()