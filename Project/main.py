import cv2
import os
import mediapipe as mp
import pygame 
import sys
from game import Game
#from settings import *

#Create events
update_player_movement = pygame.USEREVENT + 1

# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((800, 800), 0, 32)

pygame.time.set_timer(update_player_movement, 500)

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

#START OF MAIN-LOOP

while True: 
    
    #Buttons
    user_events()

    #Update game, draw on screen
    game.update()
    
#END OF MAIN   
