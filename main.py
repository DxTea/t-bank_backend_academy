from src.word_dictionary import WordDictionary
from src.game_loop import GameLoop
from src.render import Renderer

if __name__ == "__main__":
    Renderer.display_welcome_screen()
    word_dictionary = WordDictionary()
    game_loop = GameLoop(word_dictionary)
    game_loop.run()
