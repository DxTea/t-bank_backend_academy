class InvalidMenuChoiceError(Exception):
    """Ошибка, возникающая при недопустимом выборе в меню."""
    pass


class InvalidOptionChoiceError(Exception):
    """Ошибка, возникающая при недопустимом выборе опции."""
    pass


class InvalidUserGuessError(Exception):
    """Ошибка, возникающая при недопустимом вводе пользователя."""
    pass


class InvalidParametersError(Exception):
    """Ошибка, возникающая при недопустимых параметрах"""
    pass


class HintUsageError(Exception):
    """Ошибка, возникающая при недопустимом использовании подсказки."""
    pass
