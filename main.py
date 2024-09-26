from scr.word_dictionary import WordDictionary
from scr.game_loop import GameLoop

if __name__ == "__main__":
    word_dictionary = WordDictionary()
    game_loop = GameLoop(word_dictionary)
    game_loop.run()
