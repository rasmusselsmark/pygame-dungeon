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
        # Get delta time
        dt = self.clock.get_time() / 1000.0

        # move player
        keys = pygame.key.get_pressed()
        self.player.update(keys, dt)

        # Check for player attacks hitting enemies
        if self.player.is_attacking and not self.player.has_hit_this_attack:
            # Check if we're in the middle of attack animation (frames 2-4)
            if 2 <= self.player.attack_frame <= 4:
                attack_rect = self.player.get_attack_rect()
                for enemy in self.level_manager.current_level.enemies:
                    if enemy.is_alive and not enemy.is_dying:
                        if attack_rect.colliderect(enemy.get_rect()):
                            enemy.take_damage(self.player.attack_damage)
                            self.player.has_hit_this_attack = True
                            break

        # Check for enemy collision with player
        if self.player.is_alive and not self.player.is_dying:
            player_rect = self.player.get_rect()
            for enemy in self.level_manager.current_level.enemies:
                if enemy.is_alive and not enemy.is_dying:
                    if player_rect.colliderect(enemy.get_rect()):
                        self.player.take_damage(10)
                        break

        # Update current level (enemies, etc.)
        self.level_manager.current_level.update(self.player, dt)

        # check if player is at an exit
        if self.player.is_alive:
            self.level_manager.check_transition(self.player)

    def draw(self):
        # Draw level (background and enemies)
        self.level_manager.current_level.draw(self.screen)

        # Draw player on top
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
