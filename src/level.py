import pygame
import os


class Level:
    def __init__(self, name, background_file, width, height):
        self.name = name
        self.width = width
        self.height = height

        # Load and scale background
        bg_path = os.path.join("assets", "images", background_file)
        self.background = pygame.image.load(bg_path).convert()
        self.background = pygame.transform.scale(self.background, (width, height))

        # Define exit zones (x, y, width, height) and their directions
        exit_margin = 80
        exit_width = 120
        exit_height = 80

        self.exits = {
            "top": pygame.Rect(width // 2 - exit_width // 2, 0, exit_width, exit_height),
            "bottom": pygame.Rect(width // 2 - exit_width // 2, height - exit_height, exit_width, exit_height),
            "left": pygame.Rect(0, height // 2 - exit_width // 2, exit_height, exit_width),
            "right": pygame.Rect(width - exit_height, height // 2 - exit_width // 2, exit_height, exit_width)
        }

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

    def check_exit(self, player_rect):
        """Check if player is in an exit zone, return direction or None"""
        for direction, exit_rect in self.exits.items():
            if player_rect.colliderect(exit_rect):
                return direction
        return None


class LevelManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Create levels
        self.levels = {
            "dungeon": Level("dungeon", "dungeon.png", width, height),
            "forest": Level("forest", "forest.png", width, height)
        }

        # Define level connections (level_name -> {direction: (next_level, entry_direction)})
        self.connections = {
            "dungeon": {
                "top": ("forest", "bottom"),
                "bottom": ("forest", "top"),
                "left": ("forest", "right"),
                "right": ("forest", "left")
            },
            "forest": {
                "top": ("dungeon", "bottom"),
                "bottom": ("dungeon", "top"),
                "left": ("dungeon", "right"),
                "right": ("dungeon", "left")
            }
        }

        # Start in dungeon
        self.current_level_name = "dungeon"

    @property
    def current_level(self):
        return self.levels[self.current_level_name]

    def check_transition(self, player):
        """Check if player should transition to another level"""
        exit_direction = self.current_level.check_exit(player.get_rect())

        if exit_direction and exit_direction in self.connections[self.current_level_name]:
            next_level_name, entry_direction = self.connections[self.current_level_name][exit_direction]
            self.transition_to_level(next_level_name, entry_direction, player)

    def transition_to_level(self, level_name, entry_direction, player):
        """Transition to a new level and position player at entry point"""
        self.current_level_name = level_name

        # Position player based on entry direction (opposite of exit)
        padding = 100

        if entry_direction == "top":
            player.x = self.width // 2 - player.display_size // 2
            player.y = padding
        elif entry_direction == "bottom":
            player.x = self.width // 2 - player.display_size // 2
            player.y = self.height - padding - player.display_size
        elif entry_direction == "left":
            player.x = padding
            player.y = self.height // 2 - player.display_size // 2
        elif entry_direction == "right":
            player.x = self.width - padding - player.display_size
            player.y = self.height // 2 - player.display_size // 2
