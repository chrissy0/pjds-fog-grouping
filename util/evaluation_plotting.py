import pickle
import json
import numpy as np
import matplotlib.pyplot as plt



def plot_measurement(group_mode, group_size, duration, time):
    #time = np.array(time) - np.array(duration)*11
    plt.plot(duration, time, "--o", label=f"Mode: {group_mode} Group size: {group_size}")
    print(f"{group_mode}-{group_size}-{duration}-{time}")


def evaluate(test_results):
    measurements_over_duration = []

    for group_mode_data in test_results:
        group_mode = group_mode_data["group_mode"]
        for group_size_data in group_mode_data["group_sizes"]:
            group_size = group_size_data["group_size"]
            measurements_over_duration.append({
                "group_mode": group_mode,
                "group_size": group_size,
                "measurements": {
                    "duration": [],
                    "time": [],
                    "measurements_per_datapoint": 0
                }
            })
            for duration_data in group_size_data["durations"]:
                duration = duration_data["duration"]
                measurements = duration_data["measurements"]
                measurements_over_duration[-1]["measurements"]["duration"].append(duration)
                measurements_over_duration[-1]["measurements"]["time"].append(np.mean(measurements))
                measurements_over_duration[-1]["measurements"]["measurements_per_datapoint"] = len(measurements)



    for mod in measurements_over_duration:
        plot_measurement(mod["group_mode"], mod["group_size"], mod["measurements"]["duration"], mod["measurements"]["time"])
    plt.legend()
    plt.yscale("log")
    plt.xlabel("function duration in s")
    plt.ylabel("t in s (roundtrip)")
    plt.grid()
    plt.show()

    print()


if __name__ == "__main__":
    test_results = pickle.load(open("test_results_2021_07_21_04_54_42_grouped_3_1_1.p", "rb"))
    evaluate(test_results)