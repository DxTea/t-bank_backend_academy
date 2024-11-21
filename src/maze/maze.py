from src.maze.maze_interface import IMaze
from src.maze.surfaces import Surface, Trap, Coin
import random
from typing import List, Tuple, Dict, Optional


class Maze(IMaze):
    def __init__(self, width: int, height: int) -> None:
        """
        Инициализирует объект лабиринта с заданной шириной и высотой.

        :param width: Ширина лабиринта.
        :param height: Высота лабиринта.
        """
        self.width: int = width
        self.height: int = height
        self.maze = [['#'] * width for _ in range(height)]
        self.start: Tuple[int, int] = (0, 0)
        self.finish: Tuple[int, int] = (width - 1, height - 1)
        self.surfaces: Dict[Tuple[int, int], Surface] = {}

    def get_width(self) -> int:
        """
        Возвращает ширину лабиринта.

        :return: Ширина лабиринта.
        """
        return self.width

    def get_height(self) -> int:
        """
        Возвращает высоту лабиринта.

        :return: Высота лабиринта.
        """
        return self.height

    def get_maze(self) -> List[List[str]]:
        """
        Возвращает текущий лабиринт в виде двумерного списка.

        :return: Двумерный список, представляющий лабиринт.
        """
        return self.maze

    def set_surface(self, x: int, y: int, surface: Optional[Surface]) -> None:
        """
        Устанавливает поверхность в указанной ячейке лабиринта.

        :param x: Координата x ячейки.
        :param y: Координата y ячейки.
        :param surface: Объект поверхности, который нужно установить.
        """
        if surface is None:
            self.surfaces.pop((x, y), None)
            self.maze[y][x] = ' '
        else:
            self.surfaces[(x, y)] = surface
            self.maze[y][x] = surface.symbol

    def get_surface(self, x: int, y: int) -> Optional[Surface]:
        """
        Возвращает поверхность, установленную в указанной ячейке лабиринта.

        :param x: Координата x ячейки.
        :param y: Координата y ячейки.
        :return: Объект поверхности или None, если поверхность не установлена.
        """
        return self.surfaces.get((x, y), None)

    def place_random_surfaces(self, num_traps: int, num_coins: int) -> None:
        """
        Размещает случайные ловушки и монеты в лабиринте.

        :param num_traps: Количество ловушек для размещения.
        :param num_coins: Количество монет для размещения.
        """
        print("Размещаем поверхности в случайных местах...")
        empty_cells: List[Tuple[int, int]] = [(x, y) for y in
                                              range(self.height) for x in
                                              range(self.width) if
                                              self.maze[y][x] == ' ']
        random.shuffle(empty_cells)
        for _ in range(num_traps):
            if empty_cells:
                x, y = empty_cells.pop()
                self.set_surface(x, y, Trap())

        for _ in range(num_coins):
            if empty_cells:
                x, y = empty_cells.pop()
                self.set_surface(x, y, Coin())
