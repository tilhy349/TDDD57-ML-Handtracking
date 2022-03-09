from turtle import pos
import pygame
import random
from settings import *
from abc import ABC, abstractmethod

class DrawableObject(ABC):
    def __init__(self, pos, image):
        self.pos = pos
        self.hitbox = pygame.Rect(self.pos.x, self.pos.y, MAP_BLOCK_WIDTH, MAP_BLOCK_HEIGHT)
        self.image = image
        
    @abstractmethod
    def draw(self, surface):
        pass

    @abstractmethod
    def update_pos(self, pos):
        pass

class Coin (DrawableObject):
    def __init__(self, pos, image):
        DrawableObject.__init__(self, pos, image)
        
    def draw(self, surface):
        surface.blit(self.image, self.pos)
        #pygame.draw.rect(surface, (250, 250, 0), self.hitbox)

    def update_pos(self, pos):
        self.pos = pygame.Vector2(self.pos.x, self.pos.y + pos)
        self.hitbox.update(self.pos.x, self.pos.y, IMAGE_COIN.get_width(), IMAGE_COIN.get_height())

class Block (DrawableObject):
    def __init__(self, pos, image):
        DrawableObject.__init__(self, pos, image)
        
    def draw(self, surface):
        surface.blit(self.image, self.pos)
        #pygame.draw.rect(surface, (155, 103, 60), self.hitbox)
    
    def update_pos(self, pos):
        border = 7
        self.pos = pygame.Vector2(self.pos.x, self.pos.y + pos)
        self.hitbox.update(self.pos.x + border, self.pos.y + border, MAP_BLOCK_WIDTH - border * 2, MAP_BLOCK_HEIGHT - border * 2)


class Map:
    def __init__(self):
        self.objects = []  
        self.n_coins = 0
        self.total_distance = 0
        
        self.block_movement = 0

        self.clouds_pos_1 = pygame.Vector2(GAME_DISPLACEMENT,-IMAGE_CLOUDS_HEIGHT + SCREEN_HEIGHT)
        self.clouds_pos_2 = pygame.Vector2(GAME_DISPLACEMENT,-IMAGE_CLOUDS_HEIGHT * 2 + SCREEN_HEIGHT)

    def createRow(self):
        #Spawn rate, spawn or not? what to spawn?
        
        for i in range(GAME_DISPLACEMENT, GAME_DISPLACEMENT + GAME_WIDTH, MAP_BLOCK_WIDTH):
            rand = random.uniform(0, 1)

            #If an object should spawn or not
            if rand < SPAWN_RATE_OBJECT:
                rand = random.uniform(0, 1)
                #If the object should be a block or coin
                if rand < SPAWN_RATE_BLOCK:
                    self.objects.append(Block(pygame.Vector2(i, -MAP_BLOCK_HEIGHT - 10), self.random_image()))
                else:
                    self.objects.append(Coin(pygame.Vector2(i + IMAGE_COIN.get_width() / 2, -MAP_BLOCK_HEIGHT - 10), IMAGE_COIN))
    
    def random_image(self):
        rand = random.uniform(0, 1)
        if rand < 1/3:
            return IMAGE_BLOCK1
        elif rand > 2/3:
            return IMAGE_BLOCK2
        else:
            return IMAGE_BLOCK3
        
        
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
        #Move clouds
        self.clouds_pos_1 += pygame.Vector2(0, pos * 0.2)
        self.clouds_pos_2 += pygame.Vector2(0, pos * 0.2)

        #If the bottom image reaches the bottom of the screen, then move it above the other one
        if self.clouds_pos_1.y > SCREEN_HEIGHT:
            self.clouds_pos_1 = pygame.Vector2(GAME_DISPLACEMENT,-IMAGE_CLOUDS_HEIGHT * 2 + SCREEN_HEIGHT)
        elif self.clouds_pos_2.y > SCREEN_HEIGHT:
            self.clouds_pos_2 = pygame.Vector2(GAME_DISPLACEMENT,-IMAGE_CLOUDS_HEIGHT * 2 + SCREEN_HEIGHT)

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

        surface.blit(IMAGE_BACKGROUND, [0,0])

        #Blit the cloud images that is visible on screen
        if self.clouds_pos_1.y > -IMAGE_CLOUDS_HEIGHT:
            surface.blit(IMAGE_CLOUDS, self.clouds_pos_1)
        if self.clouds_pos_2.y > -IMAGE_CLOUDS_HEIGHT:
            surface.blit(IMAGE_CLOUDS_MIRROR, self.clouds_pos_2)

        #pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(0, 0, GAME_DISPLACEMENT, SCREEN_HEIGHT), 1)
        #pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(SCREEN_WIDTH - GAME_DISPLACEMENT, 0, GAME_DISPLACEMENT, SCREEN_HEIGHT), 1)

        #Draw all objects in list
        for i in self.objects:
            i.draw(surface)

        