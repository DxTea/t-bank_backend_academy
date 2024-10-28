import random

import keyboard


class InputHandler:
    @staticmethod
    def get_choice(prompt):
        """
        Получает выбор пользователя.

        :param prompt: Сообщение для запроса ввода.
        :return: Введенное пользователем значение.
        """
        return input(prompt)

    @staticmethod
    def wait_for_space():
        """
        Ждет нажатия клавиши пробела.
        """
        while True:
            if keyboard.is_pressed('space'):
                break

    @staticmethod
    def get_maze_size():
        """
        Получает размер лабиринта от пользователя.

        :return: Ширина и высота лабиринта.
        """
        width = int(input("Enter maze inner width (0 for random): "))
        height = int(input("Enter maze inner height (0 for random): "))
        if width == 0:
            width = random.randint(10, 20)
        if height == 0:
            height = random.randint(10, 20)
        return width, height