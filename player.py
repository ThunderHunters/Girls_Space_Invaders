# player

import pygame
from laser import Laser
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed, screen):
        super().__init__()

        # Load player image  ## Here you will need to change the file path to your unique folder on your computer where you downloaded the files.##
        # REPLACE XXX WITH YOUR FILE PATH # 
        self.image = pygame.image.load("XXX/player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)  # Set the initial position of the player
        self.speed = speed  # Set the speed of the player
        self.max_x_constraint = constraint  # Set the maximum x constraint for the player
        self.ready = True  # Flag to check if the player is ready to shoot
        self.laser_time = 0  # Time when the last laser was shot
        self.laser_cooldown = 200  # Cooldown time between shots

        self.lasers = pygame.sprite.Group()  # Group to store player's lasers

        ## Here you will need to change the file path to your unique folder on your computer where you downloaded the files.##
        # REPLACE XXX WITH YOUR FILE PATH # 
        self.laser_sound = pygame.mixer.Sound("XXX/Player Laser.wav")
        self.laser_sound.set_volume(0.1)  # Set the volume of the laser sound effect

    # Check for keyboard input
    def get_input(self):
        
        keys = pygame.key.get_pressed()

        # Move player based on input
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        # Shoot laser if space is pressed and the player is ready
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            self.laser_sound.play()

    # Check if the player is ready to shoot again
    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    # Keep the player within the screen boundaries
    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    # Add a new laser to the group
    def shoot_laser(self):
        
        self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom))

    # Update player based on user input and constraints
    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()  # Update the position of player's lasers
