import unittest
from unittest.mock import patch
from src.word_dictionary import WordDictionary
from src.word import Word
from src.error_handler import ErrorHandler


class TestWordDictionary(unittest.TestCase):
    def setUp(self):
        """
        Метод для установки начальных условий перед каждым тестом.
        """
        self.word_dictionary = WordDictionary()
        self.error_handler = ErrorHandler()

    def test_add_word(self):
        """
        Тест проверяет добавление слова в словарь.
        """
        word_count = len(self.word_dictionary.words)
        self.word_dictionary.add_word("тест", "подсказка1", "подсказка2",
                                      "категория")
        self.assertEqual(len(self.word_dictionary.words), word_count + 1)

    @patch('random.choice')
    def test_get_random_word(self, mock_random_choice):
        """
        Тест проверяет получение случайного слова из словаря.
        """
        mock_random_choice.return_value = Word("тест", "подсказка1",
                                               "подсказка2", "категория")
        word = self.word_dictionary.get_random_word()
        self.assertEqual(word.word, "тест")

    def test_get_word_by_difficulty_and_category(self):
        """
        Тест проверяет получение слова из словаря по сложности и категории.
        """
        word = self.word_dictionary.get_word_by_difficulty_and_category(
            "Легко", "категория", self.error_handler)
        self.assertIsInstance(word, Word)

    def test_get_word_by_difficulty_and_category_no_word(self):
        """
        Тест проверяет получение слова из словаря по сложности и категории,
        когда нет подходящего слова.
        """
        self.word_dictionary.words = []

        word = self.word_dictionary.get_word_by_difficulty_and_category(
            "Легко", "категория", self.error_handler)
        self.assertIsNone(word)

        self.assertEqual(self.error_handler.error_message,
                         "Ошибка: Не нашлось слов с выбранной категорией ("
                         "категория) и сложностью (Легко). Попробуйте другие "
                         "параметры.")

    def test_unique_categories(self):
        """
        Тест проверяет получение уникальных категорий слов в словаре.
        """
        categories = self.word_dictionary.unique_categories
        self.assertIsInstance(categories, list)

    def test_unique_difficulties(self):
        """
        Тест проверяет получение уникальных сложностей слов в словаре.
        """
        difficulties = self.word_dictionary.unique_difficulties
        self.assertIsInstance(difficulties, list)


if __name__ == '__main__':
    unittest.main()
