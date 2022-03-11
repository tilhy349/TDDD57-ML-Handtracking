import pygame
from settings import * 
from abc import ABC, abstractmethod

IMAGE_COIN = [pygame.transform.scale( pygame.image.load("Project\Images\Coin_1.png"), (MAP_BLOCK_HEIGHT * 1.75, MAP_BLOCK_HEIGHT)),
              pygame.transform.scale( pygame.image.load("Project\Images\Coin_2.png"), (MAP_BLOCK_HEIGHT * 1.75, MAP_BLOCK_HEIGHT)),
              pygame.transform.scale( pygame.image.load("Project\Images\Coin_3.png"), (MAP_BLOCK_HEIGHT * 1.75, MAP_BLOCK_HEIGHT)),
              pygame.transform.scale( pygame.image.load("Project\Images\Coin_3_5.png"), (MAP_BLOCK_HEIGHT * 1.75, MAP_BLOCK_HEIGHT)),
              pygame.transform.scale( pygame.image.load("Project\Images\Coin_4.png"), (MAP_BLOCK_HEIGHT * 1.75, MAP_BLOCK_HEIGHT))]

class DrawableObject(ABC):
    def __init__(self, pos, image):
        self.pos = pos
        self.hitbox = pygame.Rect(self.pos.x, self.pos.y, MAP_BLOCK_WIDTH, MAP_BLOCK_HEIGHT)
        self.image = image
        
    @abstractmethod
    def draw(self, surface):
        pass

    @abstractmethod
    def update_pos(self, pos, dt):
        pass

class Coin (DrawableObject):
    def __init__(self, pos, image, time):
        DrawableObject.__init__(self, pos, image)
        self.current_coin = CoinImage.FRONT1
        self.timer_limit = time #0.2
        self.time = 0
        
    def draw(self, surface):
        surface.blit(self.image, self.pos)
        #pygame.draw.rect(surface, (250, 250, 0), self.hitbox)

    def update_pos(self, pos, dt):
        self.pos = pygame.Vector2(self.pos.x, self.pos.y + pos)
        self.hitbox.update(self.pos.x - 5, self.pos.y - 5, MAP_BLOCK_HEIGHT + 10, MAP_BLOCK_HEIGHT + 10)

        self.update_image(dt)
    
    def change_image(self):
        #Set image according to rotation
        if self.current_coin == CoinImage.FRONT1:
            self.image = IMAGE_COIN[0]
        elif self.current_coin == CoinImage.FRONT2 or self.current_coin == CoinImage.BACK3:
            self.image = IMAGE_COIN[1]
        elif self.current_coin == CoinImage.FRONT3 or self.current_coin == CoinImage.BACK2:
            self.image = IMAGE_COIN[2]
        elif self.current_coin == CoinImage.FRONT4 or self.current_coin == CoinImage.BACK1:
            self.image = IMAGE_COIN[3]
        elif self.current_coin == CoinImage.SIDE:
            self.image = IMAGE_COIN[4]
    
    def update_image(self, dt):
        self.time += dt/60
        
        if self.time >= self.timer_limit:
            self.time = 0
            if (self.current_coin == CoinImage.BACK3):
                self.current_coin = CoinImage.FRONT1
            else:
                self.current_coin = CoinImage(self.current_coin.value + 1)

            self.change_image()                
        
class Block (DrawableObject):
    def __init__(self, pos, image):
        DrawableObject.__init__(self, pos, image)
        
    def draw(self, surface):
        surface.blit(self.image, self.pos)
        #pygame.draw.rect(surface, (155, 103, 60), self.hitbox)
    
    def update_pos(self, pos, dt):
        border = 7
        self.pos = pygame.Vector2(self.pos.x, self.pos.y + pos)
        self.hitbox.update(self.pos.x + border, self.pos.y + border, MAP_BLOCK_WIDTH - border * 2, MAP_BLOCK_HEIGHT - border * 2)