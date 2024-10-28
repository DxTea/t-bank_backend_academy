import random
from src.maze.algorithms.for_generation.base_maze_generator import \
    BaseMazeGenerator


class Kruskal(BaseMazeGenerator):
    def __init__(self, maze):
        """
        Инициализирует объект алгоритма Краскала для генерации лабиринта.

        :param maze: Объект лабиринта, который нужно сгенерировать.
        """
        super().__init__(maze)
        self.edges = []
        self.parent = {}
        self.rank = {}
        self._initialize_maze()
        self._generate_maze_kruskal()
        self._set_exit()

    def _initialize_maze(self):
        """
        Инициализирует лабиринт, устанавливая начальные пустые клетки и
        добавляя возможные ребра.
        """
        for y in range(self.height):
            for x in range(self.width):
                if x % 2 == 0 and y % 2 == 0:
                    self.maze[y][x] = ' '
                    if x + 2 < self.width:
                        self.edges.append(((x, y), (x + 2, y)))
                    if y + 2 < self.height:
                        self.edges.append(((x, y), (x, y + 2)))

    def _find(self, node):
        """
        Находит корень множества для заданного узла с использованием сжатия
        пути.

        :param node: Узел, для которого нужно найти корень множества.
        :return: Корень множества для заданного узла.
        """
        if self.parent[node] != node:
            self.parent[node] = self._find(self.parent[node])
        return self.parent[node]

    def _union(self, node1, node2):
        """
        Объединяет два множества с использованием рангов.

        :param node1: Первый узел.
        :param node2: Второй узел.
        """
        root1 = self._find(node1)
        root2 = self._find(node2)
        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            else:
                self.parent[root1] = root2
                if self.rank[root1] == self.rank[root2]:
                    self.rank[root2] += 1

    def _generate_maze_kruskal(self):
        """
        Генерирует лабиринт с использованием алгоритма Краскала.
        """
        for y in range(self.height):
            for x in range(self.width):
                if x % 2 == 0 and y % 2 == 0:
                    self.parent[(x, y)] = (x, y)
                    self.rank[(x, y)] = 0

        random.shuffle(self.edges)

        for (x1, y1), (x2, y2) in self.edges:
            if (x1, y1) not in self.parent:
                self.parent[(x1, y1)] = (x1, y1)
                self.rank[(x1, y1)] = 0
            if (x2, y2) not in self.parent:
                self.parent[(x2, y2)] = (x2, y2)
                self.rank[(x2, y2)] = 0
            if self._find((x1, y1)) != self._find((x2, y2)):
                self._union((x1, y1), (x2, y2))
                self.maze[(y1 + y2) // 2][(x1 + x2) // 2] = ' '
