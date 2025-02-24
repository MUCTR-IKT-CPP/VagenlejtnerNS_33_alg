import random
import time
import matplotlib.pyplot as plt
from collections import defaultdict, deque
from typing import List, Tuple, Dict, Optional


# ---------- Класс граф ----------
class Graph:
    def __init__(self, vertices: int, edges: List[Tuple[int, int]], directed: bool = False):
        self.vertices = vertices
        self.edges = edges
        self.directed = directed

        # Генерация списка смежности
        self.adj_list = defaultdict(list)
        for edge in edges:
            u, v = edge
            self.adj_list[u].append(v)
            if not directed:
                self.adj_list[v].append(u)

    def adjacency_matrix(self) -> List[List[int]]:
        """Возвращает матрицу смежности"""
        matrix = [[0] * self.vertices for _ in range(self.vertices)]
        for u, v in self.edges:
            matrix[u][v] = 1
            if not self.directed:
                matrix[v][u] = 1
        return matrix

    def incidence_matrix(self) -> List[List[int]]:
        """Возвращает матрицу инцидентности"""
        num_edges = len(self.edges)
        matrix = [[0] * num_edges for _ in range(self.vertices)]
        for i, (u, v) in enumerate(self.edges):
            matrix[u][i] = 1
            if not self.directed:
                matrix[v][i] = 1
            else:
                matrix[v][i] = -1
        return matrix

    def adjacency_list(self) -> Dict[int, List[int]]:
        """Возвращает список смежности"""
        return dict(self.adj_list)

    def edge_list(self) -> List[Tuple[int, int]]:
        """Возвращает список всех рёбер"""
        return self.edges


# ---------- Генератор графов ----------
class RandomGraphGenerator:
    def __init__(self,
                 min_vertices: int,
                 max_vertices: int,
                 min_edges: int,
                 max_edges: int,
                 max_edges_per_vertex: int,
                 directed: bool):
        self.min_vertices = min_vertices
        self.max_vertices = max_vertices
        self.min_edges = min_edges
        self.max_edges = max_edges
        self.max_edges_per_vertex = max_edges_per_vertex
        self.directed = directed

    def generate(self) -> Graph:
        """Генерация случайного графа"""
        vertices = random.randint(self.min_vertices, self.max_vertices)
        max_possible_edges = (vertices * (vertices - 1)) if self.directed else (vertices * (vertices - 1)) // 2
        num_edges = random.randint(self.min_edges, min(max_possible_edges, self.max_edges))

        edges = set()
        while len(edges) < num_edges:
            u = random.randint(0, vertices - 1)
            v = random.randint(0, vertices - 1)
            if u == v:
                continue  # исключение петель
            if (u, v) not in edges and (not self.directed and (v, u) not in edges):
                edges.add((u, v))

        return Graph(vertices, list(edges), directed=self.directed)


# ---------- Поиск кратчайшего пути ----------

def bfs_shortest_path(graph: Graph, start: int, end: int) -> Optional[List[int]]:
    """Поиск кратчайшего пути с использованием BFS"""
    queue = deque([[start]])
    visited = set()

    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == end:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph.adjacency_list().get(node, []):
                if neighbor not in visited:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
    return None


def dfs_shortest_path(graph: Graph, start: int, end: int) -> Optional[List[int]]:
    """Поиск пути с использованием DFS"""
    stack = [[start]]
    visited = set()

    while stack:
        path = stack.pop()
        node = path[-1]
        if node == end:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph.adjacency_list().get(node, []):
                if neighbor not in visited:
                    new_path = list(path)
                    new_path.append(neighbor)
                    stack.append(new_path)
    return None


# ---------- Тесты производительности ----------

def test_performance():
    generator = RandomGraphGenerator(
        min_vertices=10,
        max_vertices=50,
        min_edges=20,
        max_edges=100,
        max_edges_per_vertex=10,
        directed=False
    )

    vertices_range = range(10, 105, 10)
    bfs_times = []
    dfs_times = []

    for num_vertices in vertices_range:
        graph = generator.generate()
        start, end = random.randint(0, num_vertices - 1), random.randint(0, num_vertices - 1)
        while start == end:  # Исключаем одинаковые вершины
            end = random.randint(0, num_vertices - 1)

        # Замер времени для BFS
        start_time = time.time()
        bfs_shortest_path(graph, start, end)
        bfs_time = time.time() - start_time
        bfs_times.append(bfs_time)

        # Замер времени для DFS
        start_time = time.time()
        dfs_shortest_path(graph, start, end)
        dfs_time = time.time() - start_time
        dfs_times.append(dfs_time)

    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(vertices_range, bfs_times, label="BFS", marker="o")
    plt.plot(vertices_range, dfs_times, label="DFS", marker="o")
    plt.xlabel("Количество вершин")
    plt.ylabel("Время выполнения (секунды)")
    plt.title("Производительность BFS и DFS на случайных графах")
    plt.legend()
    plt.grid()
    plt.show()


# Запуск тестов
test_performance()
