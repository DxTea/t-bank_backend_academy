import random

from src.custom_errors import InvalidParametersError
from src.list_of_words import words
from typing import List, Optional
from src.word import Word
from src.error_handler import ErrorHandler


class WordDictionary:
    """
    Класс представляет словарь слов,
    из которого выбирается случайное слово для игры.
    """

    def __init__(self) -> None:
        """
        Инициализация класса WordDictionary.
        """
        self.words: List[Word] = words

    def add_word(self, word: str, hint1: str, hint2: str,
                 category: str) -> None:
        """
        Метод для добавления слова в словарь.

        Args:
            word (str): Слово, которое нужно добавить.
            hint1 (str): Первая подсказка, связанная со словом.
            hint2 (str): Вторая подсказка, связанная со словом.
            category (str): Категория, к которой относится слово.
        """
        self.words.append(Word(word, hint1, hint2, category))

    def get_random_word(self) -> Word:
        """
        Метод для получения случайного слова из словаря.

        Returns:
            Word: Случайное слово из словаря.
        """
        return random.choice(self.words)

    def get_word_by_difficulty_and_category(self, difficulty: str,
                                            category: str,
                                            error_handler: ErrorHandler) -> \
            Optional[Word]:
        """
        Метод для получения слова из словаря по сложности и категории.

        Args:
            difficulty (str): Сложность слова.
            category (str): Категория слова.
            error_handler: Обработчик ошибок.

        Returns:
            Word: Слово из словаря, соответствующее заданным параметрам.
        """
        filtered_words = [word for word in self.words if
                          (word.difficulty == difficulty or
                           difficulty == "Случайно") and
                          (word.category == category or
                           category == "Случайная")]

        if not filtered_words:
            error_message = (
                f"Не нашлось слов с выбранной категорией ({category}) "
                f"и сложностью ({difficulty}). "
                f"Попробуйте другие параметры.")
            error_handler.handle_error(InvalidParametersError(error_message))
            return None
        return random.choice(filtered_words)

    @property
    def unique_categories(self):
        """
        Свойство для получения уникальных категорий слов в словаре.

        Returns:
            list: Список уникальных категорий.
        """
        return list(set(word.category for word in self.words))

    @property
    def unique_difficulties(self):
        """
        Свойство для получения уникальных сложностей слов в словаре.

        Returns:
            list: Список уникальных сложностей.
        """
        return list(set(word.difficulty for word in self.words))
