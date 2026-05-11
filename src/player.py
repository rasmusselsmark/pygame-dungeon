import pygame
import os


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3
        self.sprite_size = 32
        self.scale = 3
        self.display_size = self.sprite_size * self.scale

        # Load sprite sheet
        sheet_path = os.path.join("assets", "images", "CharAni-Sheet4.png")
        self.sprite_sheet = pygame.image.load(sheet_path).convert_alpha()

        # Animation state
        self.direction = "down"
        self.frame = 0
        self.animation_speed = 0.15
        self.animation_counter = 0
        self.is_moving = False

        # Sprite rows for each direction (row index in sprite sheet)
        self.animations = {
            "right": 1,
            "up": 2,
            "left": 3,
            "down": 4,
        }

        # Current sprite
        self.current_sprite = self.get_sprite(0, 0)

    def get_sprite(self, col, row):
        """Extract a sprite from the sprite sheet"""
        sprite = pygame.Surface((self.sprite_size, self.sprite_size), pygame.SRCALPHA)
        sprite.blit(self.sprite_sheet, (0, 0),
                   (col * self.sprite_size, row * self.sprite_size,
                    self.sprite_size, self.sprite_size))
        return pygame.transform.scale(sprite, (self.display_size, self.display_size))

    def update(self, keys):
        """Update player position and animation"""
        dx = 0
        dy = 0

        # Handle input (WASD and arrow keys)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
            self.direction = "left"
            self.is_moving = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
            self.direction = "right"
            self.is_moving = True

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
            self.direction = "up"
            self.is_moving = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed
            self.direction = "down"
            self.is_moving = True

        # Check if not moving
        if dx == 0 and dy == 0:
            self.is_moving = False
            self.frame = 0

        # Update position
        self.x += dx
        self.y += dy

        # Update animation
        if self.is_moving:
            self.animation_counter += self.animation_speed
            if self.animation_counter >= 1:
                self.animation_counter = 0
                self.frame = (self.frame + 1) % 8

        # Get current sprite
        row = self.animations[self.direction]
        self.current_sprite = self.get_sprite(self.frame, row)

    def draw(self, screen):
        """Draw the player on screen"""
        screen.blit(self.current_sprite, (self.x, self.y))

    def get_rect(self):
        """Get player rect for collision detection"""
        return pygame.Rect(self.x, self.y, self.display_size, self.display_size)
