class Player:
    def __init__(self, start_position):
        """
        Инициализирует объект игрока с начальной позицией.

        :param start_position: Начальная позиция игрока в лабиринте.
        """
        self.position = start_position
        self.score = 0

    def move(self, direction, maze, maze_obj):
        """
        Перемещает игрока в указанном направлении, если это возможно.

        :param direction: Направление движения ('w', 's', 'a', 'd' или '0' для выхода).
        :param maze: Текущий лабиринт в виде двумерного списка.
        :param maze_obj: Объект лабиринта для обновления поверхностей.
        :return: None или 'settings' для перехода в меню настроек.
        """
        if direction == '0':
            print("Exiting the game...")
            exit(0)
        elif direction == '1':
            return 'settings'
        elif direction == '2':
            return 'main_menu'

        x, y = self.position
        if direction == 'w' and y > 0 and maze[y - 1][x] in [' ', '🪙', '☠️']:
            self.position = (x, y - 1)
        elif direction == 's' and y < len(maze) - 1 and maze[y + 1][x] in [' ',
                                                                           '🪙',
                                                                           '☠️']:
            self.position = (x, y + 1)
        elif direction == 'a' and x > 0 and maze[y][x - 1] in [' ', '🪙', '☠️']:
            self.position = (x - 1, y)
        elif direction == 'd' and x < len(maze[0]) - 1 and maze[y][x + 1] in [
            ' ', '🪙', '☠️']:
            self.position = (x + 1, y)

        # Проверяет новую позицию на наличие монет или ловушек
        self.check_position(maze, maze_obj)
        return None

    def check_position(self, maze, maze_obj):
        """
        Проверяет текущую позицию игрока на наличие монет или ловушек и обновляет счет.

        :param maze: Текущий лабиринт в виде двумерного списка.
        :param maze_obj: Объект лабиринта для обновления поверхностей.
        """
        x, y = self.position
        if maze[y][x] == '🪙':
            self.score += 10
            maze[y][x] = ' '  # Заменяет монету на пустую ячейку
            maze_obj.set_surface(x, y, None)  # Обновляет объект лабиринта
        elif maze[y][x] == '☠️':
            self.score -= 20
            maze[y][x] = ' '  # Заменяет ловушку на пустую ячейку
            maze_obj.set_surface(x, y, None)  # Обновляет объект лабиринта

    def increase_score(self):
        """
        Увеличивает счет игрока на 100 очков.
        """
        self.score += 100
