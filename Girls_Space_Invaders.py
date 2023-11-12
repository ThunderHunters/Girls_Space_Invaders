# Girls Space Invaders

import pygame
import sys
from player import Player
from laser import Laser
import obstacle
from alien import Alien, Extra
from random import choice, randint

pygame.init()

class Game:
    def __init__(self):

        # Add flags to track game state
        self.game_over = False  
        self.game_running = True  

        # player setup
        player_sprite = Player((screen_width / 2, screen_height - 30), screen_width, 5, screen)

        self.player = pygame.sprite.GroupSingle()
        self.player.add(player_sprite)
        
        # health and score setup ## Here you will need to change the file path to your unique folder on your computer where you downloaded the files.##
        # REPLACE XXX WITH YOUR FILE PATH # 
        self.lives = 3
        self.live_surf = pygame.image.load("XXX/player.png").convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[1] * 6 + 10)
        self.score = 0 
        ## Here you will need to change the file path to your unique folder on your computer where you downloaded the files.##
        # REPLACE XXX WITH YOUR FILE PATH # 
        self.font = pygame.font.Font("XXX/Bradley Hand Bold.ttf",50)

        # obstacle setup
        self.shape = obstacle.shape
        self.block_size = 3
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 5
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = screen_width / 15, y_start = 480)

        # alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows = 6, cols = 6)
        self.alien_direction = 1

        # extra setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(2,20)

        # audio ## Here you will need to change the file path to your unique folder on your computer where you downloaded the files.##
        # REPLACE XXX WITH YOUR FILE PATH # 
        music = pygame.mixer.Sound("XXX/CD-349321485-TRACK22-1.wav")
        music.set_volume(0.1)
        music.play(loops = -1)
        self.laser_sound = pygame.mixer.Sound("XXX/laser2.WAV")
        self.laser_sound.set_volume(0.1)
        self.explosion_sound = pygame.mixer.Sound("XXX/explosion2.wav")
        self.explosion_sound.set_volume(0.2)
        self.extra_sound = pygame.mixer.Sound("XXX/bgg.wav")
        self.extra_sound.set_volume(0.2)
        
    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index,col in enumerate(row):
                if col == "x":
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size,(241,79,80),x,y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset_x, x_start, y_start):
        for offset_x in offset_x:
            self.create_obstacle(x_start,y_start,offset_x)

    def alien_setup(self, rows, cols, x_distance = 60, y_distance = 48, x_offset = 70, y_offset = 100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0: alien_sprite = Alien("red",x,y)
                elif 1 <= row_index <= 2: alien_sprite = Alien("green",x,y)
                else: alien_sprite = Alien("yellow",x,y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self,distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            alien_laser_sprite = Laser(random_alien.rect.center, 6, screen_height, color=(255, 0, 0))
            self.alien_lasers.add(alien_laser_sprite)
            self.laser_sound.play()

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(["right","left"]),screen_width))
            self.extra_spawn_time = randint(300,600)

    def collision_checks(self):
        # player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()

                # alien jelly collisions
                aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()  
                    self.explosion_sound.play() 
                                        
                # extra collisions
                if pygame.sprite.spritecollide(laser,self.extra,True):
                    self.score += 500
                    laser.kill()
                    self.extra_sound.play()
        
        # jelly lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()

                if pygame.sprite.spritecollide(laser,self.player,False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        self.done_message()

        # jellyfish
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien,self.blocks,True)
                
                if pygame.sprite.spritecollide(alien,self.player,False):
                    self.done_message()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf,(x,10))

    def display_score(self):
        score_surf = self.font.render(f'SCORE: {self.score}',False,"yellow")
        score_rect = score_surf.get_rect(topleft = (20, 16))
        screen.blit(score_surf,score_rect)

    def done_message(self):
        if self.lives <= 0:
            self.game_over = True  # Set the game_over flag
            screen.fill((0, 0, 0))  # Fill the screen with a background color
            done_surf = self.font.render(" You Lose! Try Again!",False,"white")
            done_rect = done_surf.get_rect(center = (screen_width / 2, screen_height / 2))
            screen.blit(done_surf,done_rect)  
            self.game_running = False  # Set the game_running flag to False  

    def victory_message(self):
        if not self.aliens.sprites():
            victory_surf = self.font.render(" You Won! ",False,"white")
            victory_rect = victory_surf.get_rect(center = (screen_width / 2, screen_height / 2))
            screen.blit(victory_surf,victory_rect)
            self.game_over = True  # Set the game_over flag
            self.game_running = False  # Set the game_running flag to False 

    def run(self):
        if not self.game_over:

            self.player.update()
            self.alien_lasers.update()
            self.extra.update()
        
            self.aliens.update(self.alien_direction)
            self.alien_position_checker()
            self.extra_alien_timer()
            self.collision_checks()
    
            self.player.sprite.lasers.draw(screen)
            self.player.draw(screen)
            self.blocks.draw(screen)
            self.aliens.draw(screen)
            self.alien_lasers.draw(screen)
            self.extra.draw(screen)

            self.display_lives()
            self.display_score()
            self.victory_message()

        if pygame.display.get_init():
            self.done_message()

class CRT:
    def __init__(self):
        ## Here you will need to change the file path to your unique folder on your computer where you downloaded the files.##
        # REPLACE XXX WITH YOUR FILE PATH # 
        self.tv = pygame.image.load("XXX/tv.png").convert_alpha()
        self.tv = pygame.transform.scale(self.tv,(screen_width, screen_height))

    def create_crt_lines(self):
        line_height = 2
        line_amount = int(screen_height / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, "white",(0,y_pos),(screen_width,y_pos),1)
    
    def draw(self):
        self.tv.set_alpha(randint(65,75))
        self.create_crt_lines()
        screen.blit(self.tv,(0,0))
        
if __name__ == "__main__":

    screen_width = 650
    screen_height = 650
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Girls Space Invaders")
    clock = pygame.time.Clock()
    game = Game()
    crt = CRT()

    # Define colors
    hot_pink = (255, 0, 193)  # RGB values for hot pink
   
    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER,800)
  
    # Timer to change player color every 5 seconds
    COLOR_CHANGE_EVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(COLOR_CHANGE_EVENT, 5000)

    player_sprite = Player((screen_width / 2, screen_height - 30), screen_width, 5, screen)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Set the running variable to False
            elif event.type == ALIENLASER:
                game.alien_shoot()
         
        screen.fill((30,30,30)) 

    # Draw the hot pink border
        pygame.draw.rect(screen, hot_pink, (0, 0, screen_width, screen_height), 3)  # Adjust the border thickness as needed
        game.run()
        crt.draw()

        pygame.display.flip()
        clock.tick(60)

        if game.game_over:
            running = False  # Set running to False to stop the game logic      
                        
# Wait for 3 seconds before quitting
pygame.time.delay(3000)            
pygame.quit()




