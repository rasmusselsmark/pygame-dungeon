from src.game import Game


def main():
    game = Game(width=1200, height=800, title="2D Dungeon Game")
    game.run()


if __name__ == "__main__":
    main()
