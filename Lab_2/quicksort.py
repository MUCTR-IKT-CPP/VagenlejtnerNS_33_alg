import time
from random import choice, uniform


recursion_calls = 0
max_recursion_depth = 0
swap_operations = 0


def quicksort(nums, depth=0):
    global recursion_calls, max_recursion_depth, swap_operations

    recursion_calls += 1
    max_recursion_depth = max(max_recursion_depth, depth)

    if len(nums) <= 1:
        return nums
    else:
        q = choice(nums)
        l_nums = [n for n in nums if n < q]
        e_nums = [q] * nums.count(q)
        b_nums = [n for n in nums if n > q]

        swap_operations += len(l_nums) + len(b_nums)

        return quicksort(l_nums, depth + 1) + e_nums + quicksort(b_nums, depth + 1)


if __name__ == "__main__":

    dimensions = [1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000]

    for dimension in dimensions:
        for approach in range(20):
            nums = [uniform(-1, 1) for _ in range(dimension)]

            # Сброс счетчиков
            recursion_calls = 0
            max_recursion_depth = 0
            swap_operations = 0

            # Замер времени
            start_time = time.time()
            sorted_nums = quicksort(nums)
            end_time = time.time()
            execution_time = end_time - start_time

            # Запись результатов в файл
            with open("results.txt", "a", encoding='UTF-8') as file:
                file.write(
                    f"Размерность: {dimension} "
                    f"Время: {execution_time:.6f} "
                    f"Количество вызовов рекурсии: {recursion_calls} "
                    f"Глубина рекурсии: {max_recursion_depth} "
                    f"Количество обменов: {swap_operations}\n"
                )
