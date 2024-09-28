import unittest
from src.word import Word


class TestWord(unittest.TestCase):
    def setUp(self):
        """
        Метод для установки начальных условий перед каждым тестом.
        """
        self.word = Word("тест", "подсказка1", "подсказка2",
                         "категория")

    def test_length(self):
        """
        Тест проверяет свойство length.
        """
        self.assertEqual(self.word.length, 4)

    def test_hints(self):
        """
        Тест проверяет свойство hints.
        """
        self.assertEqual(self.word.hints, ["подсказка1", "подсказка2"])

    def test_difficulty(self):
        """
        Тест проверяет свойство difficulty.
        """
        self.assertEqual(self.word.difficulty, "Легко")


if __name__ == '__main__':
    unittest.main()
