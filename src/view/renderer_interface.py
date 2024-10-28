from abc import ABC, abstractmethod
from typing import List, Any


class IRenderer(ABC):
    """
    Интерфейс IRenderer определяет контракт для всех классов, которые будут
    его реализовывать.
    Он используется для обеспечения единообразия в реализации различных
    рендереров.
    """

    @abstractmethod
    def render_maze(self, maze: Any) -> None:
        """
        Метод для рендеринга лабиринта.

        :param maze: Лабиринт, который нужно отобразить.
        """
        pass

    @abstractmethod
    def display_game_settings_menu(self, menu_options: List[str]) -> None:
        """
        Метод для рендеринга меню.

        :param menu_options: Опции меню, которые нужно отобразить.
        """
        pass

    @abstractmethod
    def display_welcome_screen(self) -> None:
        """
        Метод для рендеринга приветственного экрана.
        """
        pass
