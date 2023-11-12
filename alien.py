# alien

import pygame

class Alien(pygame.sprite.Sprite):

    def __init__(self,color,x,y):

        super().__init__()

        # Construct the file path based on the provided color ## Here you will need to change the file path to your unique folder on your computer where you downloaded the files.##
        # REPLACE XXX WITH YOUR FILE PATH # 
        file_path = "XXX" + color + ".png"

        # Load the jellyfish image with transparency
        self.image = pygame.image.load(file_path).convert_alpha()

        # Set the initial position of the jellyfish
        self.rect = self.image.get_rect(topleft = (x,y))

        # Assign a point value based on the color
        if color == "yellow" : self.value = 100
        elif color  == "green" : self.value = 200
        else: self.value = 300


    # Method to update the position of the jellyfish based on the provided direction
    def update(self,direction):
        self.rect.x += direction

# Crab
class Extra(pygame.sprite.Sprite):

    def __init__(self,side,screen_width):

        super().__init__()

        # Load the extra crab image with transparency   ## Here you will need to change the file path to your unique folder on your computer where you downloaded the files.##
        # REPLACE XXX WITH YOUR FILE PATH # 
        self.image = pygame.image.load("XXX/extra.png").convert_alpha()

        # Set the initial position and speed based on the provided side
        if side == "right":
            x = screen_width + 40
            self.speed = - 3
        else:
            x = -50
            self.speed = 3

        self.rect = self.image.get_rect(topleft = (x,50))

    # Method to update the position of the extra crab
    def update(self):
        self.rect.x += self.speed
