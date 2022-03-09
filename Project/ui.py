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
        self.text_powerup = UI_FONT_SMALL.render('Power: ', True, COLOR_ORIGINAL)
        
        #Text for Game
        self.text_power_start_end = UI_FONT_XS.render('End the game', True, COLOR_ORIGINAL)
        self.text_power_peace = UI_FONT_XS.render('Slowmotion power', True, COLOR_ORIGINAL)
        self.text_power_close = UI_FONT_XS.render('Invisible power', True, COLOR_ORIGINAL)
        
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
        middle = SCREEN_WIDTH - 17 - IMAGE_FRAME_SMALL_WIDTH/2 
        x = middle - box_width/2
        y = SCREEN_HEIGHT*3/4  - FONT_SMALL_HEIGHT/2 # - (FONT_SMALL_HEIGHT + displacement + box_height) / 2
        
        #render power bar (GAME_DISPLACEMENT + GAME_WIDTH + self.text_powerup.get_width()) /2
        self.surface.blit(self.text_powerup, dest=(middle - (self.text_powerup.get_width()) / 2, y))
        pygame.draw.rect(self.surface, (0,0,0), pygame.Rect(x, y + self.text_powerup.get_height() + displacement, box_width, box_height ), 1)
        
        for i in range(powerups):
            pygame.draw.rect(self.surface, (105,240,0), pygame.Rect(x + displacement + (size_box + displacement) * i, y + self.text_powerup.get_height() + displacement * 2, size_box, size_box))
       
    
    def draw_ui_menu(self, timer_val):
        self.surface.fill((220, 100, 10))
        
        #Fixing the background
        self.surface.blit(IMAGE_BACKGROUND_MENU, [0,0])
        
        self.surface.blit(IMAGE_FRAME_LARGE, [75, 50])
        
        #Draw loading bar
        self.draw_loading_bar(timer_val, pygame.Vector2((SCREEN_WIDTH - 260) / 2, 150 + 145 + 50))
         
        #Render text   
        self.surface.blit(self.text_game_name,dest=((SCREEN_WIDTH - self.text_game_name.get_width()) / 2, 80))
        self.surface.blit(self.text_instructions,dest=((SCREEN_WIDTH - self.text_instructions.get_width()) / 2, 150 + 145 + 10))
        
        #Render pinch image
        image = pygame.transform.scale(IMAGE_START_END, [170, 0.66*170])
        self.surface.blit(image, [(SCREEN_WIDTH - image.get_width()) / 2, 170])
    
    def draw_ui_game(self, n_coins, tot_dist):
        
        #Set variables
        frame_height = 160
        border = 10    
        disp_y = int((SCREEN_HEIGHT - 3*frame_height)/4)
        text_place = frame_height - FONT_XS_HEIGHT - 10
        image_place = 20
        middle = SCREEN_WIDTH - 17 - IMAGE_FRAME_SMALL_WIDTH/2
        
        #Render left side with gesture instructions
        self.surface.blit(IMAGE_FRAME_SMALL, [17, disp_y])
        self.surface.blit(self.text_power_start_end, [( 210 - self.text_power_start_end.get_width()) /2, disp_y + text_place])
        self.surface.blit(IMAGE_START_END, [ (210 - IMAGE_START_END_WIDTH) /2, disp_y + image_place ])
        
        self.surface.blit(IMAGE_FRAME_SMALL, [17, disp_y*2 + frame_height])
        self.surface.blit(self.text_power_peace, [ (210 - self.text_power_peace.get_width())/ 2, disp_y*2 + frame_height + text_place])
        self.surface.blit(IMAGE_PEACE, [(200 - IMAGE_PEACE_WIDTH) / 2, disp_y*2 + frame_height + image_place ])
        
        self.surface.blit(IMAGE_FRAME_SMALL, [17, disp_y*3 + frame_height*2])
        self.surface.blit(self.text_power_close, [ (210 - self.text_power_close.get_width()) /2,  disp_y*3 + frame_height*2 + text_place])
        self.surface.blit(IMAGE_CLOSE, [( 210 - IMAGE_CLOSE_WIDTH)/2, disp_y*3 + frame_height*2 + image_place])
        
        #Render frames for the left side
        self.surface.blit(IMAGE_FRAME_SMALL, [SCREEN_WIDTH - 17 - IMAGE_FRAME_SMALL_WIDTH, disp_y])
        self.surface.blit(IMAGE_FRAME_SMALL, [SCREEN_WIDTH - 17 - IMAGE_FRAME_SMALL_WIDTH, disp_y*2 + frame_height])
        self.surface.blit(IMAGE_FRAME_SMALL, [SCREEN_WIDTH - 17 - IMAGE_FRAME_SMALL_WIDTH, disp_y*3 + frame_height*2])
        
        #Render distance information 
        text_distance = UI_FONT_SMALL.render("Distance: " + str(int(tot_dist/(2*MAP_BLOCK_HEIGHT))), True, COLOR_ORIGINAL)
        self.surface.blit(text_distance,dest=( middle - text_distance.get_width()/2, disp_y + frame_height/2 - text_distance.get_height()/2))
        
        #Render coin information
        coin_y = SCREEN_HEIGHT/2 - (MAP_BLOCK_HEIGHT + FONT_SMALL_HEIGHT + border)/2
        text_coins = UI_FONT_SMALL.render("Coins: " + str(n_coins), True, COLOR_ORIGINAL)
        self.surface.blit(IMAGE_COIN, [middle - MAP_BLOCK_HEIGHT/2, coin_y])
        self.surface.blit(text_coins,dest=(middle - text_coins.get_width()/2, coin_y + MAP_BLOCK_HEIGHT + border))
        
    def draw_ui_end(self, n_coins, tot_dist, timer_val):
        # Initialing Color
        self.surface.fill((220, 100, 10))
        
        #Fixing the background
        self.surface.blit(IMAGE_BACKGROUND_MENU, [0,0])
        self.surface.blit(IMAGE_FRAME_LARGE, [75, 50])
        
        #Render text
        self.surface.blit(self.text_game_over,dest=((SCREEN_WIDTH - self.text_game_over.get_width()) / 2, 80))

        #text = UI_FONT_SMALL.render("You collected " + str(n_coins) + " coins. Good job!", True, COLOR_ORIGINAL)
        #self.surface.blit(text,dest=((SCREEN_WIDTH - text.get_width())/2, 170))
        text = UI_FONT_SMALL.render("Total distance is " + str(int(tot_dist/(2*MAP_BLOCK_HEIGHT))) + ". Not bad!", True, COLOR_ORIGINAL)
        self.surface.blit(text,dest=((SCREEN_WIDTH - text.get_width())/2, 190))
        text = UI_FONT_SMALL.render("Do gesture to play again!", True, COLOR_ORIGINAL)
        self.surface.blit(text,dest=((SCREEN_WIDTH - text.get_width())/2, 220))
        
        #Render pinch image
        image = pygame.transform.scale(IMAGE_START_END, [170, 0.66*170])
        self.surface.blit(image, [(SCREEN_WIDTH - image.get_width()) / 2, 240])
        
        #Draw loading bar
        self.draw_loading_bar(timer_val, pygame.Vector2((SCREEN_WIDTH - 260) / 2, 240 + image.get_height() + 20))  
        