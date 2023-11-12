# Laser

import pygame

class Laser(pygame.sprite.Sprite):

    # Constructor method, initializes the laser object
    def __init__(self,pos,speed,screen_height,color=(255, 0, 193)):

        # Call the superclass constructor
        super().__init__()


        # Create a surface for the laser 
        self.image = pygame.Surface((8,30))

        # Fill the laser surface with the specified color
        self.image.fill((color))

        # Retrieve the rectangle object that represents the laser's position and size.
        self.rect = self.image.get_rect(center = pos)

        # Set the speed of the laser
        self.speed = speed

        # Set the height constraint for the laser
        self.height_y_constraint = screen_height

    # Method to destroy the laser if it goes beyond specified y-coordinate limits
    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    # Method to update the position of the laser
    def update(self):
        self.rect.y += self.speed

        # Call the destroy method to check if the laser needs to be removed
        self.destroy()
       
        
