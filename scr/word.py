from typing import List


class Word:
    """
    Класс представляет слово, которое нужно угадать, и содержит связанные с ним подсказки и категорию.
    """

    def __init__(self, word: str, hint1: str, hint2: str, category: str) -> None:
        """
        Инициализация класса Word.

        Args:
            word (str): Слово, которое нужно угадать.
            hint1 (str): Первая подсказка, связанная со словом.
            hint2 (str): Вторая подсказка, связанная со словом.
            category (str): Категория, к которой относится слово.
        """
        self.word = word
        self.hint1 = hint1
        self.hint2 = hint2
        self.category = category

    @property
    def length(self) -> int:
        """
        Свойство для получения длины слова.

        Returns:
            int: Длина слова.
        """
        return len(self.word)

    @property
    def hints(self) -> List[str]:
        """
        Свойство для получения подсказок, связанных со словом.

        Returns:
            list: Список подсказок.
        """
        return [self.hint1, self.hint2]

    @property
    def difficulty(self) -> str:
        """
         Свойство для определения сложности слова на основе его длины.

         Returns:
             str: Сложность слова ("Легко", "Средне" или "Сложно").
         """
        if self.length < 5:
            return "Легко"
        elif 5 <= self.length < 8:
            return "Средне"
        else:
            return "Сложно"
