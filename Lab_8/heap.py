import time
import random
import heapq
import matplotlib.pyplot as plt


# Бинарная куча (мин-куча)
class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, val):
        heapq.heappush(self.heap, val)

    def get_min(self):
        return self.heap[0] if self.heap else None

    def remove_min(self):
        if len(self.heap) > 0:
            return heapq.heappop(self.heap)
        return None

    def size(self):
        return len(self.heap)


# Биноминальная куча
class BinomialNode:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = None
        self.child = None
        self.sibling = None


class BinomialHeap:
    def __init__(self):
        self.head = None

    def merge(self, other_heap):
        self.head = self._merge(self.head, other_heap.head)

    def _merge(self, h1, h2):
        if not h1: return h2
        if not h2: return h1

        # Старт итеративного слияния
        dummy = BinomialNode(None)  # Служебный узел для облегчения работы с головами
        current = dummy
        while h1 and h2:
            if h1.key < h2.key:
                current.sibling = h1
                h1 = h1.sibling
            else:
                current.sibling = h2
                h2 = h2.sibling
            current = current.sibling

        # Присоединяем оставшиеся элементы
        if h1:
            current.sibling = h1
        elif h2:
            current.sibling = h2

        return dummy.sibling  # Возвращаем новый список, начиная с первого элемента

    def insert(self, key):
        new_node = BinomialNode(key)
        new_heap = BinomialHeap()
        new_heap.head = new_node
        self.merge(new_heap)

    def get_min(self):
        if not self.head:
            return None
        current = self.head
        min_node = current
        while current:
            if current.key < min_node.key:
                min_node = current
            current = current.sibling
        return min_node.key

    def remove_min(self):
        if not self.head:
            return None

        current = self.head
        prev = None
        min_node = current
        min_prev = None
        while current:
            if current.key < min_node.key:
                min_node = current
                min_prev = prev
            prev = current
            current = current.sibling

        if min_prev:
            min_prev.sibling = min_node.sibling
        else:
            self.head = min_node.sibling

        children = self._reverse(min_node.child)
        new_heap = BinomialHeap()
        new_heap.head = children
        self.merge(new_heap)
        return min_node.key

    def _reverse(self, node):
        prev = None
        while node:
            next_node = node.sibling
            node.sibling = prev
            prev = node
            node = next_node
        return prev



# Тестирование
def run_tests():
    sizes = [10**i for i in range(3, 8)]  # N = 10^i для i от 3 до 7
    results = []

    for size in sizes:
        print(f"Running tests for N={size}")

        # Генерация случайных данных
        data = [random.randint(1, 1000000) for _ in range(size)]

        # Тест для MinHeap
        min_heap = MinHeap()
        for val in data:
            min_heap.insert(val)

        # Замер времени для 1000 операций поиска минимума
        start_time = time.time()
        for _ in range(1000):
            min_heap.get_min()
        search_time = (time.time() - start_time) / 1000

        # Замер времени для 1000 операций удаления минимума
        start_time = time.time()
        for _ in range(1000):
            min_heap.remove_min()
        remove_time = (time.time() - start_time) / 1000

        # Замер времени для 1000 операций добавления нового элемента
        start_time = time.time()
        for _ in range(1000):
            min_heap.insert(random.randint(1, 1000000))
        insert_time = (time.time() - start_time) / 1000

        # Сохраняем результаты для MinHeap
        results.append({
            'size': size,
            'min_heap_insert': insert_time,
            'min_heap_remove': remove_time,
            'min_heap_search': search_time
        })
        print(f"MinHeap - Search Time: {search_time:.6f}s, Remove Time: {remove_time:.6f}s, Insert Time: {insert_time:.6f}s")

        # Тест для BinomialHeap
        binomial_heap = BinomialHeap()
        for val in data:
            binomial_heap.insert(val)

        # Замер времени для 1000 операций поиска минимума
        start_time = time.time()
        for _ in range(1000):
            binomial_heap.get_min()
        binomial_search_time = (time.time() - start_time) / 1000

        # Замер времени для 1000 операций удаления минимума
        start_time = time.time()
        for _ in range(1000):
            binomial_heap.remove_min()
        binomial_remove_time = (time.time() - start_time) / 1000

        # Замер времени для 1000 операций добавления нового элемента
        start_time = time.time()
        for _ in range(1000):
            binomial_heap.insert(random.randint(1, 1000000))
        binomial_insert_time = (time.time() - start_time) / 1000

        # Сохраняем результаты для BinomialHeap
        results[-1].update({
            'binomial_insert': binomial_insert_time,
            'binomial_remove': binomial_remove_time,
            'binomial_search': binomial_search_time
        })
        print(f"BinomialHeap - Search Time: {binomial_search_time:.6f}s, Remove Time: {binomial_remove_time:.6f}s, Insert Time: {binomial_insert_time:.6f}s")

    plot_graphs(results)


# Построение графиков
def plot_graphs(results):
    sizes = [result['size'] for result in results]
    min_heap_insert_times = [result['min_heap_insert'] for result in results]
    binomial_insert_times = [result['binomial_insert'] for result in results]
    min_heap_remove_times = [result['min_heap_remove'] for result in results]
    binomial_remove_times = [result['binomial_remove'] for result in results]
    min_heap_search_times = [result['min_heap_search'] for result in results]
    binomial_search_times = [result['binomial_search'] for result in results]

    # График времени вставки
    plt.plot(sizes, min_heap_insert_times, label='MinHeap Insert')
    plt.plot(sizes, binomial_insert_times, label='BinomialHeap Insert')
    plt.xlabel('N (Number of elements)')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.title('Insert Time vs N')
    plt.show()

    # График времени удаления
    plt.plot(sizes, min_heap_remove_times, label='MinHeap Remove')
    plt.plot(sizes, binomial_remove_times, label='BinomialHeap Remove')
    plt.xlabel('N (Number of elements)')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.title('Remove Time vs N')
    plt.show()

    # График времени поиска
    plt.plot(sizes, min_heap_search_times, label='MinHeap Search')
    plt.plot(sizes, binomial_search_times, label='BinomialHeap Search')
    plt.xlabel('N (Number of elements)')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.title('Search Time vs N')
    plt.show()


if __name__ == "__main__":
    run_tests()
