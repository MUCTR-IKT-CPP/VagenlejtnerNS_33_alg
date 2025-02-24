from typing import Generic, TypeVar, List, Iterator, Optional, Any
from collections import namedtuple
import random
from datetime import datetime, timedelta

# Типовой шаблон
T = TypeVar('T')


# ---------- Реализация стека через массив ----------
class ArrayStack(Generic[T]):
    def __init__(self):
        self._data: List[T] = []

    def push(self, value: T) -> None:
        self._data.append(value)

    def pop(self) -> T:
        if not self._data:
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[T]:
        return reversed(self._data)


# ---------- Реализация стека через односвязный список ----------
class LinkedListStack(Generic[T]):
    class _Node(Generic[T]):
        def __init__(self, value: T, next_: Optional['LinkedListStack._Node'] = None):
            self.value = value
            self.next = next_

    def __init__(self):
        self._head: Optional[LinkedListStack._Node[T]] = None
        self._size = 0

    def push(self, value: T) -> None:
        new_node = self._Node(value, self._head)
        self._head = new_node
        self._size += 1

    def pop(self) -> T:
        if self._head is None:
            raise IndexError("pop from empty stack")
        value = self._head.value
        self._head = self._head.next
        self._size -= 1
        return value

    def is_empty(self) -> bool:
        return self._head is None

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        current = self._head
        while current is not None:
            yield current.value
            current = current.next


# ---------- Тесты ----------

# Тест 1: Заполнение контейнера числами и подсчет характеристик
def test_numeric_operations(stack_class: Any):
    stack = stack_class[int]()
    # Заполнение контейнера
    for _ in range(1000):
        stack.push(random.randint(-1000, 1000))

    # Итерация и подсчеты
    total = 0
    count = 0
    minimum = float('inf')
    maximum = float('-inf')

    for value in stack:
        total += value
        count += 1
        minimum = min(minimum, value)
        maximum = max(maximum, value)

    average = total / count if count > 0 else 0

    print(f"Test Numeric Operations ({stack_class.__name__}):")
    print(f"  Total: {total}, Average: {average}, Min: {minimum}, Max: {maximum}")
    return total, average, minimum, maximum


# Тест 2: Проверка строковых данных
def test_string_operations(stack_class: Any):
    stack = stack_class[str]()
    strings = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

    # Вставка элементов
    for s in strings:
        stack.push(s)

    # Извлечение и проверка
    results = []
    while not stack.is_empty():
        results.append(stack.pop())

    print(f"Test String Operations ({stack_class.__name__}):")
    print(f"  Results: {results}")


# Структура для тестирования данных о людях
Person = namedtuple('Person', ['last_name', 'first_name', 'patronymic', 'birth_date'])


# Генерация случайного человека
def random_person():
    last_names = ["Ivanov", "Petrov", "Sidorov", "Smirnov"]
    first_names = ["Ivan", "Petr", "Alexey", "Dmitry"]
    patronymics = ["Ivanovich", "Petrovich", "Alexeevich", "Dmitrievich"]
    birth_date_start = datetime(1980, 1, 1)
    birth_date_end = datetime(2020, 1, 1)
    birth_date = birth_date_start + timedelta(days=random.randint(0, (birth_date_end - birth_date_start).days))

    return Person(
        last_name=random.choice(last_names),
        first_name=random.choice(first_names),
        patronymic=random.choice(patronymics),
        birth_date=birth_date
    )


# Тест 3: Работа с данными о людях
def test_person_data(stack_class: Any):
    stack = stack_class[Person]()

    # Заполнение контейнера
    for _ in range(100):
        stack.push(random_person())

    # Фильтрация
    now = datetime.now()
    below_20 = []
    above_30 = []

    for person in stack:
        age = (now - person.birth_date).days // 365
        if age < 20:
            below_20.append(person)
        elif age > 30:
            above_30.append(person)

    print(f"Test Person Data ({stack_class.__name__}):")
    print(f"  Below 20: {len(below_20)}, Above 30: {len(above_30)}")


# Тест 4: Инвертирование содержимого
def test_inversion(stack_class: Any):
    stack = stack_class[int]()
    for i in range(1, 11):  # Заполнение отсортированными числами
        stack.push(i)

    inverted_stack = stack_class[int]()

    for value in stack:
        inverted_stack.push(value)

    print(f"Test Inversion ({stack_class.__name__}):")
    print(f"  Original: {list(stack)}")
    print(f"  Inverted: {list(inverted_stack)}")


# Тест 5: Сравнение производительности
def test_comparison():
    import time
    array_stack = ArrayStack[int]()
    linked_list_stack = LinkedListStack[int]()
    data = list(range(10000))

    # Тест скорости ArrayStack
    start = time.time()
    for value in data:
        array_stack.push(value)
    for _ in data:
        array_stack.pop()
    array_time = time.time() - start

    # Тест скорости LinkedListStack
    start = time.time()
    for value in data:
        linked_list_stack.push(value)
    for _ in data:
        linked_list_stack.pop()
    linked_time = time.time() - start

    print("Comparison:")
    print(f"  ArrayStack Time: {array_time:.5f} s")
    print(f"  LinkedListStack Time: {linked_time:.5f} s")


# Запуск тестов
test_numeric_operations(ArrayStack)
test_numeric_operations(LinkedListStack)
test_string_operations(ArrayStack)
test_string_operations(LinkedListStack)
test_person_data(ArrayStack)
test_person_data(LinkedListStack)
test_inversion(ArrayStack)
test_inversion(LinkedListStack)
test_comparison()
