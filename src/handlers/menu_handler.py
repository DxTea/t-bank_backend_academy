import random

from src.handlers.input_handler import InputHandler
from src.maze.generation.generator import Generator
from src.game.game import Game
from src.maze.solution.solver import Solver
from src.view.renderer import ConsoleRenderer


class Menu:
    def __init__(self):
        """
        Инициализирует объект меню с настройками по умолчанию.
        """
        self.options = [
            "Play Game",
            "Build Maze with Solution",
            "Exit"
        ]
        self.renderer = ConsoleRenderer()
        self.input_handler = InputHandler()
        self.generation_algorithm = "Random"
        self.solution_algorithm = "Random"
        self.maze_size = "Random"
        self.surfaces_enabled = False
        self.num_coins = 0
        self.num_traps = 0
        self.complicate_generation = False
        self.complicate_algorithms = ["Random", "Kruskal", "Prim",
                                      "Recursive Backtracking", "Binary Tree"]
        self.selected_algorithms = []
        self.generation_algorithms = ["Random", "Kruskal", "Prim",
                                      "Recursive Backtracking", "Binary Tree"]
        self.solution_algorithms = ["Random", "A* Star", "BFS", "DFS",
                                    "Ford-Bellman"]

    def display_welcome_screen(self):
        """
        Отображает приветственный экран и ждет нажатия клавиши пробела.
        """
        self.renderer.display_welcome_screen()
        self.input_handler.wait_for_space()

    def display_build_maze_with_solution_menu(self):
        """
        Отображает меню построения лабиринта с решением и обрабатывает
        выбор пользователя.
        """
        while True:
            self.renderer.display_build_maze_with_solution_menu(self)
            choice = self.input_handler.get_choice(
                "Enter the number of your choice: ")
            if choice == '1':
                self.build_maze_with_solution()
            elif choice == '2':
                if self.complicate_generation:
                    print(
                        "To select an algorithm, you must first disable "
                        "Complicate Generation Settings.")
                    input("Press Enter to continue...")
                else:
                    self.change_generation_algorithm()
            elif choice == '3':
                self.change_solution_algorithm()
            elif choice == '4':
                self.change_maze_size()
            elif choice == '5':
                self.toggle_surfaces()
            elif choice == '6':
                self.display_complicate_generation_menu()
            elif choice == '7':
                break
            elif choice == '8':
                self.exit_game()
            else:
                self.renderer.display_error_message()

    def display_complicate_generation_menu(self):
        """
        Отображает меню усложненной генерации и обрабатывает выбор
        пользователя.
        """
        while True:
            self.renderer.display_complicate_generation_menu(self)
            choice = self.input_handler.get_choice(
                "Enter the number of your choice: ")
            if choice == '1':
                self.complicate_generation = not self.complicate_generation
            elif choice == '2':
                self.select_first_algorithm()
            elif choice == '3':
                self.select_second_algorithm()
            elif choice == '4':
                break
            elif choice == '5':
                self.exit_game()
            else:
                self.renderer.display_error_message()

    def select_first_algorithm(self):
        """
        Позволяет пользователю выбрать первый алгоритм для усложненной
        генерации.
        """
        choice = self.display_algorithm_menu(self.complicate_algorithms,
                                             "First Algorithm")
        if 0 <= choice < len(self.complicate_algorithms):
            self.selected_algorithms = [self.complicate_algorithms[choice]]
        print(f"First Algorithm selected: {self.selected_algorithms[0]}")

    def select_second_algorithm(self):
        """
        Позволяет пользователю выбрать второй алгоритм для усложненной
        генерации.
        """
        choice = self.display_algorithm_menu(self.complicate_algorithms,
                                             "Second Algorithm")
        if 0 <= choice < len(self.complicate_algorithms):
            if len(self.selected_algorithms) == 1:
                self.selected_algorithms.append(
                    self.complicate_algorithms[choice])
            else:
                self.selected_algorithms[1] = self.complicate_algorithms[
                    choice]
        print(f"Second Algorithm selected: {self.selected_algorithms[1]}")

    def change_solution_algorithm(self):
        """
        Позволяет пользователю изменить алгоритм решения лабиринта.
        """
        choice = self.display_algorithm_menu(self.solution_algorithms,
                                             "Solution Algorithm")
        if 0 <= choice < len(self.solution_algorithms):
            self.solution_algorithm = self.solution_algorithms[choice]
        print(f"Solution Algorithm changed to: {self.solution_algorithm}")

    def display_menu(self):
        """
        Отображает основное меню и возвращает выбор пользователя.
        """
        return self.renderer.display_menu(self.options)

    def handle_choice(self, choice):
        """
        Обрабатывает выбор пользователя в основном меню.

        :param choice: Выбор пользователя.
        """
        if choice == 1:
            self.display_game_settings_menu()
        elif choice == 2:
            self.display_build_maze_with_solution_menu()
        elif choice == 3:
            self.exit_game()
        else:
            self.renderer.display_error_message()

    def display_game_settings_menu(self):
        """
        Отображает меню настроек игры и обрабатывает выбор пользователя.
        """
        while True:
            self.renderer.display_game_settings_menu(self)
            choice = self.input_handler.get_choice(
                "Enter the number of your choice: ")
            if choice == '1':
                self.start_game()
            elif choice == '2':
                if self.complicate_generation:
                    print(
                        "To select an algorithm, you must first disable "
                        "Complicate Generation Settings.")
                    input("Press Enter to continue...")
                else:
                    self.change_generation_algorithm()
            elif choice == '3':
                self.change_maze_size()
            elif choice == '4':
                self.toggle_surfaces()
            elif choice == '5':
                self.display_complicate_generation_menu()
            elif choice == '6':
                break
            elif choice == '7':
                self.exit_game()
            else:
                self.renderer.display_error_message()

    def build_maze_with_solution(self):
        """
        Строит лабиринт с решением на основе текущих настроек.
        """
        while True:
            if self.maze_size == "Random":
                width = random.randint(5, 20)
                height = random.randint(5, 20)
            else:
                width, height = map(int, self.maze_size.split('x'))

            if self.complicate_generation:
                if len(self.selected_algorithms) < 2:
                    first_algorithm = random.choice(
                        self.complicate_algorithms[1:])
                    second_algorithm = random.choice(
                        self.complicate_algorithms[1:])
                else:
                    first_algorithm, second_algorithm = (
                        self.selected_algorithms)
            else:
                first_algorithm = self.generation_algorithm
                if first_algorithm == "Random":
                    first_algorithm = random.choice(
                        self.generation_algorithms[1:])
                second_algorithm = None

            generator = Generator(width, height)
            maze = generator.generate_maze(first_algorithm)

            if second_algorithm:
                maze = generator.generate_maze(second_algorithm)

            if self.surfaces_enabled:
                maze.place_random_surfaces(num_coins=self.num_coins,
                                           num_traps=self.num_traps)

            if self.solution_algorithm == "Random":
                chosen_solution_algorithm = random.choice(
                    self.solution_algorithms[1:])
            else:
                chosen_solution_algorithm = self.solution_algorithm

            solver = Solver(chosen_solution_algorithm, maze)

            if solver.solve():
                solved_maze = solver.maze
                self.renderer.render_maze(solved_maze)
                self.renderer.display_maze_info(first_algorithm,
                                                second_algorithm, width,
                                                height, self.surfaces_enabled,
                                                self.num_coins, self.num_traps,
                                                chosen_solution_algorithm)
                self.renderer.render_maze_solved()
            else:
                self.renderer.render_maze(maze)
                self.renderer.display_maze_info(first_algorithm,
                                                second_algorithm, width,
                                                height, self.surfaces_enabled,
                                                self.num_coins, self.num_traps)
                self.renderer.render_no_solution()

            self.renderer.render_options()
            choice = self.input_handler.get_choice(
                "Enter the number of your choice: ")
            if choice == '1':
                continue
            elif choice == '2':
                break
            elif choice == '3':
                self.exit_game()
            else:
                self.renderer.display_error_message()

    def start_game(self):
        """
        Запускает игру с текущими настройками лабиринта.
        """
        if self.maze_size == "Random":
            width = random.randint(5, 20)
            height = random.randint(5, 20)
        else:
            width, height = map(int, self.maze_size.split('x'))

        if self.complicate_generation:
            if len(self.selected_algorithms) < 2:
                first_algorithm = random.choice(self.complicate_algorithms[1:])
                second_algorithm = random.choice(
                    self.complicate_algorithms[1:])
            else:
                first_algorithm, second_algorithm = self.selected_algorithms
        else:
            first_algorithm = self.generation_algorithm
            if first_algorithm == "Random":
                first_algorithm = random.choice(self.generation_algorithms[1:])
            second_algorithm = None

        generator = Generator(width, height)
        maze = generator.generate_maze(first_algorithm)

        if second_algorithm:
            maze = generator.generate_maze(second_algorithm)

        if self.surfaces_enabled:
            maze.place_random_surfaces(num_coins=self.num_coins,
                                       num_traps=self.num_traps)

        game = Game(maze)
        game.play()

        self.renderer.display_maze_info(first_algorithm, second_algorithm,
                                        width, height, self.surfaces_enabled,
                                        self.num_coins, self.num_traps)

    def display_algorithm_menu(self, algorithms, title):
        """
        Отображает меню выбора алгоритма и возвращает выбор пользователя.

        :param algorithms: Список доступных алгоритмов.
        :param title: Заголовок меню.
        :return: Выбор пользователя.
        """
        return self.renderer.display_algorithm_menu(algorithms, title)

    def change_generation_algorithm(self):
        """
        Позволяет пользователю изменить алгоритм генерации лабиринта.
        """
        if self.complicate_generation:
            print(
                "To select an algorithm, you must first disable Complicate "
                "Generation Settings.")
            input("Press Enter to continue...")
            return
        choice = self.display_algorithm_menu(self.generation_algorithms,
                                             "Generation Algorithm")
        if 0 <= choice < len(self.generation_algorithms):
            self.generation_algorithm = self.generation_algorithms[choice]
        print(f"Generation Algorithm changed to: {self.generation_algorithm}")

    def change_maze_size(self):
        """
        Позволяет пользователю изменить размер лабиринта.
        """
        while True:
            width, height = self.input_handler.get_maze_size()
            choice = self.renderer.preview_maze_size(width, height)
            if choice == '1':
                self.maze_size = f"{width}x{height}"
                break
            elif choice == '2':
                continue
            elif choice == '3':
                break
            elif choice == '4':
                self.exit_game()
            else:
                self.renderer.display_error_message()

    def toggle_surfaces(self):
        """
        Переключает состояние поверхностей в лабиринте.
        """
        self.display_surfaces_menu()

    def display_surfaces_menu(self):
        """
        Отображает меню поверхностей и обрабатывает выбор пользователя.
        """
        while True:
            self.renderer.display_surfaces_menu(self)
            choice = self.input_handler.get_choice(
                "Enter the number of your choice: ")
            if choice == '1':
                self.surfaces_enabled = not self.surfaces_enabled
            elif choice == '2':
                self.num_coins = self.renderer.change_num_coins()
            elif choice == '3':
                self.num_traps = self.renderer.change_num_traps()
            elif choice == '4':
                break
            elif choice == '5':
                self.exit_game()
            else:
                self.renderer.display_error_message()

    def exit_game(self):
        """
        Завершает игру и отображает сообщение о выходе.
        """
        self.renderer.display_exit_message()
        exit(0)
