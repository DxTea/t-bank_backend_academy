from typing import List


class SettingsManager:
    def __init__(self, menu) -> None:
        """
        Инициализирует объект SettingsManager.

        :param menu: Объект меню, связанный с настройками.
        """
        self.menu = menu
        self.generation_algorithm: str = "Cлучайно"
        self.solution_algorithm: str = "Cлучайно"
        self.maze_size: str = "Cлучайно"
        self.surfaces_enabled: bool = False
        self.num_coins: int = 0
        self.num_traps: int = 0
        self.complicate_generation: bool = False
        self.complicate_algorithms: List[str] = [
            "Cлучайно", "Краскал", "Прим",
            "Рекурсивное обратное отслеживание",
            "Двоичное дерево"]
        self.selected_algorithms: List[str] = []
        self.generation_algorithms: List[str] = [
            "Cлучайно", "Краскал", "Прим",
            "Рекурсивное обратное отслеживание",
            "Двоичное дерево"]
        self.solution_algorithms: List[str] = ["Cлучайно", "A*", "BFS", "DFS",
                                               "Форд-Беллман"]

    def select_first_algorithm(self) -> None:
        """
        Позволяет пользователю выбрать первый алгоритм из списка
        усложненных алгоритмов.
        """
        choice: int = self.menu.algorithm_menu(self.complicate_algorithms,
                                               "Первый алгоритм")
        if 0 <= choice < len(self.complicate_algorithms):
            self.selected_algorithms = [self.complicate_algorithms[choice]]
        print(f"Первый алгоритм выбран: {self.selected_algorithms[0]}")

    def select_second_algorithm(self) -> None:
        """
        Позволяет пользователю выбрать второй алгоритм из списка
        усложненных алгоритмов.
        """
        choice: int = self.menu.algorithm_menu(self.complicate_algorithms,
                                               "Второй алгоритм")
        if 0 <= choice < len(self.complicate_algorithms):
            if len(self.selected_algorithms) == 1:
                self.selected_algorithms.append(
                    self.complicate_algorithms[choice])
            else:
                self.selected_algorithms[1] = self.complicate_algorithms[
                    choice]
        print(f"Второй алгоритм выбран: {self.selected_algorithms[1]}")

    def change_solution_algorithm(self) -> None:
        """
        Позволяет пользователю изменить алгоритм решения лабиринта.
        """
        choice: int = self.menu.algorithm_menu(self.solution_algorithms,
                                               "Алгоритм решения")
        if 0 <= choice < len(self.solution_algorithms):
            self.solution_algorithm = self.solution_algorithms[choice]
        print(f"Алгоритм решения изменен на: {self.solution_algorithm}")

    def change_generation_algorithm(self) -> None:
        """
        Позволяет пользователю изменить алгоритм генерации лабиринта.
        """
        if self.complicate_generation:
            print("Чтобы выбрать алгоритм, сначала необходимо отключить "
                  "настройки усложненной генерации.")
            input("Нажмите Enter, чтобы продолжить...")
            return
        choice: int = self.menu.algorithm_menu(self.generation_algorithms,
                                               "Алгоритм генерации")
        if 0 <= choice < len(self.generation_algorithms):
            self.generation_algorithm = self.generation_algorithms[choice]
            self.menu.generation_algorithm = self.generation_algorithm
        print(f"Алгоритм генерации изменен на: {self.generation_algorithm}")

    def change_maze_size(self) -> None:
        """
        Позволяет пользователю изменить размер лабиринта.
        """
        while True:
            width: int
            height: int
            width, height = self.menu.input_handler.get_maze_size()
            choice: str = self.menu.renderer.preview_maze_size(width, height)
            if choice == '1':
                self.maze_size = f"{width}x{height}"
                self.menu.maze_size = self.maze_size
                break
            elif choice == '2':
                continue
            elif choice == '3':
                break
            elif choice == '4':
                self.menu.exit_game()
            else:
                self.menu.renderer.display_error_message()

    def toggle_surfaces(self) -> None:
        """
        Переключает состояние поверхностей в лабиринте.
        """
        self.surfaces_enabled = not self.surfaces_enabled
        self.menu.surfaces_enabled = self.surfaces_enabled
        print(f"Поверхности включены: {self.surfaces_enabled}")

    def change_num_coins(self) -> None:
        """
        Метод для изменения количества монет в лабиринте.
        """
        self.num_coins = self.menu.renderer.change_num_coins_menu()

    def change_num_traps(self) -> None:
        """
        Метод для изменения количества ловушек в лабиринте.
        """
        self.num_traps = self.menu.renderer.change_num_traps_menu()
