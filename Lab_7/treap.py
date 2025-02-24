import random
import time
import matplotlib.pyplot as plt
import numpy as np

class TreapNode:
    def __init__(self, key):
        self.key = key
        self.priority = random.randint(1, 1000000)  # Случайный приоритет
        self.left = None
        self.right = None

class Treap:
    def __init__(self):
        self.root = None

    def _rotate_right(self, node):
        left = node.left
        node.left = left.right
        left.right = node
        return left

    def _rotate_left(self, node):
        right = node.right
        node.right = right.left
        right.left = node
        return right

    def _insert(self, node, key):
        if node is None:
            return TreapNode(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
            if node.left.priority > node.priority:
                node = self._rotate_right(node)
        else:
            node.right = self._insert(node.right, key)
            if node.right.priority > node.priority:
                node = self._rotate_left(node)

        return node

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:  # Key found
            if node.left is None or node.right is None:
                node = node.left if node.left else node.right
            elif node.left.priority > node.right.priority:
                node = self._rotate_right(node)
                node.right = self._delete(node.right, key)
            else:
                node = self._rotate_left(node)
                node.left = self._delete(node.left, key)

        return node

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _search(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def search(self, key):
        return self._search(self.root, key)

    def max_depth(self, node):
        if node is None:
            return 0
        return 1 + max(self.max_depth(node.left), self.max_depth(node.right))

    def get_max_depth(self):
        return self.max_depth(self.root)


class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _update_height(self, node):
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

    def _rotate_left(self, z):
        y = z.right
        z.right = y.left
        y.left = z
        self._update_height(z)
        self._update_height(y)
        return y

    def _rotate_right(self, z):
        y = z.left
        z.left = y.right
        y.right = z
        self._update_height(z)
        self._update_height(y)
        return y

    def _balance(self, node):
        if not node:
            return node

        balance = self._get_height(node.left) - self._get_height(node.right)

        if balance > 1:
            if self._get_height(node.left.left) >= self._get_height(node.left.right):
                return self._rotate_right(node)
            else:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)

        if balance < -1:
            if self._get_height(node.right.right) >= self._get_height(node.right.left):
                return self._rotate_left(node)
            else:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

        return node

    def _insert(self, node, key):
        if not node:
            return AVLNode(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        self._update_height(node)
        return self._balance(node)

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:  # Key found
            if not node.left or not node.right:
                node = node.left if node.left else node.right
            else:
                temp = self._get_min(node.right)
                node.key = temp.key
                node.right = self._delete(node.right, temp.key)

        if node:
            self._update_height(node)
            return self._balance(node)
        return node

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _get_min(self, node):
        while node.left:
            node = node.left
        return node

    def _search(self, node, key):
        if not node or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def search(self, key):
        return self._search(self.root, key)

    def get_max_depth(self):
        return self.max_depth(self.root)

    def max_depth(self, node):
        if node is None:
            return 0
        return 1 + max(self.max_depth(node.left), self.max_depth(node.right))



def run_tests():
    N_values = [2**i for i in range(10, 19)]
    treap_insert_times = []
    treap_delete_times = []
    treap_search_times = []
    avl_insert_times = []
    avl_delete_times = []
    avl_search_times = []
    treap_max_depths = []
    avl_max_depths = []

    for N in N_values:
        treap = Treap()
        avl = AVLTree()

        # Генерация случайных значений
        values = [random.randint(1, 1000000) for _ in range(N)]

        # Заполнение деревьев
        for value in values:
            treap.insert(value)
            avl.insert(value)

        # Измерение максимальной глубины
        treap_max_depths.append(treap.get_max_depth())
        avl_max_depths.append(avl.get_max_depth())

        # Вставка
        start_time = time.time()
        for value in values:
            treap.insert(value)
        treap_insert_times.append((time.time() - start_time) / N)

        start_time = time.time()
        for value in values:
            avl.insert(value)
        avl_insert_times.append((time.time() - start_time) / N)

        # Удаление
        start_time = time.time()
        for value in values:
            treap.delete(value)
        treap_delete_times.append((time.time() - start_time) / N)

        start_time = time.time()
        for value in values:
            avl.delete(value)
        avl_delete_times.append((time.time() - start_time) / N)

        # Поиск
        start_time = time.time()
        for value in values:
            treap.search(value)
        treap_search_times.append((time.time() - start_time) / N)

        start_time = time.time()
        for value in values:
            avl.search(value)
        avl_search_times.append((time.time() - start_time) / N)

    # Графики
    plt.figure(figsize=(10, 6))
    plt.plot(N_values, treap_insert_times, label='Treap Insert', marker='o')
    plt.plot(N_values, avl_insert_times, label='AVL Insert', marker='x')
    plt.xlabel('Number of Elements (N)')
    plt.ylabel('Average Time (seconds)')
    plt.title('Average Insertion Time')
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(N_values, treap_delete_times, label='Treap Delete', marker='o')
    plt.plot(N_values, avl_delete_times, label='AVL Delete', marker='x')
    plt.xlabel('Number of Elements (N)')
    plt.ylabel('Average Time (seconds)')
    plt.title('Average Deletion Time')
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(N_values, treap_search_times, label='Treap Search', marker='o')
    plt.plot(N_values, avl_search_times, label='AVL Search', marker='x')
    plt.xlabel('Number of Elements (N)')
    plt.ylabel('Average Time (seconds)')
    plt.title('Average Search Time')
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(N_values, treap_max_depths, label='Treap Max Depth', marker='o')
    plt.plot(N_values, avl_max_depths, label='AVL Max Depth', marker='x')
    plt.xlabel('Number of Elements (N)')
    plt.ylabel('Max Depth')
    plt.title('Max Depth Comparison')
    plt.legend()
    plt.show()

run_tests()
