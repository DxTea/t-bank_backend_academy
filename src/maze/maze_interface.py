from abc import ABC, abstractmethod


class IMaze(ABC):
    @abstractmethod
    def get_width(self):
        """
        Возвращает ширину лабиринта.

        :return: Ширина лабиринта.
        """
        pass

    @abstractmethod
    def get_height(self):
        """
        Возвращает высоту лабиринта.

        :return: Высота лабиринта.
        """
        pass

    @abstractmethod
    def get_maze(self):
        """
        Возвращает объект лабиринта.

        :return: Объект лабиринта.
        """
        pass
