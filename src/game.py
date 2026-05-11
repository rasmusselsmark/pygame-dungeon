import pygame
import os
from pygame.locals import *


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

        # Load background image
        bg_path = os.path.join("assets", "images", "background.png")
        self.background = pygame.image.load(bg_path).convert()
        self.background = pygame.transform.scale(self.background, (width, height))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
        pygame.quit()
