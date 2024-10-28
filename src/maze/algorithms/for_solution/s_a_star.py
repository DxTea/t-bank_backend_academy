import heapq

from src.maze.algorithms.for_solution.base_solver import BaseSolver


class AStar(BaseSolver):
    def __init__(self, maze):
        """
        Инициализирует объект алгоритма A* для решения лабиринта.

        :param maze: Объект лабиринта, который нужно решить.
        """
        super().__init__(maze)
        self.open_set = []
        self.g_score = {self.start: 0}
        self.f_score = {self.start: self._heuristic(self.start, self.finish)}
        self.came_from = {}
        self.visited = set()

        heapq.heappush(self.open_set, (self.f_score[self.start], self.start))

    def solve(self):
        """
        Решает лабиринт, используя алгоритм A*.

        :return: True, если путь найден, иначе False.
        """
        while self.open_set:
            _, current = heapq.heappop(self.open_set)

            if current == self.finish:
                self._mark_path(current)
                return True

            self.visited.add(current)

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if (0 <= neighbor[0] < self.width and 0 <= neighbor[1] <
                        self.height):
                    if neighbor in self.visited:
                        continue
                    if self.maze[neighbor[1]][neighbor[0]] in [' ', '🪙', '☠️']:
                        tentative_g_score = self.g_score[
                                                current] + self.get_cost(
                            neighbor[0], neighbor[1])

                        if (neighbor not in self.g_score or tentative_g_score
                                < self.g_score[neighbor]):
                            self.came_from[neighbor] = current
                            self.g_score[neighbor] = tentative_g_score
                            self.f_score[
                                neighbor] = (tentative_g_score +
                                             self._heuristic(
                                                 neighbor, self.finish))
                            if neighbor not in [i[1] for i in self.open_set]:
                                heapq.heappush(self.open_set, (
                                    self.f_score[neighbor], neighbor))

        return False

    def _heuristic(self, a, b):
        """
        Вычисляет эвристическую оценку расстояния от точки a до точки b.

        :param a: Координаты точки а.
        :param b: Координаты точки b.
        :return: Эвристическая оценка расстояния.
        """
        base_heuristic = abs(a[0] - b[0]) + abs(a[1] - b[1])
        surface = self.maze_obj.get_surface(a[0], a[1])
        if surface:
            if surface.symbol == '🪙':
                return base_heuristic - 5
                # Уменьшаем эвристику на 5 для монетки
            elif surface.symbol == '☠️':
                return base_heuristic + 10
                # Увеличиваем эвристику на 10 для ловушки
        return base_heuristic

    def _mark_path(self, current):
        """
        Отмечает найденный путь в лабиринте и вычисляет общий счет.

        :param current: Текущая клетка.
        """
        total_score = 0
        while current in self.came_from:
            surface = self.maze_obj.get_surface(current[0], current[1])
            if surface:
                if surface.symbol == '🪙':
                    print(f"Монетка собрана на координатах: {current}")
                    total_score -= 5  # Вычитаем 5 за монетку
                elif surface.symbol == '☠️':
                    total_score += 10  # Добавляем 10 за ловушку
            total_score += self.get_cost(current[0], current[1])
            self.maze[current[1]][current[0]] = '1'
            current = self.came_from[current]
        self.maze[self.start[1]][self.start[0]] = '1'
