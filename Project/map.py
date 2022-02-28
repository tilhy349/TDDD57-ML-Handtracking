from turtle import pos
import pygame
import random
from settings import *
from abc import ABC, abstractmethod

class DrawableObject(ABC):
    def __init__(self, pos):
        self.pos = pos
    
    @abstractmethod
    def draw(self, surface):
        pass

    def update_pos(self):
        self.pos = pygame.Vector2(self.pos.x, self.pos.y + MAP_SPEED)

class Coin (DrawableObject):
    def __init__(self, pos):
        DrawableObject.__init__(self, pos)
    
    def draw(self, surface):
        #print("Drawing coin")
        pygame.draw.rect(surface, (250, 250, 0), pygame.Rect(self.pos.x, self.pos.y, MAP_BLOCK_WIDTH, MAP_BLOCK_HEIGHT))

class Block (DrawableObject):
    def __init__(self, pos):
        DrawableObject.__init__(self, pos)
    
    def draw(self, surface):
        #print("Drawing box")
        pygame.draw.rect(surface, (200, 0, 30), pygame.Rect(self.pos.x, self.pos.y, MAP_BLOCK_WIDTH, MAP_BLOCK_HEIGHT))


class Map:
    def __init__(self):
        self.objects = []
        self.createRow()  

    def createRow(self):
        #Spawn rate, spawn or not? what to spawwn?
        
        for i in range(0, SCREEN_WIDTH, MAP_BLOCK_WIDTH):
            rand = random.uniform(0, 1)

            #If an object should spawn or not
            if rand < SPAWN_RATE_OBJECT:
                rand = random.uniform(0, 1)
                #If the object should be a block or coin
                if rand < SPAWN_RATE_BLOCK:
                    self.objects.append(Block(pygame.Vector2(i, 0)))
                else:
                    self.objects.append(Coin(pygame.Vector2(i, 0)))
    
    def move_objects(self):
        
        for i in self.objects:
            i.update_pos()
      

    def draw(self, surface):  
        #Draw borders
        for i in range(0, SCREEN_WIDTH, MAP_BLOCK_WIDTH):
            pygame.draw.line(surface, (0,0,200), (i,0), (i,SCREEN_HEIGHT))

        #Draw all objects in list
        for i in self.objects:
            i.draw(surface)

        