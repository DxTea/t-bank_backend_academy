from src.game.player import Player
from src.view.renderer import ConsoleRenderer



class Game:
    def __init__(self, maze):
        """
        Инициализирует объект игры с заданным лабиринтом.

        :param maze: Объект лабиринта.
        """
        self.maze_obj = maze  # Сохраняет объект лабиринта
        self.maze = maze.get_maze()
        self.player = Player(maze.start)
        self.exit = maze.finish
        self.renderer = ConsoleRenderer()
        self.game_started = False

    def play(self):
        """
        Запускает игровой цикл, в котором игрок перемещается по лабиринту
        до тех пор, пока не достигнет выхода.
        """
        self.game_started = True
        while self.player.position != self.exit:
            self.renderer.render_game(self)
            print("0 to exit")
            print("1 for settings")
            move = input("Enter move (w, s, a, d): ")
            result = self.player.move(move, self.maze, self.maze_obj)
            if result == 'settings':
                if self.display_game_settings_menu() == 'main_menu':
                    return
            elif self.player.position == self.exit:
                self.player.increase_score()
                self.renderer.render_game(self)
                print("Congratulations! You've reached the exit.")
                print(f"Your score: {self.player.score}")
                break

    @staticmethod
    def display_game_settings_menu():
        """
        Отображает меню настроек игры.
        """
        from src.handlers.menu_handler import Menu
        menu = Menu()
        return menu.display_game_settings_menu()
