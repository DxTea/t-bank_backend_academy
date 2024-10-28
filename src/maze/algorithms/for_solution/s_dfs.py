from src.maze.algorithms.for_solution.base_solver import BaseSolver

class DFS(BaseSolver):
    def solve(self):
        """
        Решает лабиринт, используя алгоритм поиска в глубину (DFS).

        :return: True, если путь найден, иначе False.
        """
        stack = [self.start]
        visited = set()
        parent = {self.start: None}
        self.g_score[self.start] = 0

        while stack:
            current = stack.pop()
            if self._process_current_node(current, parent, visited, stack):
                return True

        return False