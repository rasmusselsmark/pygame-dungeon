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
        self.is_dying = False
        self.death_frame = 0
        self.death_frames = 8

        # Health
        self.health = 100
        self.max_health = 100
        self.is_alive = True
        self.damage_cooldown = 1.0  # seconds between taking damage
        self.damage_timer = 0

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

        # Death animation row
        self.death_animation_row = 15

        # Current sprite
        self.current_sprite = self.get_sprite(0, 0)

    def get_sprite(self, col, row):
        """Extract a sprite from the sprite sheet"""
        sprite = pygame.Surface((self.sprite_size, self.sprite_size), pygame.SRCALPHA)
        sprite.blit(self.sprite_sheet, (0, 0),
                   (col * self.sprite_size, row * self.sprite_size,
                    self.sprite_size, self.sprite_size))
        return pygame.transform.scale(sprite, (self.display_size, self.display_size))

    def update(self, keys, dt=0):
        """Update player position and animation"""
        # Update damage cooldown
        if self.damage_timer > 0:
            self.damage_timer -= dt

        # Handle death animation
        if self.is_dying:
            self.animation_counter += self.animation_speed * 0.8
            if self.animation_counter >= 1:
                self.animation_counter = 0
                self.death_frame += 1

                if self.death_frame >= self.death_frames:
                    self.death_frame = self.death_frames - 1  # Stay on last frame
                    self.is_alive = False

            self.current_sprite = self.get_sprite(self.death_frame, self.death_animation_row)
            return

        if not self.is_alive:
            # Keep showing the last death frame
            self.current_sprite = self.get_sprite(self.death_frames - 1, self.death_animation_row)
            return

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
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        """Draw health bar above player"""
        if not self.is_alive and not self.is_dying:
            return

        bar_width = 60
        bar_height = 5
        bar_x = int(self.x + (self.display_size - bar_width) // 2)
        bar_y = int(self.y - 10)

        # Background (red)
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # Health (green)
        health_width = int((self.health / self.max_health) * bar_width)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))

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

    def take_damage(self, amount):
        """Take damage with cooldown"""
        if self.is_dying or not self.is_alive or self.damage_timer > 0:
            return

        self.health -= amount
        self.damage_timer = self.damage_cooldown

        if self.health <= 0:
            self.health = 0
            self.is_dying = True
            self.death_frame = 0
            self.animation_counter = 0
