import time
import random
import matplotlib.pyplot as plt
import sys

# Устанавливаем лимит рекурсии, иначе получим супер вкуснятину в виде переполнения стека рекурсиями
# (я не мог это решить пару часов, поэтому ЭТО НАСТОЛЬКО ВАЖНО). В данном случае предельная глубина рекурсий 15000
sys.setrecursionlimit(15000)


# Класс узла для бинарного дерева
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


# Бинарное дерево поиска (BST)
class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        # Базовый случай: если узел пустой, создаём новый узел
        if node is None:
            return Node(key)

        # Проверка на дубликат: если ключ уже есть, ничего не делаем
        if key == node.key:
            return node  # Добавляем обработку дубликатов

        # Вставка элемента: идём влево или вправо в зависимости от значения
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        return node

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if not node or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return Node(key)

        # Проверка на дубликат: если ключ уже есть, ничего не делаем
        if key == node.key:
            return node  # Добавляем обработку дубликатов

        # Вставка элемента
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        # Обновление высоты текущего узла
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Балансировка дерева
        balance = self._get_balance(node)

        # Если дерево стало несбалансированным, выполняем повороты
        # Левый левый случай
        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)

        # Правый правый случай
        if balance < -1 and key > node.right.key:
            return self._left_rotate(node)

        # Левый правый случай
        if balance > 1 and key > node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Правый левый случай
        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def _left_rotate(self, z):
        if not z or not z.right:  # Проверка, что z и z.right не равны None
            return z  # Если z или z.right пусты, возвращаем сам узел (ничего не меняем)

        y = z.right
        T2 = y.left

        # Выполнение поворота
        y.left = z
        z.right = T2

        # Обновление высоты узлов
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _right_rotate(self, y):
        if not y or not y.left:  # Проверка, что y и y.left не равны None
            return y  # Если y или y.left пусты, возвращаем сам узел (ничего не меняем)

        x = y.left
        T2 = x.right

        # Выполнение поворота
        x.right = y
        y.left = T2

        # Обновление высоты узлов
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))

        return x

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if not node or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current


# Функция для тестирования
def run_tests():
    times_insert_bst = []
    times_insert_avl = []
    times_search_bst = []
    times_search_avl = []
    times_search_array = []
    times_delete_bst = []
    times_delete_avl = []

    for i in range(10):
        size = 2 ** (10 + i)

        random_array = [random.randint(0, size) for _ in range(size)]
        # sorted_array = list(range(size)) # No longer need sorted array

        # for array, name in [(random_array, "Random"), (sorted_array, "Sorted")]: # change here
        for array, name in [(random_array, "Random")]:
            bst = BST()
            avl = AVLTree()

            # Вставка элементов в деревья
            start_time = time.time()
            for num in array:
                bst.insert(num)
            times_insert_bst.append(time.time() - start_time)

            start_time = time.time()
            for num in array:
                avl.insert(num)
            times_insert_avl.append(time.time() - start_time)

            # Поиск 1000 случайных элементов
            search_times_bst = []
            search_times_avl = []
            for _ in range(1000):
                key = random.choice(array)
                start_time = time.time()
                bst.search(key)
                search_times_bst.append(time.time() - start_time)

                start_time = time.time()
                avl.search(key)
                search_times_avl.append(time.time() - start_time)
            times_search_bst.append(sum(search_times_bst) / 1000)
            times_search_avl.append(sum(search_times_avl) / 1000)

            # Поиск в обычном массиве
            search_times_array = []
            for _ in range(1000):
                key = random.choice(array)
                start_time = time.time()
                key in array
                search_times_array.append(time.time() - start_time)
            times_search_array.append(sum(search_times_array) / 1000)

            # Удаление элементов из деревьев
            start_time = time.time()
            for num in array:
                bst.delete(num)
            times_delete_bst.append(time.time() - start_time)

            start_time = time.time()
            for num in array:
                avl.delete(num)
            times_delete_avl.append(time.time() - start_time)

    # Построение графиков
    sizes = [2 ** (10 + i) for i in range(10)]

    plt.figure(figsize=(12, 8))
    plt.subplot(3, 1, 1)
    plt.plot(sizes, times_insert_bst, label='BST Insert')
    plt.plot(sizes, times_insert_avl, label='AVL Insert')
    plt.title('Insert Time')
    plt.xlabel('Number of elements')
    plt.ylabel('Time (seconds)')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(sizes, times_search_bst, label='BST Search')
    plt.plot(sizes, times_search_avl, label='AVL Search')
    plt.plot(sizes, times_search_array, label='Array Search')
    plt.title('Search Time')
    plt.xlabel('Number of elements')
    plt.ylabel('Time (seconds)')
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(sizes, times_delete_bst, label='BST Delete')
    plt.plot(sizes, times_delete_avl, label='AVL Delete')
    plt.title('Delete Time')
    plt.xlabel('Number of elements')
    plt.ylabel('Time (seconds)')
    plt.legend()

    plt.tight_layout()
    plt.show()


run_tests()