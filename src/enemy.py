import pygame
import os
import math


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1.5
        self.scale = 2

        # State
        self.state = "idle"  # idle, walk, attack, dying
        self.facing_left = False
        self.frame = 0
        self.animation_speed = 0.15
        self.animation_counter = 0
        self.is_dying = False

        # Combat
        self.attack_range = 80
        self.attack_cooldown = 2.0  # seconds
        self.attack_timer = 0
        self.is_attacking = False
        self.post_attack_idle_duration = 1.5  # seconds to idle after attack
        self.post_attack_idle_timer = 0

        # Health
        self.health = 100
        self.max_health = 100
        self.is_alive = True

        # Load sprite sheets
        base_path = os.path.join("assets", "images", "dragon-lord")

        # Idle: 4 frames, 74x74
        self.idle_sheet = pygame.image.load(
            os.path.join(base_path, "dragon_lord_idle_basic_74x74.png")
        ).convert_alpha()
        self.idle_frame_width = 74
        self.idle_frame_height = 74
        self.idle_frames = 4

        # Walk: 8 frames, 74x74
        self.walk_sheet = pygame.image.load(
            os.path.join(base_path, "dragon_lord_walk_basic_74x74.png")
        ).convert_alpha()
        self.walk_frame_width = 74
        self.walk_frame_height = 74
        self.walk_frames = 8

        # Attack: 16 frames, 90x70
        self.attack_sheet = pygame.image.load(
            os.path.join(base_path, "dragon_lord_attack_arms_90x70.png")
        ).convert_alpha()
        self.attack_frame_width = 90
        self.attack_frame_height = 70
        self.attack_frames = 16

        # Death: 36 frames, 160x160
        self.death_sheet = pygame.image.load(
            os.path.join(base_path, "dragon_lord_death_160x160.png")
        ).convert_alpha()
        self.death_frame_width = 160
        self.death_frame_height = 160
        self.death_frames = 36

        # Current sprite
        self.current_sprite = self.get_sprite("idle", 0)

    def get_sprite(self, state, frame):
        """Extract and scale a sprite from the appropriate sheet"""
        if state == "idle":
            sheet = self.idle_sheet
            width = self.idle_frame_width
            height = self.idle_frame_height
        elif state == "walk":
            sheet = self.walk_sheet
            width = self.walk_frame_width
            height = self.walk_frame_height
        elif state == "attack":
            sheet = self.attack_sheet
            width = self.attack_frame_width
            height = self.attack_frame_height
        elif state == "dying":
            sheet = self.death_sheet
            width = self.death_frame_width
            height = self.death_frame_height
        else:
            return self.current_sprite

        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(sheet, (0, 0), (frame * width, 0, width, height))

        # Scale sprite
        scaled = pygame.transform.scale(
            sprite, (int(width * self.scale), int(height * self.scale))
        )

        # Flip if facing left
        if self.facing_left:
            scaled = pygame.transform.flip(scaled, True, False)

        return scaled

    def get_distance_to(self, target_x, target_y):
        """Calculate distance to a point"""
        dx = target_x - self.x
        dy = target_y - self.y
        return math.sqrt(dx * dx + dy * dy)

    def update(self, player, dt):
        """Update enemy AI and animation"""
        # Handle death animation
        if self.is_dying:
            self.state = "dying"
            self.animation_counter += self.animation_speed * 0.8
            if self.animation_counter >= 1:
                self.animation_counter = 0
                self.frame += 1

                if self.frame >= self.death_frames:
                    self.is_alive = False
                    return

            self.current_sprite = self.get_sprite(self.state, self.frame)
            return

        if not self.is_alive:
            return

        # Update attack cooldown timer
        if self.attack_timer > 0:
            self.attack_timer -= dt

        # Update post-attack idle timer
        if self.post_attack_idle_timer > 0:
            self.post_attack_idle_timer -= dt

        # Get distance to player
        player_center_x = player.x + player.display_size // 2
        player_center_y = player.y + player.display_size // 2
        my_center_x = self.x + (self.idle_frame_width * self.scale) // 2
        my_center_y = self.y + (self.idle_frame_height * self.scale) // 2

        distance = self.get_distance_to(player_center_x, player_center_y)

        # If player is dead, move away from corpse
        if not player.is_alive:
            if distance < 150:  # Move away if within 150 pixels
                self.state = "walk"

                # Calculate direction away from player
                dx = my_center_x - player_center_x
                dy = my_center_y - player_center_y
                distance = max(distance, 0.001)

                # Normalize and apply speed
                dx = (dx / distance) * self.speed
                dy = (dy / distance) * self.speed

                # Update position
                self.x += dx
                self.y += dy

                # Update facing direction
                if dx < 0:
                    self.facing_left = True
                else:
                    self.facing_left = False

                # Update animation
                self.animation_counter += self.animation_speed
                if self.animation_counter >= 1:
                    self.animation_counter = 0
                    self.frame = (self.frame + 1) % self.walk_frames
            else:
                # Idle when far enough away
                self.state = "idle"
                self.animation_counter += self.animation_speed
                if self.animation_counter >= 1:
                    self.animation_counter = 0
                    self.frame = (self.frame + 1) % self.idle_frames

            self.current_sprite = self.get_sprite(self.state, self.frame)
            return

        # Update facing direction
        if player_center_x < my_center_x:
            self.facing_left = True
        else:
            self.facing_left = False

        # State machine
        if self.is_attacking:
            # Continue attack animation
            self.state = "attack"
            self.animation_counter += self.animation_speed
            if self.animation_counter >= 1:
                self.animation_counter = 0
                self.frame += 1

                if self.frame >= self.attack_frames:
                    self.is_attacking = False
                    self.frame = 0
                    self.attack_timer = self.attack_cooldown
                    self.post_attack_idle_timer = self.post_attack_idle_duration

        elif self.post_attack_idle_timer > 0:
            # Post-attack idle state - don't move, just play idle animation
            self.state = "idle"
            self.animation_counter += self.animation_speed
            if self.animation_counter >= 1:
                self.animation_counter = 0
                self.frame = (self.frame + 1) % self.idle_frames

        elif distance <= self.attack_range and self.attack_timer <= 0:
            # Start attack
            self.is_attacking = True
            self.state = "attack"
            self.frame = 0
            self.animation_counter = 0

        elif distance > self.attack_range:
            # Move towards player
            self.state = "walk"

            # Calculate direction
            dx = player_center_x - my_center_x
            dy = player_center_y - my_center_y
            distance = max(distance, 0.001)  # Avoid division by zero

            # Normalize and apply speed
            dx = (dx / distance) * self.speed
            dy = (dy / distance) * self.speed

            # Update position
            self.x += dx
            self.y += dy

            # Update animation
            self.animation_counter += self.animation_speed
            if self.animation_counter >= 1:
                self.animation_counter = 0
                self.frame = (self.frame + 1) % self.walk_frames

        else:
            # Idle
            self.state = "idle"
            self.animation_counter += self.animation_speed
            if self.animation_counter >= 1:
                self.animation_counter = 0
                self.frame = (self.frame + 1) % self.idle_frames

        # Get current sprite
        self.current_sprite = self.get_sprite(self.state, self.frame)

    def draw(self, screen):
        """Draw the enemy on screen"""
        if self.is_alive or self.is_dying:
            # Calculate draw position
            draw_x = int(self.x)
            draw_y = int(self.y)

            # Adjust position for death animation to keep enemy centered
            if self.is_dying:
                # Death sprite is 160x160, normal is 74x74
                # Center the larger death sprite on the enemy's position
                normal_width = self.idle_frame_width * self.scale
                normal_height = self.idle_frame_height * self.scale
                death_width = self.death_frame_width * self.scale
                death_height = self.death_frame_height * self.scale

                draw_x = int(self.x - (death_width - normal_width) // 2)
                draw_y = int(self.y - (death_height - normal_height))

            screen.blit(self.current_sprite, (draw_x, draw_y))

            # Draw health bar (only if not dying)
            if not self.is_dying:
                self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        """Draw health bar above enemy"""
        bar_width = 60
        bar_height = 5
        bar_x = int(self.x + (self.idle_frame_width * self.scale - bar_width) // 2)
        bar_y = int(self.y - 10)

        # Background (red)
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # Health (green)
        health_width = int((self.health / self.max_health) * bar_width)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))

    def get_rect(self):
        """Get enemy rect for collision detection"""
        return pygame.Rect(
            self.x, self.y,
            self.idle_frame_width // 2 * self.scale,
            self.idle_frame_height // 2 * self.scale
        )

    def take_damage(self, amount):
        """Reduce enemy health"""
        if self.is_dying or not self.is_alive:
            return

        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.is_dying = True
            self.frame = 0
            self.animation_counter = 0
