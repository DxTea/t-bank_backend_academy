import os
import random

from src.view.renderer_interface import IRenderer
from src.maze.maze import Maze


class ConsoleRenderer(IRenderer):

    def __init__(self):
        self.start = None
        self.start_symbol = None
        self.finish = None
        self.finish_symbol = None

    def render_maze(self, maze_obj: Maze):
        """
        Метод для отображения лабиринта в консоли.

        :param maze_obj: Объект лабиринта, который нужно отобразить.
        """
        maze = maze_obj.get_maze()
        width = maze_obj.get_width() + 2
        height = maze_obj.get_height() + 2
        if self.start is None or self.finish is None:
            self.start, self.start_symbol = self.get_start_position()
            self.finish, self.finish_symbol = self.get_finish_position(width,
                                                                       height)

        for y in range(height):
            for x in range(width):
                if (x, y) == self.start:
                    print(self.start_symbol, end='')
                elif (x, y) == self.finish:
                    print(self.finish_symbol, end='')
                elif x == 0 or y == 0 or x == width - 1 or y == height - 1:
                    print('⬛', end='')
                else:
                    cell = maze[y - 1][x - 1]
                    surface = maze_obj.get_surface(x - 1, y - 1)
                    if surface:
                        print(surface.symbol, end='')
                    elif cell == '#':
                        print('⬛', end='')
                    elif cell == '1':
                        print('🔳', end='')
                    else:
                        print('⬜', end='')
            print()

    @staticmethod
    def get_start_position():
        start_positions = [(1, 0), (0, 1)]
        start = random.choice(start_positions)
        start_symbol = '⬇️' if start == (1, 0) else '➡️'
        return start, start_symbol

    @staticmethod
    def get_finish_position(width, height):
        finish_positions = [(width - 2, height - 1), (width - 1, height - 2)]
        finish = random.choice(finish_positions)
        finish_symbol = '⬇️' if finish == (width - 2, height - 1) else '➡️'
        return finish, finish_symbol

    def render_game(self, game):
        # os.system('cls' if os.name == 'nt' else 'clear')

        maze = game.maze
        player_pos = game.player.position
        exit_pos = game.exit
        width = len(maze[0]) + 2
        height = len(maze) + 2
        if self.start is None or self.finish is None:
            self.start, self.start_symbol = self.get_start_position()
            self.finish, self.finish_symbol = self.get_finish_position(width,
                                                                       height)

        for y in range(height):
            for x in range(width):
                if (x, y) == self.start:
                    print(self.start_symbol, end='')
                elif (x, y) == self.finish:
                    print(self.finish_symbol, end='')
                elif (x, y) == (
                        player_pos[0] + 1,
                        player_pos[1] + 1) and game.game_started:
                    print('🪼', end='')  # 🚹😶‍🌫️♿
                elif (x, y) == (exit_pos[0] + 1, exit_pos[1] + 1):
                    print('✅', end='')
                elif x == 0 or y == 0 or x == width - 1 or y == height - 1:
                    print('⬛', end='')
                else:
                    cell = maze[y - 1][x - 1]
                    surface = game.maze_obj.get_surface(x - 1, y - 1)
                    if surface:
                        print(surface.symbol, end='')
                    elif cell == '#':
                        print('⬛', end='')
                    elif cell == '1':
                        print('🔳', end='')  # Green square for the path
                    else:
                        print('⬜', end='')
            print()

    def reset_positions(self):
        """
        Сбрасывает стартовую и финишную позиции.
        """
        self.start = None
        self.start_symbol = None
        self.finish = None
        self.finish_symbol = None

    def display_welcome_screen(self):
        """
        Метод для отображения приветственного экрана.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Добро пожаловать в игру Лабиринт!")
        print("Версия игры: 1.1.0")
        print("Разработчик: Семён Давыдов aka DxTea")
        print("Инструкция: Поиграйте в прохождение лабиринта или выберите "
              "автоматическое решение одним из алгоритмов.")
        print("Лицензия: MIT")
        print("=========================")
        print("Нажмите ПРОБЕЛ, чтобы продолжить...")

    def display_build_maze_with_solution_menu(self, menu):
        """
        Метод для отображения меню построения лабиринта с решением.

        :param menu: Объект меню, который нужно отобразить.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Настройки построения лабиринта с решением")
        print("=================================")
        self.display_common_settings(menu, show_solution_algorithm=True)
        print("1. Построить лабиринт с решением")
        print("2. Изменить алгоритм генерации")
        print("3. Изменить алгоритм решения")
        print("4. Изменить размер лабиринта")
        print("5. Переключить поверхности")
        print("6. Настройки усложненной генерации")
        print("7. Назад в главное меню")
        print("8. Выйти")

    @staticmethod
    def display_complicate_generation_menu(menu):
        """
        Метод для отображения меню усложненной генерации.

        :param menu: Объект меню, который нужно отобразить.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Настройки усложненной генерации")
        print("===============================")
        print(
            f"Усложненная генерация: "
            f"{'Включена' if menu.complicate_generation else 'Выключена'}")
        print("1. Переключить усложненную генерацию")
        print("2. Выбрать первый алгоритм")
        print("3. Выбрать второй алгоритм")
        print("4. Назад в предыдущее меню")
        print("5. Выйти")

    @staticmethod
    def display_common_settings(menu, show_solution_algorithm=True):
        """
        Метод для отображения общих настроек.

        :param menu: Объект меню, который нужно отобразить.
        :param show_solution_algorithm: Флаг, указывающий, нужно ли
        отображать алгоритм решения.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Текущие настройки:")
        if menu.complicate_generation:
            if len(menu.selected_algorithms) < 2:
                print("Алгоритм генерации: Случайный + Случайный")
            else:
                print(
                    f"Алгоритм генерации: {menu.selected_algorithms[0]} + "
                    f"{menu.selected_algorithms[1]}")
        else:
            print(f"Алгоритм генерации: {menu.generation_algorithm}")
        if show_solution_algorithm:
            print(f"Алгоритм решения: {menu.solution_algorithm}")
        print(f"Размер лабиринта: {menu.maze_size}")
        print(
            f"Поверхности: {'Включены' if menu.surfaces_enabled else 'Выключены'}")
        print(
            f"Усложненная генерация: "
            f"{'Включена' if menu.complicate_generation else 'Выключена'}")

    def display_game_settings_menu(self, menu):
        """
        Метод для отображения меню настроек игры.

        :param menu: Объект меню, который нужно отобразить.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Настройки игры")
        print("=============")
        self.display_common_settings(menu, show_solution_algorithm=False)
        print("1. Начать игру")
        print("2. Изменить алгоритм генерации")
        print("3. Изменить размер лабиринта")
        print("4. Переключить поверхности")
        print("5. Настройки усложненной генерации")
        print("6. Назад в главное меню")
        print("7. Выйти")

    @staticmethod
    def display_algorithm_menu(algorithms, title):
        """
        Метод для отображения меню выбора алгоритма.

        :param algorithms: Список доступных алгоритмов.
        :param title: Заголовок меню.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{title} Меню")
        print("================")
        for index, algorithm in enumerate(algorithms):
            print(f"{index}. {algorithm}")
        choice = int(input("Введите номер вашего выбора:"))
        return choice

    @staticmethod
    def display_menu(options):
        """
        Метод для отображения основного меню.

        :param options: Список опций меню.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Главное меню")
        print("=========")
        for index, option in enumerate(options, start=1):
            print(f"{index}. {option}")
        choice = input("Введите номер вашего выбора: ")
        return int(choice)

    @staticmethod
    def display_surfaces_menu(menu):
        """
         Метод для отображения меню поверхностей.

         :param menu: Объект меню, который нужно отобразить.
         """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Настройки поверхностей")
        print("=================")
        print(
            f"Поверхности: {'Включены' if menu.surfaces_enabled else 'Выключены'}")
        print(f"Монеты: {menu.num_coins}")
        print(f"Ловушки: {menu.num_traps}")
        print("1. Переключить поверхности")
        print("2. Изменить количество монет")
        print("3. Изменить количество ловушек")
        print("4. Назад в настройки игры")
        print("5. Выйти")

    @staticmethod
    def change_num_coins():
        """
        Метод для изменения количества монет в лабиринте.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Изменить количество монет")
        print("======================")
        print("Монеты обозначаются символом '🪙'.")
        print("Каждая монета уменьшает эвристику на 5.")
        num_coins = int(input("Введите количество монет: "))
        return num_coins

    @staticmethod
    def change_num_traps():
        """
        Метод для изменения количества ловушек в лабиринте.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Изменить количество ловушек")
        print("======================")
        print("Ловушки обозначаются символом '☠️'.")
        print("Каждая ловушка увеличивает эвристику на 10.")
        num_traps = int(input("Введите количество ловушек: "))
        return num_traps

    @staticmethod
    def preview_maze_size(width, height):
        """
        Метод для предварительного просмотра размера лабиринта.

        :param width: Ширина лабиринта.
        :param height: Высота лабиринта.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Предварительный просмотр размера лабиринта: {width}x{height}")
        for y in range(height + 2):
            for x in range(width + 2):
                if x == 0 or y == 0 or x == width + 1 or y == height + 1:
                    print('⬛', end='')
                else:
                    print('⬜', end='')
            print()
        print("Вы удовлетворены размером лабиринта?")
        print("1. Да")
        print("2. Нет")
        print("3. Назад в настройки игры")
        print("4. Выйти")
        choice = input("Введите номер вашего выбора: ")
        return choice

    @staticmethod
    def display_maze_info(first_algorithm, second_algorithm, width,
                          height, surfaces_enabled, num_coins, num_traps,
                          solution_algorithm=None):
        """
                Метод для отображения информации о лабиринте.

                :param first_algorithm: Первый алгоритм генерации.
                :param second_algorithm: Второй алгоритм генерации (если есть).
                :param width: Ширина лабиринта.
                :param height: Высота лабиринта.
                :param surfaces_enabled: Включены ли поверхности.
                :param num_coins: Количество монет.
                :param num_traps: Количество ловушек.
                :param solution_algorithm: Алгоритм решения (если есть).
                """
        print(
            f'Алгоритм генерации: {first_algorithm}'
            f'{" + " + second_algorithm if second_algorithm else ""}')
        if solution_algorithm:
            print(f'Алгоритм решения: {solution_algorithm}')
        print(f'Размер лабиринта: {width}x{height}')
        print(
            f'Поверхности: {"Включены" if surfaces_enabled else "Выключены"}')
        print(f'Количество монет: {num_coins}')
        print(f'Количество ловушек: {num_traps}')

    @staticmethod
    def display_exit_message():
        """
        Метод для отображения сообщения о выходе из игры.
        """
        print("Выход из игры...")
        print("Спасибо за игру!")

    @staticmethod
    def display_error_message():
        """
        Метод для отображения сообщения об ошибке. Invalid choice
        """
        print("Неверный выбор. Пожалуйста, попробуйте снова.")

    @staticmethod
    def render_maze_solved():
        """
        Метод для отображения сообщения об успешном решении лабиринта.
        """
        print("Лабиринт успешно решен!")

    @staticmethod
    def render_no_solution():
        """
        Метод для отображения сообщения об отсутствии решения для лабиринта.
        """
        print("Решение для лабиринта не найдено.")

    @staticmethod
    def render_options():
        """
        Метод для отображения опций после генерации лабиринта.
        """
        print("\nОпции:")
        print("1. Сгенерировать другой лабиринт с теми же параметрами")
        print("2. Назад в меню")
        print("3. Выйти")
