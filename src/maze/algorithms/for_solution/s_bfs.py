from collections import deque

from typing import Dict, Optional, Set, Tuple
from src.maze.algorithms.for_solution.base_solver import BaseSolver


class BFS(BaseSolver):
    def solve(self) -> bool:
        """
        Решает лабиринт, используя алгоритм поиска в ширину (BFS).

        :return: True, если путь найден, иначе False.
        """
        queue = deque([self.start])
        visited: Set[Tuple[int, int]] = set()
        parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {
            self.start: None}
        self.g_score[self.start] = 0

        while queue:
            current: Tuple[int, int] = queue.popleft()
            if self._process_current_node(current, parent, visited, queue):
                return True

        return False
