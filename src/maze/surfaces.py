class Surface:
    def __init__(self, symbol, cost_modifier):
        """
        Базовый класс для поверхностей в лабиринте.

        :param symbol: Символ, представляющий поверхность.
        :param cost_modifier: Модификатор стоимости пути при прохождении
        через поверхность.
        """
        self.symbol = symbol
        self.cost_modifier = cost_modifier


class Trap(Surface):
    def __init__(self):
        """
        Класс для ловушек в лабиринте.
        Ловушка увеличивает стоимость пути на 10.
        """
        super().__init__('☠️', 10)


class Coin(Surface):
    def __init__(self):
        """
        Класс для монет в лабиринте. Монета уменьшает стоимость пути на 5.
        """
        super().__init__('🪙', -5)
