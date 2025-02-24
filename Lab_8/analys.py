import matplotlib.pyplot as plt

def parse_data(file_name):
    sizes = []
    min_heap_insert_times = []
    min_heap_search_times = []
    min_heap_remove_times = []
    binomial_heap_insert_times = []
    binomial_heap_remove_times = []

    with open(file_name, 'r') as file:
        lines = file.readlines()

    for i in range(0, len(lines), 3):
        # Разбираем данные для N
        size_line = lines[i].strip()
        min_heap_line = lines[i+1].strip()
        binomial_heap_line = lines[i+2].strip()

        # Извлекаем N
        size = int(size_line.split('=')[1])

        # Извлекаем время для MinHeap
        min_heap_insert = float(min_heap_line.split('Insert:')[1].split(',')[0].strip())
        min_heap_search = float(min_heap_line.split('Search:')[1].split(',')[0].strip())
        min_heap_remove = float(min_heap_line.split('Remove:')[1].strip())

        # Извлекаем время для BinomialHeap
        binomial_heap_insert = float(binomial_heap_line.split('Insert:')[1].split(',')[0].strip())
        binomial_heap_remove = float(binomial_heap_line.split('Remove:')[1].strip())

        sizes.append(size)
        min_heap_insert_times.append(min_heap_insert)
        min_heap_search_times.append(min_heap_search)
        min_heap_remove_times.append(min_heap_remove)
        binomial_heap_insert_times.append(binomial_heap_insert)
        binomial_heap_remove_times.append(binomial_heap_remove)

    return sizes, min_heap_insert_times, min_heap_search_times, min_heap_remove_times, \
           binomial_heap_insert_times, binomial_heap_remove_times

def plot_graphs(sizes, min_heap_insert_times, min_heap_search_times, min_heap_remove_times,
                binomial_heap_insert_times, binomial_heap_remove_times):
    # График для усредненного времени
    plt.figure(figsize=(10, 6))

    plt.plot(sizes, min_heap_insert_times, label='MinHeap Insert (avg)', marker='o')
    plt.plot(sizes, min_heap_search_times, label='MinHeap Search (avg)', marker='o')
    plt.plot(sizes, min_heap_remove_times, label='MinHeap Remove (avg)', marker='o')
    plt.plot(sizes, binomial_heap_insert_times, label='BinomialHeap Insert (avg)', marker='o')
    plt.plot(sizes, binomial_heap_remove_times, label='BinomialHeap Remove (avg)', marker='o')

    plt.xlabel('Number of elements (N)', fontsize=12)
    plt.ylabel('Time (seconds)', fontsize=12)
    plt.title('Average Time per Operation (1000 operations)', fontsize=14)
    plt.legend()
    plt.grid(True)
    plt.show()

    # График для максимального времени
    max_min_heap_insert = max(min_heap_insert_times)
    max_min_heap_search = max(min_heap_search_times)
    max_min_heap_remove = max(min_heap_remove_times)
    max_binomial_heap_insert = max(binomial_heap_insert_times)
    max_binomial_heap_remove = max(binomial_heap_remove_times)

    max_times = [max_min_heap_insert, max_min_heap_search, max_min_heap_remove,
                 max_binomial_heap_insert, max_binomial_heap_remove]

    labels = ['MinHeap Insert', 'MinHeap Search', 'MinHeap Remove',
              'BinomialHeap Insert', 'BinomialHeap Remove']

    plt.figure(figsize=(10, 6))

    plt.bar(labels, max_times, color=['b', 'g', 'r', 'c', 'm'])
    plt.ylabel('Max Time (seconds)', fontsize=12)
    plt.title('Maximum Time for One Operation', fontsize=14)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Путь к файлу с данными
    file_name = 'data.txt'
    sizes, min_heap_insert_times, min_heap_search_times, min_heap_remove_times, \
    binomial_heap_insert_times, binomial_heap_remove_times = parse_data(file_name)

    # Построение графиков
    plot_graphs(sizes, min_heap_insert_times, min_heap_search_times, min_heap_remove_times,
                binomial_heap_insert_times, binomial_heap_remove_times)
