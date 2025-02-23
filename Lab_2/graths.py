import matplotlib.pyplot as plt
import numpy as np


def read_results(file_name):
    data = {}
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(" ")
            dimension = int(parts[1])
            time = float(parts[3])
            recursion_calls = int(parts[7])
            depth = int(parts[10])
            swaps = int(parts[13])

            if dimension not in data:
                data[dimension] = {
                    "time": [],
                    "recursion_calls": [],
                    "depth": [],
                    "swaps": []
                }
            data[dimension]["time"].append(time)
            data[dimension]["recursion_calls"].append(recursion_calls)
            data[dimension]["depth"].append(depth)
            data[dimension]["swaps"].append(swaps)

    return data


def build_graphs(data):
    dimensions = sorted(data.keys())

    x = np.array(dimensions)
    y_on = x * np.log2(x)

    C = max(max(data[dim]["time"]) for dim in dimensions) / max(y_on)
    y_on_scaled = C * y_on

    worst_times = [max(data[dim]["time"]) for dim in dimensions]

    plt.figure(figsize=(10, 6))
    plt.plot(dimensions, worst_times, label='Наихудшее время', marker='o')
    plt.plot(dimensions, y_on_scaled, label='O(N log N)', linestyle='--')
    plt.xlabel('Число элементов в массиве')
    plt.ylabel('Время выполнения (сек)')
    plt.title('Сравнение O(N log N) и наихудшего времени')
    plt.legend()
    plt.grid()
    plt.savefig("time_vs_on.png")
    plt.show()

    avg_times = [np.mean(data[dim]["time"]) for dim in dimensions]
    best_times = [min(data[dim]["time"]) for dim in dimensions]
    worst_times = [max(data[dim]["time"]) for dim in dimensions]

    plt.figure(figsize=(10, 6))
    plt.plot(dimensions, avg_times, label='Среднее время', marker='o')
    plt.plot(dimensions, best_times, label='Наилучшее время', marker='o')
    plt.plot(dimensions, worst_times, label='Наихудшее время', marker='o')
    plt.xlabel('Число элементов в массиве')
    plt.ylabel('Время выполнения (сек)')
    plt.title('Среднее, наилучшее и наихудшее время выполнения')
    plt.legend()
    plt.grid()
    plt.savefig("time_comparison.png")
    plt.show()

    avg_depth = [np.mean(data[dim]["depth"]) for dim in dimensions]
    best_depth = [min(data[dim]["depth"]) for dim in dimensions]
    worst_depth = [max(data[dim]["depth"]) for dim in dimensions]

    plt.figure(figsize=(10, 6))
    plt.plot(dimensions, avg_depth, label='Средняя глубина рекурсии', marker='o')
    plt.plot(dimensions, best_depth, label='Наилучшая глубина рекурсии', marker='o')
    plt.plot(dimensions, worst_depth, label='Наихудшая глубина рекурсии', marker='o')
    plt.xlabel('Число элементов в массиве')
    plt.ylabel('Глубина рекурсии')
    plt.title('Средняя, наилучшая и наихудшая глубина рекурсии')
    plt.legend()
    plt.grid()
    plt.savefig("recursion_depth_comparison.png")
    plt.show()

    avg_swaps = [np.mean(data[dim]["swaps"]) for dim in dimensions]
    best_swaps = [min(data[dim]["swaps"]) for dim in dimensions]
    worst_swaps = [max(data[dim]["swaps"]) for dim in dimensions]

    plt.figure(figsize=(10, 6))
    plt.plot(dimensions, avg_swaps, label='Среднее число обменов', marker='o')
    plt.plot(dimensions, best_swaps, label='Наилучшее число обменов', marker='o')
    plt.plot(dimensions, worst_swaps, label='Наихудшее число обменов', marker='o')
    plt.xlabel('Число элементов в массиве')
    plt.ylabel('Количество обменов')
    plt.title('Среднее, наилучшее и наихудшее количество обменов')
    plt.legend()
    plt.grid()
    plt.savefig("swap_operations_comparison.png")
    plt.show()

    avg_calls = [np.mean(data[dim]["recursion_calls"]) for dim in dimensions]
    best_calls = [min(data[dim]["recursion_calls"]) for dim in dimensions]
    worst_calls = [max(data[dim]["recursion_calls"]) for dim in dimensions]

    plt.figure(figsize=(10, 6))
    plt.plot(dimensions, avg_calls, label='Среднее число вызовов', marker='o')
    plt.plot(dimensions, best_calls, label='Наилучшее число вызовов', marker='o')
    plt.plot(dimensions, worst_calls, label='Наихудшее число вызовов', marker='o')
    plt.xlabel('Число элементов в массиве')
    plt.ylabel('Количество вызовов рекурсии')
    plt.title('Среднее, наилучшее и наихудшее количество вызовов рекурсии')
    plt.legend()
    plt.grid()
    plt.savefig("recursion_calls_comparison.png")
    plt.show()


if __name__ == "__main__":
    results_file = "results.txt"
    data = read_results(results_file)

    build_graphs(data)
