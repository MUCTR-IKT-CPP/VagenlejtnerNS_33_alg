import hashlib
import random
import time
import matplotlib.pyplot as plt
import numpy as np


# Реализация SHA-1
def sha1_hash(string):
    sha1 = hashlib.sha1()
    sha1.update(string.encode('utf-8'))
    return sha1.hexdigest()


# Генерация строки с отличиями
def generate_modified_string(base_str, num_changes):
    base_list = list(base_str)
    for _ in range(num_changes):
        index = random.randint(0, len(base_str) - 1)
        base_list[index] = random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    return ''.join(base_list)


# Проверка одинаковых последовательностей в хешах
def find_longest_common_sequence(hash1, hash2):
    max_len = 0
    for i in range(len(hash1)):
        for j in range(i + 1, len(hash1) + 1):
            if hash1[i:j] in hash2:
                max_len = max(max_len, j - i)
    return max_len


# Тестирование с разными количеством отличий в строках
def test_hash_similarity():
    base_string = 'a' * 128
    differences = [1, 2, 4, 8, 16]
    results = []

    for diff in differences:
        max_lengths = []
        for _ in range(1000):  # 1000 пар строк
            string1 = generate_modified_string(base_string, diff)
            string2 = generate_modified_string(base_string, diff)
            hash1 = sha1_hash(string1)
            hash2 = sha1_hash(string2)
            max_len = find_longest_common_sequence(hash1, hash2)
            max_lengths.append(max_len)

        avg_max_length = np.mean(max_lengths)
        results.append((diff, avg_max_length))

    # Построение графика
    diffs, avg_max_lengths = zip(*results)
    plt.plot(diffs, avg_max_lengths, label="Average Max Length")
    plt.xlabel("Number of Differences")
    plt.ylabel("Max Length of Common Sequence")
    plt.title("Hash Similarity for Different Number of Differences")
    plt.show()


# Тестирование на одинаковые хеши для разных N
def test_duplicate_hashes():
    results = []
    for i in range(2, 7):  # Для N = 10^i, где i от 2 до 6
        N = 10 ** i
        hashes = set()
        duplicates = 0
        for _ in range(N):
            random_string = ''.join(
                random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=256))
            h = sha1_hash(random_string)
            if h in hashes:
                duplicates += 1
            else:
                hashes.add(h)
        results.append((N, duplicates))

    # Вывод таблицы
    print("N (Generations) | Duplicate Hashes")
    for N, dup in results:
        print(f"{N} | {dup}")


# Тестирование времени хеширования для разных длин строк
def test_hash_time():
    sizes = [64, 128, 256, 512, 1024, 2048, 4096, 8192]
    times = []

    for size in sizes:
        start_time = time.time()
        for _ in range(1000):  # 1000 генераций
            random_string = ''.join(
                random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=size))
            sha1_hash(random_string)
        end_time = time.time()
        avg_time = (end_time - start_time) / 1000
        times.append(avg_time)

    # Построение графика
    plt.plot(sizes, times, label="Average Hash Time")
    plt.xlabel("String Size")
    plt.ylabel("Time (seconds)")
    plt.title("Hashing Time vs String Size")
    plt.show()


if __name__ == "__main__":
    # Запуск всех тестов
    test_hash_similarity()
    test_duplicate_hashes()
    test_hash_time()
