import pygame
import random
from settings import *
from drawable_object import Coin, Block

CLOUDS_HEIGHT = 1400

class Map:
    def __init__(self):
        self.objects = []  
        self.n_coins = 0
        self.total_distance = 0
        
        self.block_movement = 0

        self.clouds_pos_1 = pygame.Vector2(GAME_DISPLACEMENT,-CLOUDS_HEIGHT + SCREEN_HEIGHT)
        self.clouds_pos_2 = pygame.Vector2(GAME_DISPLACEMENT,-CLOUDS_HEIGHT * 2 + SCREEN_HEIGHT)

        self.IMAGE_BACKGROUND = pygame.transform.scale(pygame.image.load("Project\Images\Background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
        self.IMAGE_CLOUDS = pygame.transform.scale(pygame.image.load("Project\Images\Clouds.png"), (GAME_WIDTH - 2, CLOUDS_HEIGHT)).convert_alpha()
        self.IMAGE_CLOUDS_MIRROR = pygame.transform.scale(pygame.image.load("Project\Images\Clouds_mirrored.png"), (GAME_WIDTH - 2, CLOUDS_HEIGHT)).convert_alpha()

        self.IMAGE_BLOCK = [pygame.transform.scale( pygame.image.load("Project\Images\Block1.png"), (MAP_BLOCK_WIDTH, MAP_BLOCK_HEIGHT)).convert(),
                            pygame.transform.scale( pygame.image.load("Project\Images\Block2.png"), (MAP_BLOCK_WIDTH, MAP_BLOCK_HEIGHT)).convert(),
                            pygame.transform.scale( pygame.image.load("Project\Images\Block3.png"), (MAP_BLOCK_WIDTH, MAP_BLOCK_HEIGHT)).convert()]

        self.IMAGE_COIN_DEFAULT = pygame.transform.scale( pygame.image.load("Project\Images\Coin_1.png"), (MAP_BLOCK_HEIGHT * 1.75, MAP_BLOCK_HEIGHT)).convert_alpha()                    

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
                    time = random.uniform(0.08, 0.18)
                    self.objects.append(Coin(pygame.Vector2(i + MAP_BLOCK_WIDTH / 2 - MAP_BLOCK_HEIGHT * 1.75 * 0.456, -MAP_BLOCK_HEIGHT - 10), self.IMAGE_COIN_DEFAULT, time))
    
    def random_image(self):
        rand = random.uniform(0, 1)
        if rand < 1/3:
            return self.IMAGE_BLOCK[0]
        elif rand > 2/3:
            return self.IMAGE_BLOCK[1]
        else:
            return self.IMAGE_BLOCK[2]
        
        
    def update_map_movement(self, game_speed, dt):
        
        pos = game_speed * dt
        self.block_movement += pos
        self.total_distance += pos

        #Move objects down
        self.move_objects(pos, dt)

        #Spawn new row if there is enough space
        if self.block_movement >= 2 * MAP_BLOCK_HEIGHT:
            self.block_movement = 0
            self.createRow()
    
    def move_objects(self, pos, dt):
        #Move clouds
        self.clouds_pos_1 += pygame.Vector2(0, pos * 0.2)
        self.clouds_pos_2 += pygame.Vector2(0, pos * 0.2)

        #If the bottom image reaches the bottom of the screen, then move it above the other one
        if self.clouds_pos_1.y > SCREEN_HEIGHT:
            self.clouds_pos_1 = pygame.Vector2(GAME_DISPLACEMENT,-CLOUDS_HEIGHT * 2 + SCREEN_HEIGHT)
        elif self.clouds_pos_2.y > SCREEN_HEIGHT:
            self.clouds_pos_2 = pygame.Vector2(GAME_DISPLACEMENT,-CLOUDS_HEIGHT * 2 + SCREEN_HEIGHT)

        #Update position for each object
        for i in self.objects:

            #if isinstance(i, Coin):
                #i.update_image(dt)

            i.update_pos(pos, dt)
            
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
        #Draw background image
        surface.blit(self.IMAGE_BACKGROUND, [0,0])

        #Blit the cloud images that are visible on screen
        if self.clouds_pos_1.y > -CLOUDS_HEIGHT:
            surface.blit(self.IMAGE_CLOUDS, self.clouds_pos_1)
        if self.clouds_pos_2.y > -CLOUDS_HEIGHT:
            surface.blit(self.IMAGE_CLOUDS_MIRROR, self.clouds_pos_2)

        #Draw all objects in list
        for i in self.objects:
            i.draw(surface)

        