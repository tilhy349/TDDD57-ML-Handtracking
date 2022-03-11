import pygame
from settings import *

#Constants
LOGO_HEIGHT = 100 
LOGO_WIDTH = LOGO_HEIGHT * 4.04
LOGO_DINO_WIDTH = 100
LOGO_DINO_HEIGHT = LOGO_DINO_WIDTH * 1.1

COIN_HEIGHT = MAP_BLOCK_HEIGHT
COIN_WIDTH = COIN_HEIGHT * 1.75

START_END_WIDTH = 289/2.1
START_END_HEIGHT = 188/2.1
PEACE_WIDTH = 455/6.675
PEACE_HEIGHT = 767/7.67
CLOSE_WIDTH = 376/4.7
CLOSE_HEIGHT = 473/4.7

#Font settings
FONT_LARGE_HEIGHT = 100
FONT_SMALL_HEIGHT = 25
FONT_XS_HEIGHT = 20

# Initialize pygame to load fonts
pygame.font.init()

UI_FONT_LARGE = pygame.font.Font('Project\Fonts\PixelOperator-Bold.ttf', FONT_LARGE_HEIGHT)
UI_FONT_SMALL = pygame.font.Font('Project\Fonts\PixelOperator-Bold.ttf', FONT_SMALL_HEIGHT)
UI_FONT_XS = pygame.font.Font('Project\Fonts\PixelOperator-Bold.ttf', FONT_XS_HEIGHT)

FRAME_SMALL_WIDTH = 180
FRAME_SMALL_HEIGHT = 160

#Variables for text and image placement
FRAME_HEIGHT = 160
BORDER = 10    
DISP_Y = int((SCREEN_HEIGHT - 3*FRAME_HEIGHT)/4)
TEXT_PLACE = FRAME_HEIGHT - FONT_XS_HEIGHT - 10
IMAGE_PLACE = 20
MIDDLE = SCREEN_WIDTH - 17 - FRAME_SMALL_WIDTH/2

SIZE_BOX = 30 
BOX_WIDTH = (SIZE_BOX + BORDER)*3 + BORDER
BOX_HEIGHT = SIZE_BOX + BORDER*2
POWER_BAR_X = MIDDLE - BOX_WIDTH/2
POWER_BAR_Y = SCREEN_HEIGHT*3/4  - FONT_SMALL_HEIGHT/2 

