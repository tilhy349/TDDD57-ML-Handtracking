import pygame
import time
import random
import cv2
import mediapipe as mp
from HandTracking import HandTracking
from settings import *
from player import Player
from map import Map
from powerup import PowerupHandler

class Game:
    def __init__(self, surface):
        self.surface = surface

        #Load camera (webcam)
        self.cap = cv2.VideoCapture(0) 

        self.clock = pygame.time.Clock()

        self.game_state = State.MENU

        self.hand_tracking = HandTracking()
        self.player = Player()
        self.map = Map()
        self.powerup = PowerupHandler()

        self.game_speed = 1
        self.last_time = 0

        self.timer = 0
        self.timer_start = 0
        self.running_last_frame = False
            
        #UI
        self.game_ui_font = pygame.font.Font(pygame.font.get_default_font(), 100)
        self.game_ui_font_small = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.text_game_name = self.game_ui_font.render('The Game', True, (0, 0, 0))
        self.text_instructions = self.game_ui_font_small.render('Start game by doing the gesture', True, (0, 0, 0))
        self.text_game_over = self.game_ui_font.render('Game Over', True, (0, 0, 0))
        self.text_powerup = self.game_ui_font_small.render('Available power: ', True, (0, 0, 0))

    def load_camera(self):
        #Store the current frame from webcam
        _, self.frame = self.cap.read()
    
    def draw_running(self):
        self.surface.fill((255,255,255))
        
        #Draw map
        self.map.draw(self.surface)

        #Draw border around hands
        #pygame.draw will not use alpha
        #workaround --> create pygame surface, draw rect, blit with transparency
        pygame.draw.rect(self.surface, (0, 150, 0), pygame.Rect(X_DISPLACEMENT, Y_DISPLACEMENT, X_SCALE, Y_SCALE), 2)
            
        #Draw the player 
        self.player.draw_player(self.surface)  
            
        #Render ui text
        text_coins = self.game_ui_font_small.render("Coins: " + str(self.map.n_coins), True, (0, 0, 0))
        self.surface.blit(text_coins,dest=(130, 50))
        text_distance = self.game_ui_font_small.render("Distance: " + str(int(self.total_distance)), True, (0, 0, 0))
        self.surface.blit(text_distance,dest=(250, 50))
        
        #render power bar
        self.surface.blit(self.text_powerup, dest=(40, 500))
        pygame.draw.rect(self.surface, (0,0,0), pygame.Rect(65, 520, 100, 40), 1)
        
        for i in range(self.powerup.available_powerups):
            pygame.draw.rect(self.surface, (0,0,0), pygame.Rect(65 + 10 + 30 * i, 530, 20, 20))
          
    
    def draw_loading_bar(self, pos):
        number = int(self.timer / TIMER_LIMIT * 8)

        pygame.draw.rect(self.surface, (0,0,0), pygame.Rect(pos.x, pos.y, 260, 45), 1)
        
        for i in range(number):
            pygame.draw.rect(self.surface, (0,0,0), pygame.Rect(pos.x + 10 + 30 * i, pos.y + 10, 25, 25))
          
    def draw_menu(self):
        self.surface.fill((220, 100, 10))

        #Draw loading bar
        self.draw_loading_bar(pygame.Vector2(240, 280))
         
        #Render text   
        self.surface.blit(self.text_game_name,dest=(130, 100))
        self.surface.blit(self.text_instructions,dest=(160, 250))
             
    def draw_end(self):
        # Initialing Color
        self.surface.fill((220, 100, 10))

        #Render text
        self.surface.blit(self.text_game_over,dest=(130, 100))

        text = self.game_ui_font_small.render("You collected " + str(self.map.n_coins) + " coins. Good job!", True, (0, 0, 0))
        self.surface.blit(text,dest=(130, 250))
        text = self.game_ui_font_small.render("Total distance is " + str(int(self.map.total_distance)) + ". Not bad!", True, (0, 0, 0))
        self.surface.blit(text,dest=(130, 300))
        text = self.game_ui_font_small.render("Do pinch gesture to play again!", True, (0, 0, 0))
        self.surface.blit(text,dest=(130, 350))

        #Draw loading bar
        self.draw_loading_bar(pygame.Vector2(240, 380))
        
    def update_player_movement(self):
        #Update player position according to right hand
        end_pos = self.hand_tracking.retrieve_player_pos()
        self.player.update_moving_dir(end_pos)
    
    def timer_start_end(self):
        timer_running = self.hand_tracking.current_gesture == Gesture.START_END

        #If timer was not running last frame, reset timer
        if not self.running_last_frame and timer_running:
            self.timer = 0
            self.timer_start = pygame.time.get_ticks()
        elif timer_running:
            self.timer = pygame.time.get_ticks() - self.timer_start 
        else:
            self.timer = 0   

        if self.timer > TIMER_LIMIT :
            self.timer = 0
            self.timer_start = pygame.time.get_ticks()
            
            if self.game_state == State.RUNNING:
                self.game_state = State.END
            else:
                self.game_state = State.RUNNING
                self.reset_game()

        self.running_last_frame = timer_running

    def reset_game(self):
        self.map = Map()
        self.clock = pygame.time.Clock()
        self.player = Player()

        self.total_distance = 0
        self.last_time = pygame.time.get_ticks() * 0.001

        self.powerup = PowerupHandler()
            
    def update(self):

        self.load_camera()

        #Draw landmarks and process hand positions in videocam
        self.frame = self.hand_tracking.process_hands(self.frame)

        #Process hand gestures, 
        self.hand_tracking.process_hand_gestures()
        
        #Timer for start/end gesture
        self.timer_start_end()

        #Draw depending on the current state
        if self.game_state == State.MENU:
            self.draw_menu()
        elif self.game_state == State.RUNNING:
            dt = pygame.time.get_ticks() * 0.001 - self.last_time
            dt *= 60
            self.last_time = pygame.time.get_ticks() * 0.001

            self.draw_running()

            #Check time and update movement speed
            self.map.update_map_movement(self.game_speed, dt)
            
            #Update player pos
            self.player.move_player(dt) 
            
            #Set and process current power up
            self.powerup.set_powerup(self.hand_tracking.current_gesture)
            self.map.n_coins = self.powerup.process_powerup(dt, self.map.n_coins)

            #Update player color depending on powerup
            self.player.color = self.powerup.player_color
            
            #Controlling if the player have collided with a block, true -> end game
            if self.map.block_collision(self.player.hitbox, self.powerup.current_powerup == Powerup.INVISIBLE):
                self.game_state = State.END    
        else:
            self.draw_end()

        #Draw hand marker based on hand position
        self.hand_tracking.draw_hands(self.surface) 
        
        #Show webcam with landmarks on screen
        cv2.imshow("Frame", cv2.flip(self.frame, 1))
        cv2.waitKey(1) 

        pygame.display.update()
        self.clock.tick(FPS)