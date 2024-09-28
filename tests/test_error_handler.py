from src.custom_errors import InvalidMenuChoiceError
from src.error_handler import ErrorHandler


class TestErrorHandler:
    def test_handle_error(self):
        """
        Тест проверяет, что метод handle_error корректно обрабатывает
        исключения и устанавливает сообщение об ошибке.
        """
        error_handler = ErrorHandler()
        error_message = error_handler.handle_error(
            Exception("Тестовая ошибка"))
        assert error_message == "Ошибка: Тестовая ошибка"

    def test_set_error_message(self):
        """
        Тест проверяет, что метод set_error_message корректно устанавливает
        сообщение об ошибке.
        """
        error_handler = ErrorHandler()
        error_handler.set_error_message("Тестовая ошибка")
        assert error_handler.error_message == "Тестовая ошибка"

    def test_clear_error(self):
        """
        Тест проверяет, что метод clear_error корректно очищает сообщение
        об ошибке.
        """
        error_handler = ErrorHandler()
        error_handler.set_error_message("Тестовая ошибка")
        error_handler.clear_error()
        assert error_handler.error_message == ""

    def test_handle_specific_error(self):
        """
        Тест проверяет, что метод handle_error корректно обрабатывает
        специфические исключения.
        """
        error_handler = ErrorHandler()
        error_message = error_handler.handle_error(
            InvalidMenuChoiceError("Неправильный выбор"))
        assert error_message == "Ошибка: Неправильный выбор"

    def test_handle_error_without_exception(self):
        """
        Тест проверяет, что метод handle_error корректно обрабатывает ситуацию,
        когда исключение не было передано.
        """
        error_handler = ErrorHandler()
        error_message = error_handler.handle_error(None)
        assert error_message == "Ошибка: None"

    def test_set_error_message_with_special_characters(self):
        """
        Тест проверяет, что метод set_error_message корректно обрабатывает
        сообщения об ошибках со специальными символами.
        """
        error_handler = ErrorHandler()
        error_handler.set_error_message(
            "Тестовая ошибка со специальными символами: !@#$%^&*()")
        assert (error_handler.error_message ==
                "Тестовая ошибка со специальными символами: !@#$%^&*()")

    def test_clear_error_after_handle_error(self):
        """
        Тест проверяет, что метод clear_error корректно очищает сообщение об
        ошибке после вызова метода handle_error.
        """
        error_handler = ErrorHandler()
        error_handler.handle_error(Exception("Тестовая ошибка"))
        error_handler.clear_error()
        assert error_handler.error_message == ""
