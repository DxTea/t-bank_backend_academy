import random
from typing import Tuple

import keyboard


class InputHandler:
    @staticmethod
    def get_choice(prompt: str) -> str:
        """
        Получает выбор пользователя.

        :param prompt: Сообщение для запроса ввода.
        :return: Введенное пользователем значение.
        """
        return input(prompt)

    @staticmethod
    def wait_for_space() -> None:
        """
        Ждет нажатия клавиши пробела.
        """
        while True:
            if keyboard.is_pressed('space'):
                break

    @staticmethod
    def get_maze_size() -> Tuple[int, int]:
        """
        Получает размер лабиринта от пользователя.

        :return: Ширина и высота лабиринта.
        """
        width: int = int(input(
            "Введите внутреннюю ширину лабиринта (0 для случайного "
            "значения): "))
        height: int = int(input(
            "Введите внутреннюю высоту лабиринта (0 для случайного "
            "значения): "))
        if width == 0:
            width = random.randint(10, 20)
        if height == 0:
            height = random.randint(10, 20)
        return width, height
