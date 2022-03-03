from turtle import pos
import pygame
import random
from settings import *
from abc import ABC, abstractmethod

class DrawableObject(ABC):
    def __init__(self, pos):
        self.pos = pos
        self.hitbox = pygame.Rect(self.pos.x, self.pos.y, MAP_BLOCK_WIDTH, MAP_BLOCK_HEIGHT)
        
    @abstractmethod
    def draw(self, surface):
        pass

    def update_pos(self, pos):
        self.pos = pygame.Vector2(self.pos.x, self.pos.y + pos)
        self.hitbox.update(self.pos.x, self.pos.y, MAP_BLOCK_WIDTH, MAP_BLOCK_HEIGHT)

class Coin (DrawableObject):
    def __init__(self, pos):
        DrawableObject.__init__(self, pos)
    
    def draw(self, surface):
        #print("Drawing coin")
        pygame.draw.rect(surface, (250, 250, 0), self.hitbox)

class Block (DrawableObject):
    def __init__(self, pos):
        DrawableObject.__init__(self, pos)
    
    def draw(self, surface):
        #print("Drawing box")
        pygame.draw.rect(surface, (155, 103, 60), self.hitbox)


class Map:
    def __init__(self):
        self.objects = []  
        self.n_coins = 0
        self.total_distance = 0
        
        self.block_movement = 0

    def createRow(self):
        #Spawn rate, spawn or not? what to spawn?
        
        for i in range(0, SCREEN_WIDTH, MAP_BLOCK_WIDTH):
            rand = random.uniform(0, 1)

            #If an object should spawn or not
            if rand < SPAWN_RATE_OBJECT:
                rand = random.uniform(0, 1)
                #If the object should be a block or coin
                if rand < SPAWN_RATE_BLOCK:
                    self.objects.append(Block(pygame.Vector2(i, -MAP_BLOCK_HEIGHT - 10)))
                else:
                    self.objects.append(Coin(pygame.Vector2(i, -MAP_BLOCK_HEIGHT - 10)))
    
    
    def update_map_movement(self, game_speed, dt):
        
        pos = game_speed * dt
        self.block_movement += pos
        self.total_distance += pos

        #Move objects down
        self.move_objects(pos)

        #Spawn new row if there is enough space
        if self.block_movement >= 2 * MAP_BLOCK_HEIGHT:
            self.block_movement = 0
            self.createRow()
    
    
    def move_objects(self, pos):
        #Update position for each object
        for i in self.objects:
            i.update_pos(pos)
            
            #If object is out of bounds, remove object
            if i.pos.y > SCREEN_HEIGHT: 
                self.objects.remove(i)
    
    def block_collision(self, player_hitbox, invisible):
        
        #Check collision between all blocks and player hitbox
        for i in self.objects:
            if not invisible and isinstance(i, Block) and i.hitbox.colliderect(player_hitbox):
                return True
            elif isinstance(i, Coin) and i.hitbox.colliderect(player_hitbox):
                self.n_coins += 1
                self.objects.remove(i)

        return False
        

    def draw(self, surface):  
        #Draw borders
        #for i in range(0, SCREEN_WIDTH, MAP_BLOCK_WIDTH):
            #pygame.draw.line(surface, (0,0,200), (i,0), (i,SCREEN_HEIGHT))

        #Draw all objects in list
        for i in self.objects:
            i.draw(surface)

        