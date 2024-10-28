import random
from typing import Tuple, Optional

from src.game.game import Game
from src.maze.generation.generator import Generator
from src.maze.solution.solver import Solver


class MazeManager:
    def __init__(self, menu) -> None:
        """
        Инициализирует объект MazeManager.

        :param menu: Объект меню, связанный с менеджером лабиринта.
        """
        self.menu = menu

    def get_maze_size(self) -> Tuple[int, int]:
        """
        Возвращает размеры лабиринта на основе текущих настроек.

        :return: Кортеж, содержащий ширину и высоту лабиринта.
        """
        settings = self.menu.settings_manager
        if settings.maze_size == "Cлучайно":
            width = random.randint(5, 30)
            height = random.randint(5, 20)
        else:
            width, height = map(int, settings.maze_size.split('x'))
        return width, height

    def select_algorithms(self) -> Tuple[str, Optional[str]]:
        """
        Возвращает выбранные алгоритмы генерации на основе текущих настроек.

        :return: Кортеж, содержащий первый и второй алгоритмы генерации.
        """
        settings = self.menu.settings_manager
        if settings.complicate_generation:
            if len(settings.selected_algorithms) < 2:
                first_algorithm = random.choice(
                    settings.complicate_algorithms[1:])
                second_algorithm = random.choice(
                    settings.complicate_algorithms[1:])
            else:
                first_algorithm, second_algorithm = (
                    settings.selected_algorithms)
        else:
            first_algorithm = settings.generation_algorithm
            if first_algorithm == "Cлучайно":
                first_algorithm = random.choice(
                    settings.generation_algorithms[1:])
            second_algorithm = None
        return first_algorithm, second_algorithm

    @staticmethod
    def generate_maze(width: int, height: int, first_algorithm: str,
                      second_algorithm: Optional[str]):
        """
        Генерирует лабиринт с использованием указанных алгоритмов.

        :param width: Ширина лабиринта.
        :param height: Высота лабиринта.
        :param first_algorithm: Первый алгоритм генерации.
        :param second_algorithm: Второй алгоритм генерации (если есть).
        :return: Сгенерированный лабиринт.
        """
        generator = Generator(width, height)
        maze = generator.generate_maze(first_algorithm)
        print("generate maze")
        print(maze)
        if second_algorithm:
            maze = generator.generate_maze(second_algorithm)
        return maze

    def place_surfaces(self, maze) -> None:
        """
        Размещает поверхности в лабиринте на основе текущих настроек.

        :param maze: Лабиринт, в котором нужно разместить поверхности.
        """
        settings = self.menu.settings_manager
        if settings.surfaces_enabled:
            maze.place_random_surfaces(num_coins=settings.num_coins,
                                       num_traps=settings.num_traps)

    def build_maze_with_solution(self) -> None:
        """
        Строит лабиринт с решением на основе текущих настроек.
        """
        settings = self.menu.settings_manager
        while True:
            width, height = self.get_maze_size()
            first_algorithm, second_algorithm = self.select_algorithms()
            maze = self.generate_maze(width, height, first_algorithm,
                                      second_algorithm)
            self.place_surfaces(maze)

            if settings.solution_algorithm == "Cлучайно":
                chosen_solution_algorithm = random.choice(
                    settings.solution_algorithms[1:])
            else:
                chosen_solution_algorithm = settings.solution_algorithm
            solver = Solver(chosen_solution_algorithm, maze)

            if solver.solve():
                solved_maze = solver.maze
                self.menu.renderer.render_maze(solved_maze)
                self.menu.renderer.display_maze_info(first_algorithm,
                                                     second_algorithm, width,
                                                     height,
                                                     settings.surfaces_enabled,
                                                     settings.num_coins,
                                                     settings.num_traps,
                                                     chosen_solution_algorithm)
                self.menu.renderer.render_maze_solved()
            else:
                self.menu.renderer.render_maze(maze)
                self.menu.renderer.display_maze_info(first_algorithm,
                                                     second_algorithm, width,
                                                     height,
                                                     settings.surfaces_enabled,
                                                     settings.num_coins,
                                                     settings.num_traps)
                self.menu.renderer.render_no_solution()

            self.menu.renderer.render_options()
            self.menu.renderer.reset_positions()
            choice = self.menu.input_handler.get_choice(
                "Введите номер вашего выбора: ")
            if choice == '1':
                continue
            elif choice == '2':
                break
            elif choice == '3':
                self.menu.exit_game()
            else:
                self.menu.renderer.display_error_message()

    def start_game(self) -> None:
        """
        Запускает игру с текущими настройками лабиринта.
        """
        width, height = self.get_maze_size()
        first_algorithm, second_algorithm = self.select_algorithms()
        maze = self.generate_maze(width, height, first_algorithm,
                                  second_algorithm)
        self.place_surfaces(maze)
        print("starting game")
        print(maze)
        game = Game(maze)
        game.play()
        surfaces_enabled = self.menu.settings_manager.surfaces_enabled
        num_coins = self.menu.settings_manager.num_coins
        num_traps = self.menu.settings_manager.num_traps
        self.menu.renderer.display_maze_info(first_algorithm, second_algorithm,
                                             width, height, surfaces_enabled,
                                             num_coins, num_traps)
