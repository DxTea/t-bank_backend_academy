from typing import Set

from src.custom_errors import LetterAlreadyGuessedError
from src.word import Word
from src.word_dictionary import WordDictionary
from src.error_handler import ErrorHandler


class HangmanGame:
    """
    Класс для управления игрой. Содержит текущее состояние игры,
    включая выбранное слово,
    текущее отображение слова с пропусками и количество оставшихся попыток.
    Содержит методы для обновления состояния игры.
    """
    attempts_by_difficulty = {
        "Легко": 7,
        "Средне": 5,
        "Сложно": 3
    }

    def __init__(self, word_dictionary: WordDictionary, difficulty: str,
                 category: str,
                 error_handler: ErrorHandler) -> None:
        """
        Инициализация класса HangmanGame.

        Args:
            word_dictionary: Словарь слов для игры.
            difficulty: Сложность игры.
            category: Категория игры.
            error_handler: Обработчик ошибок.
        """
        self.remaining_attempts: int = 0
        self.guessed_letters: Set[str] = set()
        self.word_dictionary: WordDictionary = word_dictionary
        self.current_word: Word = self.word_dictionary.get_random_word()
        self.reset_game(difficulty, category, error_handler)

    def reset_game(self, difficulty: str, category: str,
                   error_handler: ErrorHandler) -> None:
        """
        Метод для сброса игры.

        Args:
            difficulty: Сложность игры.
            category: Категория игры.
            error_handler: Обработчик ошибок.
        """
        word = self.word_dictionary.get_word_by_difficulty_and_category(
            difficulty, category, error_handler)
        if word is not None:
            self.current_word = word
            self.guessed_letters = set()
            self.remaining_attempts = self.attempts_by_difficulty[
                self.current_word.difficulty]

    def guess_letter(self, letter: str) -> None:
        """
        Метод для угадывания буквы.

        Args:
            letter: Буква, которую предполагает пользователь.
        """
        if letter in self.guessed_letters:
            raise LetterAlreadyGuessedError(
                "Эта буква уже была использована, попробуйте другую")
        self.guessed_letters.add(letter)
        if letter not in self.current_word.word:
            self.remaining_attempts -= 1

    @property
    def word_display(self) -> str:
        """
        Свойство для отображения текущего состояния слова.
        """
        return ''.join(
            letter if letter in self.guessed_letters else '_' for letter in
            self.current_word.word)

    @property
    def is_game_over(self) -> bool:
        """
        Свойство для проверки, окончена ли игра.
        """
        return (self.remaining_attempts <= 0 or self.word_display
                == self.current_word.word)

    @property
    def is_word_guessed(self) -> bool:
        """
        Свойство для проверки, угадано ли слово.
        """
        return self.word_display == self.current_word.word
