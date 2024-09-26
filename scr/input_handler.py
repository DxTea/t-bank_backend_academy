from scr.custom_errors import InvalidMenuChoiceError, InvalidUserGuessError, HintUsageError


class InputHandler:
    """Класс для обработки ввода пользователя."""

    @staticmethod
    def get_user_input(prompt: str) -> str:
        """
        Метод для получения ввода пользователя.

        Args:
            prompt (str): Строка, которую нужно вывести перед вводом пользователя.

        Returns:
            str: Введенная пользователем строка.
        """
        return input(prompt)

    @staticmethod
    def validate_menu_choice(choice: str, valid_choices: list) -> str:
        """
        Метод для проверки выбора пользователя в меню.

        Args:
            choice (str): Выбор пользователя.
            valid_choices (list): Список допустимых выборов.

        Returns:
            str: Валидный выбор пользователя.

        Raises:
            InvalidMenuChoiceError: Если выбор пользователя недопустим.
        """
        if choice not in valid_choices:
            raise InvalidMenuChoiceError(f"Недопустимый ввод: '{choice}'. Пожалуйста, введите номер пункта меню.")
        return choice

    @staticmethod
    def validate_user_guess(guess: str) -> str:
        """
        Метод для проверки предположения пользователя.

        Args:
            guess (str): Предположение пользователя.

        Returns:
            str: Валидное предположение пользователя.

        Raises:
            InvalidUserGuessError: Если предположение пользователя недопустимо.
        """
        if guess not in ["1", "2", "3", "4"] and (not guess.isalpha() or len(guess) > 1):
            raise InvalidUserGuessError(
                f"Недопустимый ввод: '{guess}'. Пожалуйста, введите номер пункта меню или букву.")
        return guess

    @staticmethod
    def validate_hint_usage(hint_index: int, hints: list) -> None:
        """
        Метод для проверки использования подсказки.

        Args:
            hint_index (int): Индекс подсказки.
            hints (list): Список подсказок.

        Raises:
            HintUsageError: Если подсказка уже использована.
        """
        if hints[hint_index].startswith("Подсказка"):
            raise HintUsageError(f"Недопустимый ввод: '{hint_index + 1}'. Подсказка {hint_index + 1} уже использована.")
