from abc import ABC, abstractmethod
from typing import List


class IMaze(ABC):
    @abstractmethod
    def get_width(self) -> int:
        """
        Возвращает ширину лабиринта.

        :return: Ширина лабиринта.
        """
        pass

    @abstractmethod
    def get_height(self) -> int:
        """
        Возвращает высоту лабиринта.

        :return: Высота лабиринта.
        """
        pass

    @abstractmethod
    def get_maze(self) -> List[List[str]]:
        """
        Возвращает объект лабиринта.

        :return: Объект лабиринта.
        """
        pass
