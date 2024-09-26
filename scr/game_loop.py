import random
import sys
from typing import List

from scr.custom_errors import InvalidMenuChoiceError, HintUsageError, InvalidUserGuessError
from scr.hangman_game import HangmanGame
from scr.render import Renderer
from scr.word_dictionary import WordDictionary
from scr.input_handler import InputHandler
from scr.error_handler import ErrorHandler


class GameLoop:
    """
    Класс для управления циклом игры.
    """

    def __init__(self, word_dictionary: WordDictionary,
                 difficulty: str = "Случайно",
                 category: str = "Случайная"):
        """
        Инициализация класса GameLoop.

        Args:
            word_dictionary (WordDictionary): Словарь слов для игры.
            difficulty (str, optional): Сложность игры. По умолчанию "Случайно".
            category (str, optional): Категория игры. По умолчанию "Случайная".
        """
        self.word_dictionary: WordDictionary = word_dictionary
        self.error_handler = ErrorHandler()
        self.difficulty: str = difficulty
        self.category: str = category

    def run(self) -> None:
        """
        Метод для запуска цикла игры.
        """
        while True:
            self.clear_screen_and_display_errors()

            Renderer.render_main_menu(self.category, self.difficulty)
            choice = InputHandler.get_user_input("Введите номер пункта меню: ")
            try:
                self.handle_main_menu_choice(choice)
            except InvalidMenuChoiceError as e:
                self.error_handler.handle_error(e)

    def start_game(self) -> None:
        """
        Метод для начала игры.
        """

        self.set_random_category_and_difficulty_if_needed()
        game = HangmanGame(self.word_dictionary,
                           self.difficulty,
                           self.category,
                           self.error_handler)
        game.reset_game(self.difficulty, self.category, self.error_handler)

        if game.current_word is None:
            Renderer.display_error_if_exists(self.error_handler.error_message)
            return
        renderer = Renderer(game)
        hints = ["1. Подсказка 1", "2. Подсказка 2"]
        while not game.is_game_over:

            self.clear_screen_and_display_errors()

            renderer.render_game()
            Renderer.render_game_menu(hints)
            try:
                guess = InputHandler.get_user_input('Введите номер пункта меню или введите вашу букву: ')
                try:
                    InputHandler.validate_user_guess(guess)
                except InvalidUserGuessError as e:
                    self.error_handler.handle_error(e)
                    continue
                if guess in ["1", "2"]:
                    self.handle_hint(guess, hints, game)
                elif guess == "3":
                    break
                elif guess == "4":
                    self.exit_program()
                else:
                    game.guess_letter(guess.lower())
            except InvalidUserGuessError as e:
                self.error_handler.handle_error(e)
                continue

        renderer.render_game_result(game)
        self.post_game()

    def handle_hint(self, guess: str, hints: List[str], game: HangmanGame) -> None:
        """
        Метод для обработки подсказки.

        Args:
            guess (str): Предположение пользователя.
            hints (List[str]): Список подсказок.
            game (HangmanGame): Объект игры.
        """
        hint_index = int(guess) - 1
        try:
            InputHandler.validate_hint_usage(hint_index, hints)
            hints[hint_index] = f"Подсказка {guess}: {game.current_word.hints[hint_index]}"
        except HintUsageError as e:
            self.error_handler.handle_error(e)

    def handle_main_menu_choice(self, choice):
        """
        Метод для обработки выбора в главном меню.

        Args:
            choice: Выбор пользователя.
        """
        choice = InputHandler.validate_menu_choice(choice, ["1", "2", "3", "4"])
        match choice:
            case "1":
                self.start_game()
            case "2":
                self.choose_category()
            case "3":
                self.choose_difficulty()
            case "4":
                self.exit_program()

    def reset_settings(self) -> None:
        """
        Метод для сброса настроек игры на дефолтные значения.
        """
        self.difficulty = "Случайно"
        self.category = "Случайная"

    def post_game(self) -> None:
        """
        Метод для действий после игры.
        """
        while True:
            Renderer.render_post_game_menu()
            try:
                post_game_choice = InputHandler.get_user_input("Введите номер пункта меню: ")
                InputHandler.validate_menu_choice(post_game_choice, ["1", "2"])
                if post_game_choice == "1":
                    self.reset_settings()
                    self.return_to_main_menu()
                elif post_game_choice == "2":
                    self.exit_program()
            except InvalidMenuChoiceError as e:
                self.error_handler.handle_error(e)
                self.clear_screen_and_display_errors()
                continue

    def choose_category(self) -> None:
        """
        Метод для выбора категории.
        """
        self.choose_option("категории", self.word_dictionary.unique_categories, "category")

    def choose_difficulty(self) -> None:
        """
        Метод для выбора сложности.
        """
        self.choose_option("сложности", ["Легко", "Средне", "Сложно"], "difficulty")

    def choose_option(self, option_name: str, options: List[str], attribute_name: str) -> None:
        """
        Метод для выбора опции.

        Args:
            option_name (str): Название опции.
            options (List[str]): Список возможных опций.
            attribute_name (str): Название атрибута.
        """
        while True:
            self.clear_screen_and_display_errors()
            Renderer.render_choose_option_menu(options)
            try:
                option_choice = InputHandler.get_user_input(f"Введите номер {option_name}: ")
                InputHandler.validate_menu_choice(option_choice, [str(i) for i in range(len(options) + 1)])
                if option_choice == "0":
                    setattr(self, attribute_name, "Случайно")
                else:
                    setattr(self, attribute_name, options[int(option_choice) - 1])
                break
            except InvalidMenuChoiceError as e:
                self.error_handler.handle_error(e)
                continue

    def set_random_category_and_difficulty_if_needed(self) -> None:
        """
        Метод для установки случайной категории и сложности, если это необходимо.
        """
        if self.category == "Случайно":
            self.category = random.choice(self.word_dictionary.unique_categories)
        if self.difficulty == "Случайно":
            self.difficulty = random.choice(self.word_dictionary.unique_difficulties)

    @staticmethod
    def exit_program() -> None:
        """
        Метод для завершения программы.
        """
        sys.exit()

    def return_to_main_menu(self) -> None:
        """
        Метод для возвращения в главное меню.
        """
        self.run()

    def clear_screen_and_display_errors(self) -> None:
        """
        Метод для очистки экрана и отображения ошибок.
        """
        Renderer.clear_screen()
        Renderer.display_error_if_exists(self.error_handler.error_message)
        self.error_handler.clear_error()
