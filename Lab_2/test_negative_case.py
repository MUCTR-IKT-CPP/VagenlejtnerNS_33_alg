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


def quicksort_deterministic(nums, depth=0):
    global recursion_calls, max_recursion_depth, swap_operations

    recursion_calls += 1
    max_recursion_depth = max(max_recursion_depth, depth)

    if len(nums) <= 1:
        return nums
    else:
        q = nums[len(nums) // 2]
        l_nums = [n for n in nums if n < q]
        e_nums = [q] * nums.count(q)
        b_nums = [n for n in nums if n > q]

        swap_operations += len(l_nums) + len(b_nums)

        return quicksort_deterministic(l_nums, depth + 1) + e_nums + quicksort_deterministic(b_nums, depth + 1)


def test_negative_case(test_type, nums, sort_function, results_file):
    global recursion_calls, max_recursion_depth, swap_operations

    recursion_calls = 0
    max_recursion_depth = 0
    swap_operations = 0

    start_time = time.time()
    sorted_nums = sort_function(nums)
    end_time = time.time()

    with open(results_file, "a", encoding="UTF-8") as file:
        file.write(
            f"Тест: {test_type} "
            f"Размер массива: {len(nums)} "
            f"Время выполнения: {end_time - start_time:.6f} "
            f"Рекурсии: {recursion_calls} "
            f"Максимальная глубина: {max_recursion_depth} "
            f"Операции замены: {swap_operations}\n"
        )


if __name__ == "__main__":

    results_file = "testing.txt"

    test_cases = [
        {
            "name": "Отсортированный массив",
            "generator": lambda size: list(range(size)),
            "sort_function": quicksort,
        },
        {
            "name": "Массив с одинаковыми элементами",
            "generator": lambda size: [0.1] * size,
            "sort_function": quicksort,
        },
        {
            "name": "Обратно отсортированный массив (Средний как pivot)",
            "generator": lambda size: list(uniform(0, -1) for _ in range(dimension)),
            "sort_function": quicksort,
        },
        {
            "name": "Обратно отсортированный массив (Детерминированный pivot)",
            "generator": lambda size: list(uniform(0, -1) for _ in range(dimension)),
            "sort_function": quicksort_deterministic,
        },
    ]

    dimensions = [1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000]

    for _ in range(20):
        for test in test_cases:
            for dimension in dimensions:
                nums = test["generator"](dimension)
                test_negative_case(test["name"], nums, test["sort_function"], results_file)