class UI:
    def __init__(self, surface):
        self.surface = surface
        
        #---- UI for Start menu ---
        #Texts
        self.text_instructions = UI_FONT_SMALL.render('Start Game With The Gesture', True, COLOR_ORIGINAL).convert_alpha()
        self.text_instructions_width = self.text_instructions.get_width()
        self.text_instructions_height = self.text_instructions.get_height()
        #Images
        self.IMAGE_BACKGROUND_MENU = pygame.transform.scale(pygame.image.load("Project\Images\Background_menu.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
        self.IMAGE_LOGO = pygame.transform.scale(pygame.image.load("Project\Images\Game_name.png"), (LOGO_WIDTH, LOGO_HEIGHT)).convert_alpha()
        self.IMAGE_LOGO_DINO = pygame.transform.scale(pygame.image.load("Project\Images\Dino_default.png"), (LOGO_DINO_WIDTH, LOGO_DINO_HEIGHT)).convert_alpha()

        self.IMAGE_START_END_BLACK = pygame.transform.scale( pygame.image.load("Project\Images\Start_end_black.png"), (288/2.2, 186/2.2)).convert_alpha()

        #---- UI for End menu -----
        #Texts
        self.text_game_over = UI_FONT_LARGE.render('Game Over', True, COLOR_ORIGINAL).convert_alpha()
        self.text_game_over_width = self.text_game_over.get_width()
        self.text_game_over_height = self.text_game_over.get_height()

        self.text_powerup = UI_FONT_SMALL.render('Power: ', True, COLOR_ORIGINAL).convert_alpha()
        self.text_powerup_width = self.text_powerup.get_width()
        self.text_powerup_height = self.text_powerup.get_height()
        
        #---- UI for Game -----
        #Texts
        self.text_power_start_end = UI_FONT_XS.render('End the game', True, COLOR_ORIGINAL).convert_alpha()
        self.text_power_start_end_width = self.text_power_start_end.get_width()
        self.text_power_start_end_height = self.text_power_start_end.get_height()

        self.text_power_peace = UI_FONT_XS.render('Slowmotion power', True, COLOR_ORIGINAL).convert_alpha()
        self.text_power_peace_width = self.text_power_peace.get_width()
        self.text_power_peace_height = self.text_power_peace.get_height()

        self.text_power_close = UI_FONT_XS.render('Invisible power', True, COLOR_ORIGINAL).convert_alpha()
        self.text_power_close_width = self.text_power_close.get_width()
        self.text_power_close_height = self.text_power_close.get_height()

        #Images
        self.IMAGE_COIN_DEFAULT = pygame.transform.scale( pygame.image.load("Project\Images\Coin_1.png"), (COIN_WIDTH, COIN_HEIGHT)).convert_alpha()

        self.IMAGE_START_END = pygame.transform.scale( pygame.image.load("Project\Images\Start_end.png"), (START_END_WIDTH, START_END_HEIGHT)).convert_alpha()
        self.IMAGE_PEACE = pygame.transform.scale( pygame.image.load("Project\Images\Peace.png"), (PEACE_WIDTH, PEACE_HEIGHT)).convert_alpha()
        self.IMAGE_CLOSE = pygame.transform.scale( pygame.image.load("Project\Images\Close.png"), (CLOSE_WIDTH, CLOSE_HEIGHT)).convert_alpha()

        self.IMAGE_FRAME_LARGE = pygame.transform.scale(pygame.image.load("Project\Images\Frame.png"), (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 100)).convert_alpha()
        self.IMAGE_FRAME_XS = pygame.transform.scale(self.IMAGE_FRAME_LARGE, (125, 85)).convert_alpha()
        self.IMAGE_FRAME_SMALL = pygame.transform.scale(self.IMAGE_FRAME_LARGE, (FRAME_SMALL_WIDTH, FRAME_SMALL_HEIGHT)).convert_alpha()
        
    #Function which draws the loading bar given a specified time and position
    def draw_loading_bar(self, timer_val, pos):
        number = int(timer_val / TIMER_LIMIT * 8) #Number of boxes

        pygame.draw.rect(self.surface, COLOR_ORIGINAL, pygame.Rect(pos.x, pos.y, 260, 45), 2)
        
        for i in range(number):
            pygame.draw.rect(self.surface, (252, 120 + 15 * (i+1), 30 * i), pygame.Rect(pos.x + 10 + 30 * i, pos.y + 10, 25, 25))
            pygame.draw.rect(self.surface, COLOR_ORIGINAL, pygame.Rect(pos.x + 10 + 30 * i, pos.y + 10, 25, 25), 1)
    
    def draw_power_bar(self, powerups):
        
        #Render power bar 
        self.surface.blit(self.text_powerup, dest=(MIDDLE - (self.text_powerup_width) / 2, POWER_BAR_Y))
        pygame.draw.rect(self.surface, COLOR_ORIGINAL, pygame.Rect(POWER_BAR_X, POWER_BAR_Y + self.text_powerup_height + BORDER, 
                         BOX_WIDTH, BOX_HEIGHT ), 1)
        
        for i in range(powerups):
            pygame.draw.rect(self.surface, (255-165/(i+1),248-7/(i+1),255-64/(i+1)), 
            pygame.Rect(POWER_BAR_X + BORDER + (SIZE_BOX + BORDER) * i, 
                        POWER_BAR_Y + self.text_powerup_height + BORDER * 2, SIZE_BOX, SIZE_BOX))
       
    def draw_ui_menu(self, timer_val):
        
        #Fixing the background
        self.surface.blit(self.IMAGE_BACKGROUND_MENU, [0,0])
        
        self.surface.blit(self.IMAGE_FRAME_LARGE, [75, 50])
        pygame.draw.rect(self.surface, (155, 218, 250), pygame.Rect(105, 75, SCREEN_WIDTH - 210, SCREEN_HEIGHT - 145))
        
        #Draw loading bar
        self.draw_loading_bar(timer_val, pygame.Vector2((SCREEN_WIDTH - 260) / 2, 270))
         
        #Render text   
        self.surface.blit(self.text_instructions,dest=((SCREEN_WIDTH - self.text_instructions_width) / 2, 230))
        
        #Render logo
        self.surface.blit(self.IMAGE_LOGO, [(SCREEN_WIDTH - LOGO_WIDTH + 55) / 2, 120])

        #Render start_end image
        self.surface.blit(self.IMAGE_START_END_BLACK, [430, 330])

        #Render dino
        self.surface.blit(self.IMAGE_LOGO_DINO, [227, 115])
    
    def draw_ui_game(self, n_coins, tot_dist, current_powerups):
        
        #Render left side with gesture instructions
        self.surface.blit(self.IMAGE_FRAME_SMALL, [17, DISP_Y])
        self.surface.blit(self.text_power_start_end, [( 210 - self.text_power_start_end_width) /2, DISP_Y + TEXT_PLACE])
        self.surface.blit(self.IMAGE_START_END, [ (210 - START_END_WIDTH) /2, DISP_Y + IMAGE_PLACE ])
        
        self.surface.blit(self.IMAGE_FRAME_SMALL, [17, DISP_Y*2 + FRAME_HEIGHT])
        self.surface.blit(self.text_power_peace, [ (210 - self.text_power_peace_width)/ 2, DISP_Y*2 + FRAME_HEIGHT + TEXT_PLACE])
        self.surface.blit(self.IMAGE_PEACE, [(200 - PEACE_WIDTH) / 2, DISP_Y*2 + FRAME_HEIGHT + IMAGE_PLACE ])
        
        self.surface.blit(self.IMAGE_FRAME_SMALL, [17, DISP_Y*3 + FRAME_HEIGHT*2])
        self.surface.blit(self.text_power_close, [ (210 - self.text_power_close_width) /2,  DISP_Y*3 + FRAME_HEIGHT*2 + TEXT_PLACE])
        self.surface.blit(self.IMAGE_CLOSE, [( 210 - CLOSE_WIDTH)/2, DISP_Y*3 + FRAME_HEIGHT*2 + IMAGE_PLACE])
        
        #Render frames for the left side
        self.surface.blit(self.IMAGE_FRAME_SMALL, [SCREEN_WIDTH - 17 - FRAME_SMALL_WIDTH, DISP_Y])
        self.surface.blit(self.IMAGE_FRAME_SMALL, [SCREEN_WIDTH - 17 - FRAME_SMALL_WIDTH, DISP_Y*2 + FRAME_HEIGHT])
        self.surface.blit(self.IMAGE_FRAME_SMALL, [SCREEN_WIDTH - 17 - FRAME_SMALL_WIDTH, DISP_Y*3 + FRAME_HEIGHT*2])
        
        #Render distance information 
        text_distance = UI_FONT_SMALL.render("Distance: " + str(int(tot_dist/(2*MAP_BLOCK_HEIGHT))), True, COLOR_ORIGINAL)
        self.surface.blit(text_distance,dest=( MIDDLE - text_distance.get_width()/2, DISP_Y + FRAME_HEIGHT/2 - text_distance.get_height()/2))
        
        #Render coin information
        coin_y = SCREEN_HEIGHT/2 - (MAP_BLOCK_HEIGHT + FONT_SMALL_HEIGHT + BORDER)/2
        text_coins = UI_FONT_SMALL.render("Coins: " + str(n_coins), True, COLOR_ORIGINAL)
        self.surface.blit(self.IMAGE_COIN_DEFAULT, [MIDDLE - MAP_BLOCK_HEIGHT * 1.75 * 0.456, coin_y])
        self.surface.blit(text_coins,dest=(MIDDLE - text_coins.get_width()/2, coin_y + MAP_BLOCK_HEIGHT + BORDER))

        #Draw the power up bar
        self.draw_power_bar(current_powerups)
        
    def draw_ui_end(self, tot_dist, timer_val):
        
        #Fixing the background
        self.surface.blit(self.IMAGE_BACKGROUND_MENU, [0,0])
        self.surface.blit(self.IMAGE_FRAME_LARGE, [75, 50])

        pygame.draw.rect(self.surface, (155, 218, 250), pygame.Rect(105, 75, SCREEN_WIDTH - 210, SCREEN_HEIGHT - 145))
        
        #Render text
        self.surface.blit(self.text_game_over,dest=((SCREEN_WIDTH - self.text_game_over.get_width()) / 2, 80))

        #text = UI_FONT_SMALL.render("You collected " + str(n_coins) + " coins. Good job!", True, COLOR_ORIGINAL)
        #self.surface.blit(text,dest=((SCREEN_WIDTH - text.get_width())/2, 170))
        text = UI_FONT_SMALL.render("Total distance is " + str(int(tot_dist/(2*MAP_BLOCK_HEIGHT))) + ". Not bad!", True, COLOR_ORIGINAL)
        self.surface.blit(text,dest=((SCREEN_WIDTH - text.get_width())/2, 190))
        text = UI_FONT_SMALL.render("Do gesture to play again!", True, COLOR_ORIGINAL)
        self.surface.blit(text,dest=((SCREEN_WIDTH - text.get_width())/2, 220))
        
        #Render pinch image
        self.surface.blit(self.IMAGE_START_END_BLACK, [430, 245])
        
        #Draw loading bar
        self.draw_loading_bar(timer_val, pygame.Vector2(370, 337))  
        