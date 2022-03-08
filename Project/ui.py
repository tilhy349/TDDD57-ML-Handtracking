import pygame
from settings import *

class UI:
    def __init__(self, surface):
        self.surface = surface
        
        #Text for Start menu
        self.text_game_name = UI_FONT.render('The Game', True, COLOR_ORIGINAL)
        self.text_instructions = UI_FONT_SMALL.render('Start Game With The Gesture', True, COLOR_ORIGINAL)
        
        #Text for End menu
        self.text_game_over = UI_FONT.render('Game Over', True, COLOR_ORIGINAL)
        self.text_powerup = UI_FONT_SMALL.render('Available power: ', True, COLOR_ORIGINAL)
        
        #Text for Game
        self.text_power_start_end = UI_FONT_XS.render('Start/end the game', True, COLOR_ORIGINAL)
        self.text_power_peace = UI_FONT_XS.render('Slowmotion power', True, COLOR_ORIGINAL)
        self.text_power_close = UI_FONT_XS.render('Invisible power', True, COLOR_ORIGINAL)

        #Images for Peace, Close and Pinch
        self.image_peace_gesture = pygame.transform.scale( pygame.image.load("Project\Images\Peace.png"), (IMAGE_PEACE_WIDTH, IMAGE_PEACE_HEIGHT))
        self.image_close_gesture = pygame.transform.scale( pygame.image.load("Project\Images\Close.png"), (IMAGE_CLOSE_WIDTH, IMAGE_CLOSE_HEIGHT))
        self.image_start_end_gesture = pygame.transform.scale( pygame.image.load("Project\Images\Start_end.png"), (IMAGE_START_END_WIDTH, IMAGE_START_END_HEIGHT))
    
    def draw_loading_bar(self, timer_val, timerpos):
        number = int(timer_val / TIMER_LIMIT * 8)

        pygame.draw.rect(self.surface, (0,0,0), pygame.Rect(timerpos.x, timerpos.y, 260, 45), 1)
        
        for i in range(number):
            pygame.draw.rect(self.surface, (0,0,0), pygame.Rect(timerpos.x + 10 + 30 * i, timerpos.y + 10, 25, 25))
    
    
    def draw_power_bar(self, powerups):
        
        size_box = 30 
        displacement = 10
        box_width = (size_box + displacement)*3 + displacement
        box_height = size_box + displacement*2
        x = SCREEN_WIDTH - GAME_DISPLACEMENT + box_width/2 - 10
        y = SCREEN_HEIGHT*3/4  - FONT_SMALL_HEIGHT/2 # - (FONT_SMALL_HEIGHT + displacement + box_height) / 2
        
        #render power bar (GAME_DISPLACEMENT + GAME_WIDTH + self.text_powerup.get_width()) /2
        self.surface.blit(self.text_powerup, dest=(SCREEN_WIDTH - GAME_DISPLACEMENT + (GAME_DISPLACEMENT - self.text_powerup.get_width()) / 2, y))
        pygame.draw.rect(self.surface, (0,0,0), pygame.Rect(x, y + self.text_powerup.get_height() + displacement, box_width, box_height ), 1)
        
        for i in range(powerups):
            pygame.draw.rect(self.surface, (0,0,0), pygame.Rect(x + displacement + (size_box + displacement) * i, y + self.text_powerup.get_height() + displacement * 2, size_box, size_box))
       
    
    def draw_ui_menu(self, timer_val):
        self.surface.fill((220, 100, 10))
        
        #Fixing the background
        self.surface.blit(IMAGE_BACKGROUND_MENU, [0,0])
        self.surface.blit(pygame.transform.scale(IMAGE_FRAME, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 100)), [75, 50])
        
        #Draw loading bar
        self.draw_loading_bar(timer_val, pygame.Vector2((SCREEN_WIDTH - 260) / 2, 150 + IMAGE_START_END_HEIGHT + 50))
         
        #Render text   
        self.surface.blit(self.text_game_name,dest=((SCREEN_WIDTH - self.text_game_name.get_width()) / 2, 80))
        self.surface.blit(self.text_instructions,dest=((SCREEN_WIDTH - self.text_instructions.get_width()) / 2, 150 + IMAGE_START_END_HEIGHT + 10))
        
        #Render pinch image
        image = pygame.transform.scale(self.image_start_end_gesture, [170, 0.66*170])
        self.surface.blit(image, [(SCREEN_WIDTH - image.get_width()) / 2, 170])
    
    def draw_ui_game(self, n_coins, tot_dist):
        
        #Set variables
        displacement = 20
        border = 10 
        
        #Render distance information 
        distance_y = SCREEN_HEIGHT/4 - (FONT_SMALL_HEIGHT)/2
        text_distance = UI_FONT_SMALL.render("Distance: " + str(int(tot_dist/(2*MAP_BLOCK_HEIGHT))), True, COLOR_ORIGINAL)
        self.surface.blit(text_distance,dest=((GAME_DISPLACEMENT - text_distance.get_width()) / 2 + SCREEN_WIDTH - GAME_DISPLACEMENT - 10, distance_y))
        
        #Render coin information
        coin_y = SCREEN_HEIGHT/2 - (IMAGE_COIN.get_height() + FONT_SMALL_HEIGHT + border)/2
        self.surface.blit(IMAGE_COIN, [(GAME_DISPLACEMENT - IMAGE_COIN.get_width()) / 2 + SCREEN_WIDTH - GAME_DISPLACEMENT - 10, coin_y])
        text_coins = UI_FONT_SMALL.render("Coins: " + str(n_coins), True, COLOR_ORIGINAL)
        self.surface.blit(text_coins,dest=((GAME_DISPLACEMENT - text_coins.get_width()) / 2 + SCREEN_WIDTH - GAME_DISPLACEMENT - 10, coin_y + IMAGE_COIN.get_height() + border))
        
        #Render left side with gesture instructions
        y = displacement
        self.surface.blit(self.image_start_end_gesture, [(GAME_DISPLACEMENT - IMAGE_START_END_WIDTH) / 2, y])
        y += IMAGE_START_END_HEIGHT + border 
        self.surface.blit(self.text_power_start_end, [(GAME_DISPLACEMENT - self.text_power_start_end.get_width()) / 2, y])
        y += displacement + FONT_XS_HEIGHT
        self.surface.blit(self.image_peace_gesture, [(GAME_DISPLACEMENT - IMAGE_PEACE_WIDTH) / 2,  y])
        y += IMAGE_PEACE_HEIGHT + border
        self.surface.blit(self.text_power_peace, [(GAME_DISPLACEMENT - self.text_power_peace.get_width()) / 2, y])
        y += displacement + FONT_XS_HEIGHT
        self.surface.blit(self.image_close_gesture, [(GAME_DISPLACEMENT - IMAGE_CLOSE_WIDTH) / 2, y])
        y += IMAGE_CLOSE_HEIGHT + border
        self.surface.blit(self.text_power_close, [(GAME_DISPLACEMENT - self.text_power_close.get_width()) / 2, y])
        
        
    def draw_ui_end(self, n_coins, tot_dist, timer_val):
        # Initialing Color
        self.surface.fill((220, 100, 10))
        
        #Fixing the background
        self.surface.blit(IMAGE_BACKGROUND_MENU, [0,0])
        self.surface.blit(pygame.transform.scale(IMAGE_FRAME, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 100)), [75, 50])
        
        #Render text
        self.surface.blit(self.text_game_over,dest=((SCREEN_WIDTH - self.text_game_over.get_width()) / 2, 80))

        #text = UI_FONT_SMALL.render("You collected " + str(n_coins) + " coins. Good job!", True, COLOR_ORIGINAL)
        #self.surface.blit(text,dest=((SCREEN_WIDTH - text.get_width())/2, 170))
        text = UI_FONT_SMALL.render("Total distance is " + str(int(tot_dist/(2*MAP_BLOCK_HEIGHT))) + ". Not bad!", True, COLOR_ORIGINAL)
        self.surface.blit(text,dest=((SCREEN_WIDTH - text.get_width())/2, 190))
        text = UI_FONT_SMALL.render("Do gesture to play again!", True, COLOR_ORIGINAL)
        self.surface.blit(text,dest=((SCREEN_WIDTH - text.get_width())/2, 220))
        
        #Render pinch image
        image = pygame.transform.scale(self.image_start_end_gesture, [170, 0.66*170])
        self.surface.blit(image, [(SCREEN_WIDTH - image.get_width()) / 2, 240])
        
        #Draw loading bar
        self.draw_loading_bar(timer_val, pygame.Vector2((SCREEN_WIDTH - 260) / 2, 240 + image.get_height() + 20))  
        