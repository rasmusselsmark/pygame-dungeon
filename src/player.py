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
        self.is_attacking = False
        self.attack_frame = 0
        self.attack_frames = 6

        # Combat
        self.attack_damage = 25
        self.has_hit_this_attack = False

        # Sprite rows for each direction (row index in sprite sheet)
        self.animations = {
            "right": 1,
            "up": 2,
            "left": 3,
            "down": 4,
        }

        # Attack animation rows
        self.attack_animations = {
            "right": 16,
            "up": 17,
            "left": 18,
            "down": 19,
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
        # Handle attack
        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL] or keys[pygame.K_SPACE]:
            if not self.is_attacking:
                self.is_attacking = True
                self.attack_frame = 0
                self.has_hit_this_attack = False

        # If attacking, play attack animation
        if self.is_attacking:
            self.animation_counter += self.animation_speed * 1.5
            if self.animation_counter >= 1:
                self.animation_counter = 0
                self.attack_frame += 1

                if self.attack_frame >= self.attack_frames:
                    self.is_attacking = False
                    self.attack_frame = 0

            # Get attack sprite
            row = self.attack_animations[self.direction]
            self.current_sprite = self.get_sprite(self.attack_frame, row)
            return

        # Normal movement and animation
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

    def get_attack_rect(self):
        """Get attack hitbox rect based on direction"""
        attack_range = 60
        attack_width = 50

        if self.direction == "right":
            return pygame.Rect(self.x + self.display_size, self.y, attack_range, self.display_size)
        elif self.direction == "left":
            return pygame.Rect(self.x - attack_range, self.y, attack_range, self.display_size)
        elif self.direction == "up":
            return pygame.Rect(self.x, self.y - attack_range, self.display_size, attack_range)
        elif self.direction == "down":
            return pygame.Rect(self.x, self.y + self.display_size, self.display_size, attack_range)

        return pygame.Rect(0, 0, 0, 0)
