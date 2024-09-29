import unittest

from src.custom_errors import LetterAlreadyGuessedError
from src.word_dictionary import WordDictionary
from src.word import Word
from src.error_handler import ErrorHandler
from src.hangman_game import HangmanGame


class TestHangmanGame(unittest.TestCase):
    def setUp(self):
        """
        Метод для установки начальных условий перед каждым тестом.
        """
        self.word_dictionary = WordDictionary()
        self.error_handler = ErrorHandler()
        self.hangman_game = HangmanGame(self.word_dictionary, "Средне",
                                        "Случайная", self.error_handler)

    def test_init(self):
        """
        Тест проверяет инициализацию игры.
        """
        self.assertEqual(self.hangman_game.remaining_attempts,
                         HangmanGame.attempts_by_difficulty["Средне"])
        self.assertEqual(self.hangman_game.guessed_letters, set())

    def test_guess_letter_already_guessed(self):
        """
        Тест проверяет угадывание буквы, которая уже была угадана.
        """
        self.hangman_game.current_word = Word("тест", "подсказка1",
                                              "подсказка2", "категория")
        self.hangman_game.guess_letter("т")
        with self.assertRaises(LetterAlreadyGuessedError):
            self.hangman_game.guess_letter("т")

    def test_guess_letter_not_in_word(self):
        """
        Тест проверяет угадывание буквы, которая не присутствует в слове.
        """
        self.hangman_game.current_word = Word("тест", "подсказка1",
                                              "подсказка2", "категория")
        self.hangman_game.guess_letter("а")
        self.assertEqual(self.hangman_game.remaining_attempts,
                         HangmanGame.attempts_by_difficulty["Средне"] - 1)

    def test_is_game_over_word_guessed(self):
        """
        Тест проверяет, окончена ли игра, когда слово было угадано.
        """
        self.hangman_game.current_word = Word("тест", "подсказка1",
                                              "подсказка2", "категория")
        self.hangman_game.guessed_letters = set("тест")
        self.assertTrue(self.hangman_game.is_game_over)

    def test_is_word_guessed_false(self):
        """
        Тест проверяет, угадано ли слово, когда слово еще не было угадано.
        """
        self.hangman_game.current_word = Word("тест", "подсказка1",
                                              "подсказка2", "категория")
        self.hangman_game.guessed_letters = set("ес")
        self.assertFalse(self.hangman_game.is_word_guessed)

    def test_reset_game(self):
        """
        Тест проверяет сброс игры.
        """
        self.hangman_game.reset_game("Средне", "Случайная", self.error_handler)
        self.assertEqual(self.hangman_game.remaining_attempts,
                         HangmanGame.attempts_by_difficulty["Средне"])
        self.assertEqual(self.hangman_game.guessed_letters, set())

    def test_guess_letter(self):
        """
        Тест проверяет угадывание буквы.
        """
        self.hangman_game.current_word = Word("тест", "подсказка1",
                                              "подсказка2", "категория")
        self.hangman_game.guess_letter("т")
        self.assertIn("т", self.hangman_game.guessed_letters)

    def test_word_display(self):
        """
        Тест проверяет отображение текущего состояния слова.
        """
        self.hangman_game.current_word = Word("тест", "подсказка1",
                                              "подсказка2", "категория")
        self.hangman_game.guess_letter("т")
        self.assertEqual(self.hangman_game.word_display, "т__т")

    def test_is_game_over(self):
        """
        Тест проверяет, окончена ли игра.
        """
        self.hangman_game.current_word = Word("тест", "подсказка1",
                                              "подсказка2", "категория")
        self.hangman_game.remaining_attempts = 0
        self.assertTrue(self.hangman_game.is_game_over)

    def test_is_word_guessed(self):
        """
        Тест проверяет, угадано ли слово.
        """
        self.hangman_game.current_word = Word("тест", "подсказка1",
                                              "подсказка2", "категория")
        self.hangman_game.guessed_letters = set("тест")
        self.assertTrue(self.hangman_game.is_word_guessed)


if __name__ == '__main__':
    unittest.main()
