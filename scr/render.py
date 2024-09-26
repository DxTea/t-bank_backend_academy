import os
from typing import List
from scr.hangman_game import HangmanGame
from scr.word import Word


class Renderer:
    """
    Класс для отображения текущего состояния игры в консоли.
    Он может отображать текущее слово с пропусками, количество оставшихся попыток и виселицу.
    """

    def __init__(self, game: HangmanGame) -> None:
        """
        Инициализация класса Renderer.

        Args:
            game: Объект игры.
        """
        self.game = game
        self.hangman_pictures: List[str] = [
            '''
              +---+
              |   |
                  |
                  |
                  |
                  |
            =========
            ''',
            '''
              +---+
              |   |
              O   |
                  |
                  |
                  |
            =========
            ''',
            '''
              +---+
              |   |
              O   |
              |   |
                  |
                  |
            =========
            ''',
            '''
              +---+
              |   |
              O   |
             /|   |
                  |
                  |
            =========
            ''',
            '''
              +---+
              |   |
              O   |
             /|\\  |
                  |
                  |
            =========
            ''',
            '''
              +---+
              |   |
              O   |
             /|\\  |
             /    |
                  |
            =========
            ''',
            '''
              +---+
              |   |
              O   |
             /|\\  |
             / \\  |
                  |
            =========
            '''
        ]

    @property
    def used_letters(self) -> str:
        """
        Свойство для получения использованных букв.
        """
        return ', '.join(sorted(self.game.guessed_letters))

    def render_game(self) -> None:
        """
        Метод для отображения текущего состояния игры.
        """
        picture_index = len(self.hangman_pictures) - self.game.remaining_attempts
        print(
            f'{self.hangman_pictures[picture_index]}\n'
            f'Слово: {self.game.word_display}\n'
            f'Осталось попыток: {self.game.remaining_attempts}\n'
            f'Использованные буквы: {self.used_letters}'
        )

    @staticmethod
    def render_game_result(game: HangmanGame) -> None:
        """
        Метод для отображения результата игры.

        Args:
            game: Объект игры.
        """
        if game.is_word_guessed:
            print(f'Поздравляем, мы выиграли! Загаданное слово было : {game.current_word.word}')
        else:
            print(f'Жаль, но вы проиграли. Загаданное слово было : {game.current_word.word}')

    @staticmethod
    def view_word(word: Word) -> None:
        """
        Метод для просмотра слова.

        Args:
            word: Слово для просмотра.
        """
        print(
            f"Слово:{word.word}\n"
            f"Подсказка 1: {word.hint1}\n"
            f"Подсказка 2: {word.hint2}\n"
            f"Категория: {word.category}\n"
            f"Сложность: {word.difficulty}"
        )

    @staticmethod
    def render_main_menu(current_category: str, current_difficulty: str) -> None:
        """
        Метод для отображения главного меню.

        Args:
            current_category (str): Текущая категория.
            current_difficulty (str): Текущая сложность.
        """
        print(f"1. Начать игру\n"
              f"2. Выбрать категорию (текущая: {current_category})\n"
              f"3. Выбрать сложность (текущая: {current_difficulty})\n"
              f"4. Выход")

    @staticmethod
    def render_game_menu(hints: List[str]) -> None:
        """
        Метод для отображения меню игры.

        Args:
            hints (List[str]): Список подсказок.
        """
        for hint in hints:
            print(hint)
        print(f"3. Сдаться\n"
              f"4. Выход из игры")

    @staticmethod
    def render_post_game_menu() -> None:
        """
        Метод для отображения меню после игры.
        """
        print(f"1. В меню\n"
              f"2. Выход из игры")

    @staticmethod
    def render_choose_option_menu(options: List[str]) -> None:
        """
        Метод для отображения меню выбора опции.

        Args:
            options (List[str]): Список опций.
        """
        print(f"0. Случайно")
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

    @staticmethod
    def clear_screen() -> None:
        """
        Метод для очистки экрана.
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def display_error_if_exists(error_message: str) -> None:
        """
        Метод для отображения ошибки, если она существует.

        Args:
            error_message (str): Сообщение об ошибке.
        """
        if error_message:
            print(error_message)
