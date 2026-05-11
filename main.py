from src.game import Game


def main():
    game = Game(width=800, height=600, title="2D Dungeon Game")
    game.run()


if __name__ == "__main__":
    main()
