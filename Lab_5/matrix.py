import random
import time
import matplotlib.pyplot as plt


# ---------- Класс графа ----------
class WeightedGraph:
    def __init__(self, vertices: int):
        """Инициализация графа."""
        self.vertices = vertices
        self.edges = []  # Список рёбер (u, v, вес)
        self.adj_matrix = [[0] * vertices for _ in range(vertices)]  # Матрица смежности

    def add_edge(self, u: int, v: int, weight: int):
        """Добавление ребра в граф."""
        self.edges.append((u, v, weight))
        self.edges.append((v, u, weight))  # Для неориентированного графа
        self.adj_matrix[u][v] = weight
        self.adj_matrix[v][u] = weight

    def generate_random_graph(self, min_edges_per_vertex: int, weight_range: tuple = (1, 20)):
        """Генерация случайного связного графа."""
        # Шаг 1: Создаем связный граф (на случай, если вершины не связаны)
        for u in range(self.vertices - 1):
            weight = random.randint(*weight_range)
            self.add_edge(u, u + 1, weight)

        # Шаг 2: Добавляем дополнительные рёбра случайным образом
        for u in range(self.vertices):
            num_edges = random.randint(min_edges_per_vertex, self.vertices - 1)
            connected = set(v for u_, v, _ in self.edges if u_ == u)  # Уже связные вершины

            while len(connected) < num_edges:
                v = random.randint(0, self.vertices - 1)
                if u != v and v not in connected:  # Исключаем петли и повторяющиеся рёбра
                    weight = random.randint(*weight_range)
                    self.add_edge(u, v, weight)
                    connected.add(v)

    def print_adjacency_matrix(self):
        """Вывод матрицы смежности для графа."""
        for row in self.adj_matrix:
            print(" ".join(f"{weight:2}" for weight in row))


# ---------- Алгоритм Краскала ----------
def kruskal(graph: WeightedGraph):
    """Алгоритм Краскала для построения минимального остовного дерева."""
    # Сортируем рёбра по весу
    edges = sorted(graph.edges, key=lambda edge: edge[2])
    parent = list(range(graph.vertices))
    rank = [0] * graph.vertices
    mst = []

    def find(u):
        """Функция для поиска сжатия пути."""
        if parent[u] != u:
            parent[u] = find(parent[u])
        return parent[u]

    def union(u, v):
        """Объединяет два дерева."""
        root_u = find(u)
        root_v = find(v)

        if root_u != root_v:
            if rank[root_u] > rank[root_v]:
                parent[root_v] = root_u
            elif rank[root_u] < rank[root_v]:
                parent[root_u] = root_v
            else:
                parent[root_v] = root_u
                rank[root_u] += 1

    # Проходим по всем рёбрам
    for u, v, weight in edges:
        if find(u) != find(v):
            mst.append((u, v, weight))
            union(u, v)

    return mst


# ---------- Тестирование и замеры ----------
def test_kruskal():
    vertex_sets = [10, 20, 50, 100]  # Количество вершин для графов
    min_edges = [3, 4, 10, 20]
    iterations = 5  # Количество тестов на один граф
    results = []

    for vertices, min_edges_per_vertex in zip(vertex_sets, min_edges):
        times = []

        for _ in range(iterations):
            # Генерация графа
            graph = WeightedGraph(vertices)
            graph.generate_random_graph(min_edges_per_vertex)

            # Печать графа (опционально включить для отладки)
            print(f"\nГраф с {vertices} вершинами:")
            graph.print_adjacency_matrix()

            # Замер времени на выполнение алгоритма Краскала
            start_time = time.time()
            mst = kruskal(graph)
            elapsed_time = time.time() - start_time
            times.append(elapsed_time)

            # Печать результата остовного дерева
            print(f"\nОстовное дерево (MST): {mst}")
            print(f"Время выполнения: {elapsed_time:.5f} сек")

        # Записываем среднее время
        average_time = sum(times) / len(times)
        results.append((vertices, average_time))

    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot([r[0] for r in results], [r[1] for r in results], label="Алгоритм Краскала", marker="o")
    plt.xlabel("Количество вершин (N)")
    plt.ylabel("Время выполнения (секунды)")
    plt.title("Время выполнения алгоритма Краскала")
    plt.legend()
    plt.grid()
    plt.show()


# ---------- Запуск тестов ----------
test_kruskal()
