import os
import random

from src.view.renderer_interface import IRenderer
from src.maze.maze import Maze


class ConsoleRenderer(IRenderer):
    def render_maze(self, maze_obj: Maze):
        """
        Метод для отображения лабиринта в консоли.

        :param maze_obj: Объект лабиринта, который нужно отобразить.
        """
        maze = maze_obj.get_maze()
        width = maze_obj.get_width() + 2
        height = maze_obj.get_height() + 2
        start, start_symbol = self.get_start_position()
        finish, finish_symbol = self.get_finish_position(width, height)

        for y in range(height):
            for x in range(width):
                if (x, y) == start:
                    print(start_symbol, end='')
                elif (x, y) == finish:
                    print(finish_symbol, end='')
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
                        print('🔳', end='')  # Зеленый квадрат для пути
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
        start, start_symbol = self.get_start_position()
        finish, finish_symbol = self.get_finish_position(width, height)

        for y in range(height):
            for x in range(width):
                if (x, y) == start:
                    print(start_symbol, end='')
                elif (x, y) == finish:
                    print(finish_symbol, end='')
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

    def display_welcome_screen(self):
        """
        Метод для отображения приветственного экрана.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Welcome to the Maze Game!")
        print("=========================")
        print("Press SPACE to continue...")

    def display_build_maze_with_solution_menu(self, menu):
        """
        Метод для отображения меню построения лабиринта с решением.

        :param menu: Объект меню, который нужно отобразить.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Build Maze with Solution Settings")
        print("=================================")
        self.display_common_settings(menu, show_solution_algorithm=True)
        print("1. Build Maze with Solution")
        print("2. Change Generation Algorithm")
        print("3. Change Solution Algorithm")
        print("4. Change Maze Size")
        print("5. Toggle Surfaces")
        print("6. Complicate Generation Settings")
        print("7. Back to Main Menu")
        print("8. Exit")

    @staticmethod
    def display_complicate_generation_menu(menu):
        """
        Метод для отображения меню усложненной генерации.

        :param menu: Объект меню, который нужно отобразить.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Complicate Generation Settings")
        print("===============================")
        print(
            f"Complicate Generation: "
            f"{'Enabled' if menu.complicate_generation else 'Disabled'}")
        print("1. Toggle Complicate Generation")
        print("2. Select First Algorithm")
        print("3. Select Second Algorithm")
        print("4. Back to Previous Menu")
        print("5. Exit")

    @staticmethod
    def display_common_settings(menu, show_solution_algorithm=True):
        """
        Метод для отображения общих настроек.

        :param menu: Объект меню, который нужно отобразить.
        :param show_solution_algorithm: Флаг, указывающий, нужно ли
        отображать алгоритм решения.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Current Settings:")
        if menu.complicate_generation:
            if len(menu.selected_algorithms) < 2:
                print("Generation Algorithm: Random + Random")
            else:
                print(
                    f"Generation Algorithm: {menu.selected_algorithms[0]} + "
                    f"{menu.selected_algorithms[1]}")
        else:
            print(f"Generation Algorithm: {menu.generation_algorithm}")
        if show_solution_algorithm:
            print(f"Solution Algorithm: {menu.solution_algorithm}")
        print(f"Maze Size: {menu.maze_size}")
        print(
            f"Surfaces: {'Enabled' if menu.surfaces_enabled else 'Disabled'}")
        print(
            f"Complicate Generation: "
            f"{'Enabled' if menu.complicate_generation else 'Disabled'}")

    def display_game_settings_menu(self, menu):
        """
        Метод для отображения меню настроек игры.

        :param menu: Объект меню, который нужно отобразить.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Game Settings")
        print("=============")
        self.display_common_settings(menu, show_solution_algorithm=False)
        print("1. Start Game")
        print("2. Change Generation Algorithm")
        print("3. Change Maze Size")
        print("4. Toggle Surfaces")
        print("5. Complicate Generation Settings")
        print("6. Back to Main Menu")
        print("7. Exit")

    @staticmethod
    def display_algorithm_menu(algorithms, title):
        """
        Метод для отображения меню выбора алгоритма.

        :param algorithms: Список доступных алгоритмов.
        :param title: Заголовок меню.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{title} Menu")
        print("================")
        for index, algorithm in enumerate(algorithms):
            print(f"{index}. {algorithm}")
        choice = int(input("Enter the number of your choice: "))
        return choice

    @staticmethod
    def display_menu(options):
        """
        Метод для отображения основного меню.

        :param options: Список опций меню.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Main Menu")
        print("=========")
        for index, option in enumerate(options, start=1):
            print(f"{index}. {option}")
        choice = input("Enter the number of your choice: ")
        return int(choice)

    @staticmethod
    def display_surfaces_menu(menu):
        """
         Метод для отображения меню поверхностей.

         :param menu: Объект меню, который нужно отобразить.
         """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Surfaces Settings")
        print("=================")
        print(
            f"Surfaces: {'Enabled' if menu.surfaces_enabled else 'Disabled'}")
        print(f"Coins: {menu.num_coins}")
        print(f"Traps: {menu.num_traps}")
        print("1. Toggle Surfaces")
        print("2. Change Number of Coins")
        print("3. Change Number of Traps")
        print("4. Back to Game Settings")
        print("5. Exit")

    @staticmethod
    def change_num_coins():
        """
        Метод для изменения количества монет в лабиринте.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Change Number of Coins")
        print("======================")
        print("Coins are represented by the symbol '🪙'.")
        print("Each coin decreases the heuristic by 5.")
        num_coins = int(input("Enter the number of coins: "))
        return num_coins

    @staticmethod
    def change_num_traps():
        """
        Метод для изменения количества ловушек в лабиринте.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Change Number of Traps")
        print("======================")
        print("Traps are represented by the symbol '☠️'.")
        print("Each trap increases the heuristic by 10.")
        num_traps = int(input("Enter the number of traps: "))
        return num_traps

    @staticmethod
    def preview_maze_size(width, height):
        """
        Метод для предварительного просмотра размера лабиринта.

        :param width: Ширина лабиринта.
        :param height: Высота лабиринта.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Preview of Maze Size: {width}x{height}")
        for y in range(height + 2):
            for x in range(width + 2):
                if x == 0 or y == 0 or x == width + 1 or y == height + 1:
                    print('⬛', end='')
                else:
                    print('⬜', end='')
            print()
        print("Are you satisfied with the maze size?")
        print("1. Yes")
        print("2. No")
        print("3. Back to Game Settings")
        print("4. Exit")
        choice = input("Enter the number of your choice: ")
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
            f'Generation Algorithm: {first_algorithm}'
            f'{" + " + second_algorithm if second_algorithm else ""}')
        if solution_algorithm:
            print(f'Solution Algorithm: {solution_algorithm}')
        print(f'Maze Size: {width}x{height}')
        print(f'Surfaces: {"Enabled" if surfaces_enabled else "Disabled"}')
        print(f'Number of Coins: {num_coins}')
        print(f'Number of Traps: {num_traps}')

    @staticmethod
    def display_exit_message():
        """
        Метод для отображения сообщения о выходе из игры.
        """
        print("Exiting the game...")
        print("Thank you for playing!")

    @staticmethod
    def display_error_message():
        """
        Метод для отображения сообщения об ошибке. Invalid choice
        """
        print("Invalid choice. Please try again.")

    @staticmethod
    def render_maze_solved():
        """
        Метод для отображения сообщения об успешном решении лабиринта.
        """
        print("Maze solved successfully!")

    @staticmethod
    def render_no_solution():
        """
        Метод для отображения сообщения об отсутствии решения для лабиринта.
        """
        print("No solution found for the maze.")

    @staticmethod
    def render_options():
        """
        Метод для отображения опций после генерации лабиринта.
        """
        print("\nOptions:")
        print("1. Generate another maze with the same parameters")
        print("2. Back to menu")
        print("3. Exit")
