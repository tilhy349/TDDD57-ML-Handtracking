import pygame
import time
import random
import cv2
import mediapipe as mp
from HandTracking import HandTracking
from settings import *
from player import Player
from map import Map

class Game:
    def __init__(self, surface):
        self.surface = surface
        self.surface.fill((255,255,255))

        #Load camera (webcam)
        self.cap = cv2.VideoCapture(0) 

        self.clock = pygame.time.Clock()

        self.timer = 0
        self.timer_start = 0
        self.running_last_frame = False

        self.game_state = State.MENU

        self.hand_tracking = HandTracking()

        self.player = Player()

        self.map = Map()

        self.total_distance = 0

        self.game_speed = 0.1
        self.last_time = 0

        self.total_movement = 0
            
        #UI
        self.game_ui_font = pygame.font.Font(pygame.font.get_default_font(), 100)
        self.game_ui_font_small = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.text_game_name = self.game_ui_font.render('The Game', True, (0, 0, 0))
        self.text_instructions = self.game_ui_font_small.render('Start game by doing the gesture', True, (0, 0, 0))
        self.text_game_over = self.game_ui_font.render('Game Over', True, (0, 0, 0))

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
        text_distance = self.game_ui_font_small.render("Distance: " + str(self.total_distance), True, (0, 0, 0))
        self.surface.blit(text_distance,dest=(250, 50))
    
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
        text = self.game_ui_font_small.render("Total distance is " + str(self.total_distance) + ". Not bad!", True, (0, 0, 0))
        self.surface.blit(text,dest=(130, 300))
        text = self.game_ui_font_small.render("Do pinch gesture to play again!", True, (0, 0, 0))
        self.surface.blit(text,dest=(130, 350))

        #Draw loading bar
        self.draw_loading_bar(pygame.Vector2(240, 380))
        
    def update_player_movement(self):
        #Update player position according to right hand
        end_pos = self.hand_tracking.retrieve_player_pos()
        self.player.update_moving_dir(end_pos)
    
    def timer_start_end(self, timer_running):
        #If timer was not running last frame, reset timer
        if not self.running_last_frame and timer_running:
            self.timer = 0
            self.timer_start = pygame.time.get_ticks()
            #print("TIMER HAS STARTED")
        elif timer_running:
            self.timer = pygame.time.get_ticks() - self.timer_start 
            #print("current time: ", self.timer) 
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
        
    def update_map_movement(self):
        dt = pygame.time.get_ticks() * 0.001 - self.last_time
        dt *= 60
        self.last_time = pygame.time.get_ticks() * 0.001

        pos = self.game_speed * dt
        self.total_movement += pos

        #Move objects down
        self.map.move_objects(pos)
        self.total_distance += pos

        #Spawn new row if there is enough space
        if self.total_movement >= 2 * MAP_BLOCK_HEIGHT:
            self.total_movement = 0
            self.map.createRow()
        
   
    def update(self):

        self.load_camera()

        #Draw landmarks and process hand positions in videocam
        self.frame = self.hand_tracking.process_hands(self.frame)

        #Process hand gestures, 
        timerRunning = self.hand_tracking.process_hand_gestures()
        
        #Timer for start/end gesture
        self.timer_start_end(timerRunning)

        #Draw depending on the current state
        if self.game_state == State.MENU:
            self.draw_menu()
        elif self.game_state == State.RUNNING:
             
            #Check time and update movement speed
            self.update_map_movement()
            
            #Update player pos
            self.player.move_player() 

            self.draw_running()

            #Controlling if the player have collided with a block, true -> end game
            if self.map.block_collision(self.player.hitbox):
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