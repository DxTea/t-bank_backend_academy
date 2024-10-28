from abc import ABC, abstractmethod


class IGenerator(ABC):
    @abstractmethod
    def generate_maze(self, algorithm):
        """
        Генерирует лабиринт, используя указанный алгоритм.

        :param algorithm: Алгоритм, который будет использоваться для генерации лабиринта.
        :return: Сгенерированный лабиринт.
        """
        pass
