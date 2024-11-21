import random
from typing import List


class BaseMazeGenerator:
    def __init__(self, maze) -> None:
        """
        Инициализирует объект базового генератора лабиринта.

        :param maze: Объект лабиринта, который нужно сгенерировать.
        """
        self.maze_obj = maze
        self.width: int = maze.get_width()
        self.height: int = maze.get_height()
        self.maze: List[List[str]] = maze.get_maze()

    def _set_exit(self) -> None:
        """
        Устанавливает выход из лабиринта в правом нижнем углу.
        """
        if self.width % 2 == 0:
            x: int = random.choice([1, 2])
            y: int = 1
            if x == 1:
                y = 2
            self.maze[self.height - x][self.width - y] = ' '

        self.maze[self.height - 1][self.width - 1] = ' '

    def get_maze(self):
        """
        Возвращает объект лабиринта.

        :return: Объект лабиринта.
        """
        self.maze_obj.maze = self.maze
        return self.maze_obj
