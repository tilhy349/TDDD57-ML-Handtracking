import mediapipe as mp
import pygame
import math
from settings import *

class Player:

    def __init__(self):
        self.hitbox = pygame.Rect(0, 0, PLAYER_WIDTH - 14, PLAYER_HEIGHT - 14)

        self.start_pos = pygame.Vector2(0.0, 0.0)
        self.end_pos = pygame.Vector2(0.0, 0.0)
        self.curr_pos = pygame.Vector2(400.0, 300.0)
        self.moving_dir = pygame.Vector2(0.0, 0.0)

        self.player_image = PlayerImage.DEFAULT
    
    def draw_player(self, surface):
        image = IMAGE_PLAYER_DEFAULT
        
        #Dino going to the left
        if self.moving_dir.x < 0:
            if self.player_image == PlayerImage.CLOSE:
                image = IMAGE_PLAYER_CLOSE_MIRROR
            elif self.player_image == PlayerImage.PEACE:
                image = IMAGE_PLAYER_PEACE_MIRROR
            else:
                image = IMAGE_PLAYER_DEFAULT_MIRROR
        #Dino going to the right
        else:
            if self.player_image == PlayerImage.CLOSE:
                image = IMAGE_PLAYER_CLOSE
            elif self.player_image == PlayerImage.PEACE:
                image = IMAGE_PLAYER_PEACE
            else:
                image = IMAGE_PLAYER_DEFAULT
            
        surface.blit(image, self.curr_pos)

    #Update the direction which the player is moving towards
    #This is called each time the timer passes a delay value
    def update_moving_dir(self, end_point):
        self.end_pos = pygame.Vector2(end_point[0], end_point[1])
        self.start_pos = pygame.Vector2(self.curr_pos)
        self.moving_dir = self.end_pos - self.start_pos
        
        if self.moving_dir.length() > 0:
            self.moving_dir.normalize_ip() 
     
    #Update player position
    def move_player(self, dt):
        #Calculate the new position
        pos = PLAYER_VELOCITY * dt        

        displacement = self.moving_dir * pos #PLAYER_VELOCITY 
        vec = self.end_pos - self.curr_pos

        #Is the displacement longer than the distance left to end_pos
        if displacement.length() < vec.length():
            self.curr_pos = self.curr_pos + displacement
        else:
            self.curr_pos = self.end_pos
        
        #BOUNDARIES
        if self.curr_pos.y < PLAYER_LIMIT_UP:
            self.curr_pos.y = PLAYER_LIMIT_UP
        elif self.curr_pos.y > PLAYER_LIMIT_DOWN:
            self.curr_pos.y = PLAYER_LIMIT_DOWN
        if self.curr_pos.x > SCREEN_WIDTH - GAME_DISPLACEMENT - PLAYER_WIDTH:
            self.curr_pos.x = SCREEN_WIDTH - GAME_DISPLACEMENT - PLAYER_WIDTH
        elif self.curr_pos.x < GAME_DISPLACEMENT:
            self.curr_pos.x = GAME_DISPLACEMENT
        
        self.hitbox.update(self.curr_pos.x + 7, self.curr_pos.y + 7,  PLAYER_WIDTH - 14, PLAYER_HEIGHT - 14)
       
    