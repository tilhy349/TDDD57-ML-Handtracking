import mediapipe as mp
import pygame
import math
from settings import *

class Player:

    def __init__(self):
        self.width = 10
        self.height = 10
        self.hitbox = pygame.Rect(0, 0, self.width, self.height)
        
        self.velocity = 10 #moving velocity

        self.curr_lerp = 0.0 #Current lerp
        self.start_pos = pygame.Vector2(0.0, 0.0)
        self.end_pos = pygame.Vector2(0.0, 0.0)
        self.curr_pos = pygame.Vector2(400.0, 300.0)
        self.moving_dir = pygame.Vector2(0.0, 0.0)
    
    def draw_player(self, surface):
        pygame.draw.rect(surface, (255,0,0), self.hitbox)

    #Update the direction which the palyer is moving towards
    #This is called each time the timer passes a delay value
    def update_moving_dir(self, end_point):
        self.end_pos = pygame.Vector2(end_point[0], end_point[1])
        self.start_pos = pygame.Vector2(self.curr_pos)
        self.moving_dir = self.end_pos - self.start_pos
        
        if self.moving_dir.length() > 0:
            self.moving_dir.normalize_ip()
     
    #Update player position
    def move_player(self):
        #Calculate the new position

        displacement = self.moving_dir * self.velocity
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
        if self.curr_pos.x > SCREEN_WIDTH - 20:
            self.curr_pos.x = SCREEN_WIDTH - 20
        elif self.curr_pos.x < 10:
            self.curr_pos.x = 10
        
        self.hitbox.update(self.curr_pos.x, self.curr_pos.y, self.width, self.height)
       
    