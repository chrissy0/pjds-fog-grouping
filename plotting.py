import matplotlib.pyplot as plt
import numpy as np


def plot_nodes(node_info_list, longitude_limits, latitude_limits, number_of_rows, number_of_columns):

    x = list(map(lambda info: info["location"]["longitude"], node_info_list))
    y = list(map(lambda info: info["location"]["latitude"], node_info_list))
    colors = np.array(list(map(lambda info: (info["group"][0]-1) * number_of_columns + info["group"][1], node_info_list)))
    color_list = np.array(['b', 'g', 'r', 'c', 'm', 'y', 'k'])

    colors = color_list[colors % len(color_list)]

    plt.scatter(x, y, c=colors, marker=".")
    plt.xlabel("longitude")
    plt.ylabel("latitude")
    plt.xlim(longitude_limits)
    plt.ylim(latitude_limits)

    if number_of_columns > 1:
        width = longitude_limits[1] - longitude_limits[0]
        x_separators = (width / number_of_columns) * np.array(range(1, number_of_columns)) + longitude_limits[0]
        for x_separator in x_separators:
            plt.axvline(x=x_separator, ls="--", c="k", alpha=0.4)

    if number_of_rows > 1:
        height = latitude_limits[1] - latitude_limits[0]
        y_separators = (height / number_of_rows) * np.array(range(1, number_of_rows)) + latitude_limits[0]
        for y_separator in y_separators:
            plt.axhline(y=y_separator, ls="--", c="k", alpha=0.4)


    plt.show()
