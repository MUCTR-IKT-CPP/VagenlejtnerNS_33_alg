import random
import numpy as np


def generate_maze(n, max_path_width, straight_galleries, concentration_squares):
    maze = np.ones((n, n), dtype=int)

    def carve_passages(x, y):
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < n - 1 and 1 <= ny < n - 1 and maze[nx, ny] == 1:
                maze[nx - dx // 2, ny - dy // 2] = 0
                maze[nx, ny] = 0
                carve_passages(nx, ny)

    start_x, start_y = 1, 1
    exit_x, exit_y = n - 2, n - 2

    maze[start_x, start_y] = 0
    carve_passages(start_x, start_y)

    maze[exit_x, exit_y] = 0

    return maze


def solve_maze(maze, start=(1, 1), end=None):
    n = len(maze)
    if end is None:
        end = (n - 2, n - 2)

    stack = [(start, [start])]
    visited = set()

    while stack:
        (x, y), path = stack.pop()
        if (x, y) == end:
            return path

        if (x, y) in visited:
            continue
        visited.add((x, y))

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and maze[nx, ny] == 0:
                stack.append(((nx, ny), path + [(nx, ny)]))

    return None


size = 21
maze = generate_maze(size, 2, True, True)
solution = solve_maze(maze)

for i in range(size):
    for j in range(size):
        if (i, j) == (1, 1):
            print("S", end=" ")
        elif (i, j) == (size - 2, size - 2):
            print("E", end=" ")
        elif (i, j) in solution:
            print(".", end=" ")
        else:
            print("#" if maze[i, j] == 1 else " ", end=" ")
    print()
