from collections import deque
from src.maze.algorithms.for_solution.base_solver import BaseSolver

class BFS(BaseSolver):
    def solve(self):
        """
        Решает лабиринт, используя алгоритм поиска в ширину (BFS).

        :return: True, если путь найден, иначе False.
        """
        queue = deque([self.start])
        visited = set()
        parent = {self.start: None}
        self.g_score[self.start] = 0

        while queue:
            current = queue.popleft()
            if self._process_current_node(current, parent, visited, queue):
                return True

        return False