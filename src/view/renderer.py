import os
import random
from typing import Tuple, List, Optional

from src.view.renderer_interface import IRenderer
from src.maze.maze import Maze


class ConsoleRenderer(IRenderer):

    def __init__(self):
        """
        Инициализирует объект ConsoleRenderer.
        """
        self.start: Optional[Tuple[int, int]] = None
        self.start_symbol: Optional[str] = None
        self.finish: Optional[Tuple[int, int]] = None
        self.finish_symbol: Optional[str] = None

    def render_maze(self, maze_obj: Maze) -> None:
        """
        Отображает лабиринт в консоли.

        :param maze_obj: Объект лабиринта, который нужно отобразить.
        """
        maze: List[List[str]] = maze_obj.get_maze()
        width: int = maze_obj.get_width() + 2
        height: int = maze_obj.get_height() + 2
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
                    cell: str = maze[y - 1][x - 1]
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
    def get_start_position() -> Tuple[Tuple[int, int], str]:
        """
        Возвращает стартовую позицию и символ для отображения.

        :return: Кортеж, содержащий стартовую позицию и символ.
        """
        start_positions: List[Tuple[int, int]] = [(1, 0), (0, 1)]
        start: Tuple[int, int] = random.choice(start_positions)
        start_symbol: str = '⬇️' if start == (1, 0) else '➡️'
        return start, start_symbol

    @staticmethod
    def get_finish_position(width: int, height: int) -> (
            Tuple)[Tuple[int, int], str]:
        """
        Возвращает финишную позицию и символ для отображения.

        :param width: Ширина лабиринта.
        :param height: Высота лабиринта.
        :return: Кортеж, содержащий финишную позицию и символ.
        """
        finish_positions: List[Tuple[int, int]] = [(width - 2, height - 1),
                                                   (width - 1, height - 2)]
        finish: Tuple[int, int] = random.choice(finish_positions)
        finish_symbol: str = '⬇️' if finish == (
            width - 2, height - 1) else '➡️'
        return finish, finish_symbol

    def render_game(self, game) -> None:
        """
        Отображает игру в консоли.

        :param game: Объект игры, который нужно отобразить.
        """
        maze: List[List[str]] = game.maze
        player_pos: Tuple[int, int] = game.player.position
        exit_pos: Tuple[int, int] = game.exit
        width: int = len(maze[0]) + 2
        height: int = len(maze) + 2
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
                    cell: str = maze[y - 1][x - 1]
                    surface = game.maze_obj.get_surface(x - 1, y - 1)
                    if surface:
                        print(surface.symbol, end='')
                    elif cell == '#':
                        print('⬛', end='')
                    elif cell == '1':
                        print('🔳', end='')
                    else:
                        print('⬜', end='')
            print()

    def reset_positions(self) -> None:
        """
        Сбрасывает стартовую и финишную позиции.
        """
        self.start = None
        self.start_symbol = None
        self.finish = None
        self.finish_symbol = None

    def display_welcome_screen(self) -> None:
        """
        Отображает приветственный экран.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Добро пожаловать в игру Лабиринт!")
        print("Версия игры: 1.2.0")
        print("Разработчик: Семён Давыдов aka DxTea")
        print(
            "Инструкция: Поиграйте в прохождение лабиринта или выберите "
            "автоматическое решение одним из алгоритмов.")
        print("Лицензия: MIT")
        print("=========================")
        print("Нажмите ПРОБЕЛ, чтобы продолжить...")

    def display_build_maze_with_solution_menu(self, menu) -> None:
        """
        Отображает меню построения лабиринта с решением.

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
    def display_complicate_generation_menu(menu) -> None:
        """
        Отображает меню усложненной генерации.

        :param menu: Объект меню, который нужно отобразить.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        complicate_generation = menu.settings_manager.complicate_generation
        print("Настройки усложненной генерации")
        print("===============================")
        print(
            f"Усложненная генерация: "
            f"{'Включена' if complicate_generation else 'Выключена'}")
        print("1. Переключить усложненную генерацию")
        print("2. Выбрать первый алгоритм")
        print("3. Выбрать второй алгоритм")
        print("4. Назад в предыдущее меню")
        print("5. Выйти")

    @staticmethod
    def display_common_settings(menu,
                                show_solution_algorithm: bool = True) -> None:
        """
        Отображает общие настройки.

        :param menu: Объект меню, который нужно отобразить.
        :param show_solution_algorithm: Флаг, указывающий, нужно ли
        отображать алгоритм решения.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        settings = menu.settings_manager
        print("Текущие настройки:")
        if settings.complicate_generation:
            if len(settings.selected_algorithms) < 2:
                print("Алгоритм генерации: Случайный + Случайный")
            else:
                print(
                    f"Алгоритм генерации: {settings.selected_algorithms[0]} "
                    f"+ {settings.selected_algorithms[1]}")
        else:
            print(f"Алгоритм генерации: {settings.generation_algorithm}")
        if show_solution_algorithm:
            print(f"Алгоритм решения: {settings.solution_algorithm}")
        print(f"Размер лабиринта: {settings.maze_size}")
        print(
            f"Поверхности: "
            f"{'Включены' if settings.surfaces_enabled else 'Выключены'}")
        print(
            f"Усложненная генерация: "
            f"{'Включена' if settings.complicate_generation else 'Выключена'}")

    def display_game_settings_menu(self, menu) -> None:
        """
        Отображает меню настроек игры.

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
    def display_algorithm_menu(algorithms: List[str], title: str) -> int:
        """
        Отображает меню выбора алгоритма.

        :param algorithms: Список доступных алгоритмов.
        :param title: Заголовок меню.
        :return: Выбранный номер алгоритма.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{title} Меню")
        print("================")
        for index, algorithm in enumerate(algorithms):
            print(f"{index}. {algorithm}")
        choice: int = int(input("Введите номер вашего выбора:"))
        return choice

    @staticmethod
    def display_menu(options: List[str]) -> int:
        """
        Отображает основное меню.

        :param options: Список опций меню.
        :return: Выбранный номер опции.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Главное меню")
        print("=========")
        for index, option in enumerate(options, start=1):
            print(f"{index}. {option}")
        choice: int = int(input("Введите номер вашего выбора: "))
        return choice

    @staticmethod
    def display_surfaces_menu(menu) -> None:
        """
        Отображает меню поверхностей.

        :param menu: Объект меню, который нужно отобразить.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Настройки поверхностей")
        print("=================")
        print(
            f"Поверхности: "
            f"{'Включены' if menu.surfaces_enabled else 'Выключены'}")
        print(f"Монеты: {menu.num_coins}")
        print(f"Ловушки: {menu.num_traps}")
        print("1. Переключить поверхности")
        print("2. Изменить количество монет")
        print("3. Изменить количество ловушек")
        print("4. Назад в настройки игры")
        print("5. Выйти")

    @staticmethod
    def change_num_coins_menu() -> int:
        """
        Изменяет количество монет в лабиринте.

        :return: Новое количество монет.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Изменить количество монет")
        print("======================")
        print("Монеты обозначаются символом '🪙'.")
        print("Каждая монета уменьшает эвристику на 5.")
        num_coins: int = int(input("Введите количество монет: "))
        return num_coins

    @staticmethod
    def change_num_traps_menu() -> int:
        """
        Изменяет количество ловушек в лабиринте.

        :return: Новое количество ловушек.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Изменить количество ловушек")
        print("======================")
        print("Ловушки обозначаются символом '☠️'.")
        print("Каждая ловушка увеличивает эвристику на 10.")
        num_traps: int = int(input("Введите количество ловушек: "))
        return num_traps

    @staticmethod
    def preview_maze_size(width: int, height: int) -> str:
        """
        Отображает предварительный просмотр размера лабиринта.

        :param width: Ширина лабиринта.
        :param height: Высота лабиринта.
        :return: Выбранный номер опции.
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
        choice: str = input("Введите номер вашего выбора: ")
        return choice

    @staticmethod
    def display_maze_info(first_algorithm: str,
                          second_algorithm: Optional[str], width: int,
                          height: int,
                          surfaces_enabled: bool, num_coins: int,
                          num_traps: int,
                          solution_algorithm: Optional[str] = None) -> None:
        """
        Отображает информацию о лабиринте.

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
    def display_exit_message() -> None:
        """
        Отображает сообщение о выходе из игры.
        """
        print("Выход из игры...")
        print("Спасибо за игру!")

    @staticmethod
    def display_error_message() -> None:
        """
        Отображает сообщение об ошибке.
        """
        print("Неверный выбор. Пожалуйста, попробуйте снова.")

    @staticmethod
    def render_maze_solved() -> None:
        """
        Отображает сообщение об успешном решении лабиринта.
        """
        print("Лабиринт успешно решен!")

    @staticmethod
    def render_no_solution() -> None:
        """
        Отображает сообщение об отсутствии решения для лабиринта.
        """
        print("Решение для лабиринта не найдено.")

    @staticmethod
    def render_options() -> None:
        """
        Отображает опции после генерации лабиринта.
        """
        print("\nОпции:")
        print("1. Сгенерировать другой лабиринт с теми же параметрами")
        print("2. Назад в меню")
        print("3. Выйти")
