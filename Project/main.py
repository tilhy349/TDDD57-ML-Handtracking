import pygame 
import sys
from game import Game
from settings import *

#Create events
update_player_movement = pygame.USEREVENT + 1
spawn_new_row = pygame.USEREVENT + 2
move_map_objects = pygame.USEREVENT + 3
update_map_speed = pygame.USEREVENT + 4

# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

#Set timers
pygame.time.set_timer(update_player_movement, DELAY)
pygame.time.set_timer(update_map_speed, GAME_SPEED_UPDATE)

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

game = Game(screen)

def user_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            
        if event.type == update_player_movement:
            #Call function in game
            game.update_player_movement()  

        if (event.type == update_map_speed and game.game_state == State.RUNNING 
            and game.powerup.current_powerup == Powerup.SLOWMOTION):
            game.game_speed += SPEED_UPDATE_STEP
    

#START OF MAIN-LOOP

#Profiling
# import cProfile, pstats

# profiler = cProfile.Profile()
# profiler.enable()
# for i in range(10):
#     game.update()
# profiler.disable()
# stats = pstats.Stats(profiler).sort_stats('ncalls')
# stats.strip_dirs()
# #stats.dump_stats('export-data.txt')
# stats.print_stats()#

while True: 
    
    #Events
    user_events()

    #Update game, draw on screen
    game.update()
   
#END OF MAIN   
