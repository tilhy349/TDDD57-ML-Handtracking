import cv2
import os
import mediapipe as mp
import pygame 
import sys
from game import Game
from settings import *

#Create events
update_player_movement = pygame.USEREVENT + 1
spawn_new_row = pygame.USEREVENT + 2
move_map_objects = pygame.USEREVENT + 3

# Initialize pygame
pygame.init()

pygame.font.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.time.set_timer(update_player_movement, DELAY)
pygame.time.set_timer(spawn_new_row, SPAWN_RATE_ROW)
pygame.time.set_timer(move_map_objects, MAP_UPDATE_SPEED)

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

        if event.type == spawn_new_row and game.game_state == State.RUNNING:
            game.map.createRow()
            game.total_distance += MAP_SPEED
        
        if event.type == move_map_objects and game.game_state == State.RUNNING:
            game.map.move_objects()
            

#START OF MAIN-LOOP

while True: 
    
    #Buttons
    user_events()

    #Update game, draw on screen
    game.update()

    #screen.fill((255,255,255))

    #textsurface = myfont.render('Some Text', False, (255, 255, 0))
   
    
#END OF MAIN   
