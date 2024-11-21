from abc import abstractmethod
from typing import List, Protocol


class IMaze(Protocol):
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
