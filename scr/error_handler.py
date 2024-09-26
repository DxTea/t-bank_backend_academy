class ErrorHandler:
    """
    Класс для обработки ошибок.
    """

    def __init__(self) -> None:
        """
        Инициализация класса ErrorHandler.
        """
        self._error_message: str = ""

    @property
    def error_message(self) -> str:
        """
        Возвращает текущее сообщение об ошибке.
        """
        return self._error_message

    def handle_error(self, error: Exception) -> str:
        """
        Обрабатывает ошибку и устанавливает сообщение об ошибке.

        Args:
            error (Exception): Объект исключения.

        Returns:
            str: Сообщение об ошибке.
        """
        self._error_message = f"Ошибка: {str(error)}"
        return self._error_message

    def set_error_message(self, message: str) -> None:
        """
        Устанавливает сообщение об ошибке.

        Args:
            message (str): Сообщение об ошибке.
        """
        self._error_message = message

    def clear_error(self) -> None:
        """
        Очищает сообщение об ошибке.
        """
        self._error_message = ""
