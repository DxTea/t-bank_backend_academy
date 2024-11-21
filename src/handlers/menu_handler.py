from src.handlers.input_handler import InputHandler
from src.maze.maze_manager import MazeManager
from src.maze.settings_manager import SettingsManager
from src.view.renderer import ConsoleRenderer
from typing import List


class Menu:
    def __init__(self) -> None:
        """
        Инициализирует объект меню с настройками по умолчанию.
        """
        self.options: List[str] = [
            "Сыграть в игру",
            "Сгенерировать лабиринт с решением",
            "Выход"
        ]
        self.renderer: ConsoleRenderer = ConsoleRenderer()
        self.input_handler: InputHandler = InputHandler()
        self.settings_manager: SettingsManager = SettingsManager(self)
        self.maze_manager: MazeManager = MazeManager(self)
        self.surfaces_enabled: bool = self.settings_manager.surfaces_enabled
        self.num_coins: int = self.settings_manager.num_coins
        self.num_traps: int = self.settings_manager.num_traps

    def _build_maze_with_solution_menu(self) -> None:
        while True:
            self.renderer.display_build_maze_with_solution_menu(self)
            choice: str = self.input_handler.get_choice(
                "Введите номер вашего выбора: ")
            match choice:
                case '1':
                    self.maze_manager.build_maze_with_solution()
                case '2':
                    if self.settings_manager.complicate_generation:
                        print(
                            "Чтобы выбрать алгоритм, сначала необходимо "
                            "отключить "
                            "настройки усложненной генерации.")
                        input("Нажмите Enter, чтобы продолжить...")
                    else:
                        self.settings_manager.change_generation_algorithm()
                case '3':
                    self.settings_manager.change_solution_algorithm()
                case '4':
                    self.settings_manager.change_maze_size()
                case '5':
                    self._surfaces_menu()
                case '6':
                    self._complicate_generation_menu()
                case '7':
                    break
                case '8':
                    self.exit_game()
                case _:
                    self.renderer.display_error_message()

    def _complicate_generation_menu(self) -> None:
        """
        Отображает меню усложненной генерации и обрабатывает выбор
        пользователя.
        """
        while True:
            self.renderer.display_complicate_generation_menu(self)
            choice: str = self.input_handler.get_choice(
                "Введите номер вашего выбора: ")
            match choice:
                case '1':
                    self.settings_manager.complicate_generation = not (
                        self.settings_manager.complicate_generation)
                case '2':
                    self.settings_manager.select_first_algorithm()
                case '3':
                    self.settings_manager.select_second_algorithm()
                case '4':
                    break
                case '5':
                    self.exit_game()
                case _:
                    self.renderer.display_error_message()

    def main_menu(self) -> int:
        """
        Отображает основное меню и возвращает выбор пользователя.
        """
        while True:
            choice: int = self.renderer.display_menu(self.options)
            if choice in [1, 2, 3]:
                return choice
            else:
                self.renderer.display_error_message()

    def handle_choice(self, choice: int) -> None:
        """
        Обрабатывает выбор пользователя в основном меню.

        :param choice: Выбор пользователя.
        """
        match choice:
            case 1:
                self.game_settings_menu()
            case 2:
                self._build_maze_with_solution_menu()
            case 3:
                self.exit_game()
            case _:
                self.renderer.display_error_message()

    def game_settings_menu(self) -> None:
        """
        Отображает меню настроек игры и обрабатывает выбор пользователя.
        """
        while True:
            self.renderer.display_game_settings_menu(self)
            choice: str = self.input_handler.get_choice(
                "Введите номер вашего выбора: ")
            match choice:
                case '1':
                    self.maze_manager.start_game()
                case '2':
                    if self.settings_manager.complicate_generation:
                        print(
                            "Чтобы выбрать алгоритм, сначала необходимо "
                            "отключить "
                            "настройки усложненной генерации.")
                        input("Нажмите Enter, чтобы продолжить...")
                    else:
                        self.settings_manager.change_generation_algorithm()
                case '3':
                    self.settings_manager.change_maze_size()
                case '4':
                    self._surfaces_menu()
                case '5':
                    self._complicate_generation_menu()
                case '6':
                    self.main_menu()
                    break
                case '7':
                    self.exit_game()
                case _:
                    self.renderer.display_error_message()

    def welcome_screen(self) -> None:
        """
        Отображает приветственный экран и ждет нажатия клавиши пробела.
        """
        self.renderer.display_welcome_screen()
        self.input_handler.wait_for_space()

    def algorithm_menu(self, algorithms: List[str], title: str) -> int:
        """
        Отображает меню выбора алгоритма и возвращает выбор пользователя.

        :param algorithms: Список доступных алгоритмов.
        :param title: Заголовок меню.
        :return: Выбор пользователя.
        """
        return self.renderer.display_algorithm_menu(algorithms, title)

    def _surfaces_menu(self) -> None:
        """
        Отображает меню поверхностей и обрабатывает выбор пользователя.
        """
        while True:
            self.renderer.display_surfaces_menu(self)
            choice: str = self.input_handler.get_choice(
                "Введите номер вашего выбора: ")
            match choice:
                case '1':
                    self.settings_manager.toggle_surfaces()
                case '2':
                    self.settings_manager.change_num_coins()
                case '3':
                    self.settings_manager.change_num_traps()
                case '4':
                    break
                case '5':
                    self.exit_game()
                case _:
                    self.renderer.display_error_message()

    def exit_game(self) -> None:
        """
        Завершает игру и отображает сообщение о выходе.
        """
        self.renderer.display_exit_message()
        exit(0)
