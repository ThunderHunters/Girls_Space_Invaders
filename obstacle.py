# obstacle

import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self,size,color,x,y):

        # Call the superclass constructor
        super().__init__()

        # Create a white surface with the specified size
        self.image = pygame.Surface((size, size))

        # Fill the surface with a white color; the 'color' parameter is not used
        self.image.fill((255, 255, 255))
        
        # Get the rect (rectangle) object representing the position and size of the block
        self.rect = self.image.get_rect(topleft=(x, y))
        
# Define a shape pattern for the obstacle using a list of strings

shape = [
'xx       xx',
' xx    xx  ',
'  xx  xx   ',
'xxxxxxxxxx',
'  xx  xx   ',
' xx     xx ',
'xx       xx'
]   

