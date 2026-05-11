import pygame
from pygame.locals import *
from src.player import Player
from src.level import LevelManager


class Game:
    def __init__(self, width=800, height=600, title="PyGame Dungeon"):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = False
        self.fps = 60

        # Create level manager
        self.level_manager = LevelManager(width, height)

        # Create player in center of screen
        self.player = Player(width // 2 - 24, height // 2 - 24)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False

    def update(self):
        # move player
        keys = pygame.key.get_pressed()
        self.player.update(keys)

        # check if player is at an exit
        self.level_manager.check_transition(self.player)

    def draw(self):
        self.level_manager.current_level.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
        pygame.quit()
