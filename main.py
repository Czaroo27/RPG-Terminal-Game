from game import Game

if __name__ == "__main__":
    game = Game()
    print("1. New Game\n2. Load Game")
    choice = input("> ")
    if choice == "2":
        if not game.load_game():
            print("Starting new game.")
            game.start()
        else:
            game.game_loop()
    else:
        game.start()