import pygame
from settings import *

class UI:
    def __init__(self, surface):
        self.surface = surface

        self.game_ui_font = pygame.font.Font(pygame.font.get_default_font(), 100)
        self.game_ui_font_small = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.text_game_name = self.game_ui_font.render('The Game', True, (0, 0, 0))
        self.text_instructions = self.game_ui_font_small.render('Start game by doing the gesture', True, (0, 0, 0))
        self.text_game_over = self.game_ui_font.render('Game Over', True, (0, 0, 0))
        self.text_powerup = self.game_ui_font_small.render('Available power: ', True, (0, 0, 0))
    
    def draw_loading_bar(self, timer_val, timerpos):
        number = int(timer_val / TIMER_LIMIT * 8)

        pygame.draw.rect(self.surface, (0,0,0), pygame.Rect(timerpos.x, timerpos.y, 260, 45), 1)
        
        for i in range(number):
            pygame.draw.rect(self.surface, (0,0,0), pygame.Rect(timerpos.x + 10 + 30 * i, timerpos.y + 10, 25, 25))
    
    
    def draw_power_bar(self, powerups):
    
        #render power bar
        self.surface.blit(self.text_powerup, dest=(40, 500))
        pygame.draw.rect(self.surface, (0,0,0), pygame.Rect(65, 520, 100, 40), 1)
        
        for i in range(powerups):
            pygame.draw.rect(self.surface, (0,0,0), pygame.Rect(65 + 10 + 30 * i, 530, 20, 20))
       
    
    def draw_ui_menu(self, timer_val):
        self.surface.fill((220, 100, 10))

        #Draw loading bar
        self.draw_loading_bar(timer_val, pygame.Vector2(240, 280))
         
        #Render text   
        self.surface.blit(self.text_game_name,dest=(130, 100))
        self.surface.blit(self.text_instructions,dest=(160, 250))
    
    def draw_ui_game(self, n_coins, tot_dist):
        
        #Render ui text
        text_coins = self.game_ui_font_small.render("Coins: " + str(n_coins), True, (0, 0, 0))
        self.surface.blit(text_coins,dest=(130, 50))
        text_distance = self.game_ui_font_small.render("Distance: " + str(int(tot_dist/(2*MAP_BLOCK_HEIGHT))), True, (0, 0, 0))
        self.surface.blit(text_distance,dest=(250, 50))
    
    def draw_ui_end(self, n_coins, tot_dist, timer_val):
        # Initialing Color
        self.surface.fill((220, 100, 10))

        #Render text
        self.surface.blit(self.text_game_over,dest=(130, 100))

        text = self.game_ui_font_small.render("You collected " + str(n_coins) + " coins. Good job!", True, (0, 0, 0))
        self.surface.blit(text,dest=(130, 250))
        text = self.game_ui_font_small.render("Total distance is " + str(int(tot_dist/(2*MAP_BLOCK_HEIGHT))) + ". Not bad!", True, (0, 0, 0))
        self.surface.blit(text,dest=(130, 300))
        text = self.game_ui_font_small.render("Do pinch gesture to play again!", True, (0, 0, 0))
        self.surface.blit(text,dest=(130, 350))

        #Draw loading bar
        self.draw_loading_bar(timer_val, pygame.Vector2(240, 380))  
        