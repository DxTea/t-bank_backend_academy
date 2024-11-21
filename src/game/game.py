from src.game.player import Player
from src.view.renderer import ConsoleRenderer
from typing import Optional, List, Tuple


class Game:
    def __init__(self, maze) -> None:
        """
        Инициализирует объект игры с заданным лабиринтом.

        :param maze: Объект лабиринта.
        """
        self.maze_obj = maze  # Сохраняет объект лабиринта
        self.maze: List[List[str]] = maze.get_maze()
        self.player: Player = Player(maze.start)
        self.exit: Tuple[int, int] = maze.finish
        self.renderer: ConsoleRenderer = ConsoleRenderer()
        self.game_started: bool = False

    def play(self) -> None:
        """
        Запускает игровой цикл, в котором игрок перемещается по лабиринту
        до тех пор, пока не достигнет выхода.
        """
        self.game_started = True
        while self.player.position != self.exit:
            self.renderer.render_game(self)
            print("0 для выхода")
            print("1 для настроек")
            move: str = input("Введите движение (w, s, a, d): ")
            result: Optional[str] = self.player.move(move, self.maze,
                                                     self.maze_obj)
            if result == 'settings':
                if self.display_game_settings_menu() == 'main_menu':
                    return
            elif self.player.position == self.exit:
                self.player.increase_score()
                self.renderer.render_game(self)
                print("Поздравляем! Вы достигли выхода.")
                print(f"Ваш счет: {self.player.score}")
                break

    @staticmethod
    def display_game_settings_menu() -> Optional[str]:
        """
        Отображает меню настроек игры.
        """
        from src.handlers.menu_handler import Menu
        menu: Menu = Menu()
        return menu.game_settings_menu()
