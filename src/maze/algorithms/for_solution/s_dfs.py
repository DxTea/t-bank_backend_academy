from src.maze.algorithms.for_solution.base_solver import BaseSolver
from typing import Dict, Optional, Set, List, Tuple


class DFS(BaseSolver):
    def solve(self) -> bool:
        """
        Решает лабиринт, используя алгоритм поиска в глубину (DFS).

        :return: True, если путь найден, иначе False.
        """
        stack: List[Tuple[int, int]] = [self.start]
        visited: Set[Tuple[int, int]] = set()
        parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {
            self.start: None}
        self.g_score[self.start] = 0

        while stack:
            current: Tuple[int, int] = stack.pop()
            if self._process_current_node(current, parent, visited, stack):
                return True

        return False
