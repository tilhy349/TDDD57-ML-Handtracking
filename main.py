import cv2
import os
import mediapipe as mp
import pygame 
import sys
from game import Game
from settings import *

# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

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


def user_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            
            elif event.key == pygame.K_1:
                #RESET
                reset = True
        
        

#START OF MAIN-LOOP
    
# Variable to keep the main loop running
running = True

game = Game(screen)


while True:
    
    #Buttons
    user_events()

    #Update game, draw on screen
    game.update()
    
#END OF MAIN   

