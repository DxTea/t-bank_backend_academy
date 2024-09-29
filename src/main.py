import logging
import platform

from .game_loop import GameLoop
from .render import Renderer
from .word_dictionary import WordDictionary

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info(platform.python_version())
    Renderer.display_welcome_screen()
    word_dictionary = WordDictionary()
    game_loop = GameLoop(word_dictionary)
    game_loop.run()


if __name__ == "__main__":
    main()
