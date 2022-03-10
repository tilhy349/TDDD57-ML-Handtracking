import pygame
from settings import *
#Constants

#Limits for the player movement area
PLAYER_LIMIT_UP = 40
PLAYER_LIMIT_DOWN = 400

#Specified delay for updating player movement
DELAY = 200
PLAYER_VELOCITY = 4
MAX_TAIL = 4

class Player:

    def __init__(self):
        self.hitbox = pygame.Rect(0, 0, PLAYER_WIDTH - 14, PLAYER_HEIGHT - 14)

        self.start_pos = pygame.Vector2(0.0, 0.0)
        self.end_pos = pygame.Vector2(0.0, 0.0)
        self.curr_pos = pygame.Vector2(400.0, 300.0)
        self.moving_dir = pygame.Vector2(0.0, 0.0)

        self.player_image = PlayerImage.DEFAULT

        self.tail = []

        self.IMAGE_PLAYER_DEFAULT = pygame.transform.scale( pygame.image.load("Project\Images\Dino_default.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()
        self.IMAGE_PLAYER_PEACE = pygame.transform.scale( pygame.image.load("Project\Images\Dino_peace.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()
        self.IMAGE_PLAYER_CLOSE = pygame.transform.scale( pygame.image.load("Project\Images\Dino_close.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()

        self.IMAGE_PLAYER_DEFAULT_MIRROR = pygame.transform.scale( pygame.image.load("Project\Images\Dino_default_mirrored.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()
        self.IMAGE_PLAYER_PEACE_MIRROR = pygame.transform.scale( pygame.image.load("Project\Images\Dino_peace_mirrored.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()
        self.IMAGE_PLAYER_CLOSE_MIRROR = pygame.transform.scale( pygame.image.load("Project\Images\Dino_close_mirrored.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()
    
    def draw_player(self, surface):
        image = self.IMAGE_PLAYER_DEFAULT
        
        #Dino going to the left
        if self.moving_dir.x < 0:
            if self.player_image == PlayerImage.CLOSE:
                image = self.IMAGE_PLAYER_CLOSE_MIRROR
            elif self.player_image == PlayerImage.PEACE:
                image = self.IMAGE_PLAYER_PEACE_MIRROR
            else:
                image = self.IMAGE_PLAYER_DEFAULT_MIRROR
        #Dino going to the right
        else:
            if self.player_image == PlayerImage.CLOSE:
                image = self.IMAGE_PLAYER_CLOSE
            elif self.player_image == PlayerImage.PEACE:
                image = self.IMAGE_PLAYER_PEACE
            else:
                image = self.IMAGE_PLAYER_DEFAULT

        #Draw tail
        for idx, i in enumerate(self.tail):
            #Tail is more transparent the further away it is
            blit_alpha(surface, image, i, 25 * idx+1) 

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

        self.tail.append(self.curr_pos)

        if len(self.tail) > MAX_TAIL:
            self.tail.pop(0)

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
       
    