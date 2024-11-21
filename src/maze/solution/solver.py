from src.maze.algorithms.for_solution.s_a_star import AStar
from src.maze.algorithms.for_solution.s_bfs import BFS
from src.maze.algorithms.for_solution.s_dfs import DFS
from src.maze.algorithms.for_solution.s_ford_bellman import FordBellman
from src.maze.maze import Maze


class Solver:
    def __init__(self, algorithm: str, maze: Maze) -> None:
        """
        Инициализирует объект решателя лабиринта с заданным алгоритмом и
        лабиринтом.

        :param algorithm: Алгоритм, который будет использоваться для
        решения лабиринта.
        :param maze: Объект лабиринта, который нужно решить.
        """
        self.algorithm: str = algorithm
        self.maze = maze

    def solve(self):
        """
        Решает лабиринт, используя указанный алгоритм.

        :return: Список координат, представляющих путь от начала до конца
        лабиринта.
        :raises ValueError: Если указанный алгоритм неизвестен.
        """
        if self.algorithm == "A*":
            solver = AStar(self.maze)
        elif self.algorithm == "BFS":
            solver = BFS(self.maze)
        elif self.algorithm == "DFS":
            solver = DFS(self.maze)
        elif self.algorithm == "Форд-Беллман":
            solver = FordBellman(self.maze)
        else:
            raise ValueError(f"Неизвестный алгоритм: {self.algorithm}")

        return solver.solve()
