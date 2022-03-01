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

        #UI
        self.game_ui_font = pygame.font.Font(pygame.font.get_default_font(), 100)
        self.game_ui_font_small = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.text_game_name = self.game_ui_font.render('The Game', True, (0, 0, 0))
        self.text_instructions = self.game_ui_font_small.render('Start game by doing the gesture', True, (0, 0, 0))
        self.text_game_over = self.game_ui_font.render('Game Over', True, (0, 0, 0))

    def load_camera(self):
        #Store the current frame from webcam
        _, self.frame = self.cap.read()
    
    #Drawing all object in the game
    def draw(self):
        # Initialing Color
        self.surface.fill((255,255,255))  

        if self.game_state == State.MENU:
            self.surface.fill((220, 100, 10))
            
            #Render text   
            self.surface.blit(self.text_game_name,dest=(130, 100))
            self.surface.blit(self.text_instructions,dest=(160, 250))
        
        elif self.game_state == State.RUNNING:

            #self.map.move_objects()
            #Draw map
            self.map.draw(self.surface)

            #Draw border around hands
            #pygame.draw will not use alpha
            #workaround --> create pygame surface, draw rect, blit with transparency
            pygame.draw.rect(self.surface, (0, 150, 0), pygame.Rect(X_DISPLACEMENT, Y_DISPLACEMENT, X_SCALE, Y_SCALE), 2)
            
            #Draw the player 
            self.player.draw_player(self.surface)  
            
            #Render text
            text_coins = self.game_ui_font_small.render("Coins: " + str(self.map.n_coins), True, (0, 0, 0))
            self.surface.blit(text_coins,dest=(130, 50))
            text_distance = self.game_ui_font_small.render("Distance: " + str(self.total_distance), True, (0, 0, 0))
            self.surface.blit(text_distance,dest=(250, 50))

        else:
            self.surface.fill((220, 100, 10))
            #Render text
            self.surface.blit(self.text_game_over,dest=(130, 100))

            text_coins = self.game_ui_font_small.render("You collected " + str(self.map.n_coins) + " coins. Good job!", True, (0, 0, 0))
            self.surface.blit(text_coins,dest=(130, 250))
            text_distance = self.game_ui_font_small.render("Total distance is " + str(self.total_distance) + ". Not bad!", True, (0, 0, 0))
            self.surface.blit(text_distance,dest=(130, 300))

        #Draw hand marker based on hand position
        self.hand_tracking.draw_hands(self.surface)    
        
    def update_player_movement(self):
        #Update player position according to right hand
        end_pos = self.hand_tracking.retrieve_player_pos()
        self.player.update_moving_dir(end_pos)
    
    def timer_start_end(self, timer_running):
        #If timer was not running last frame, reset timer
        if not self.running_last_frame and timer_running:
            self.timer = 0
            self.timer_start = pygame.time.get_ticks()
            print("TIMER HAS STARTED")
        elif timer_running:
            self.timer = pygame.time.get_ticks() - self.timer_start 
            print("current time: ", self.timer)    

        if self.timer > TIMER_LIMIT :
            self.timer = 0
            self.timer_start = pygame.time.get_ticks()
            
            if self.game_state == State.RUNNING:
                self.game_state = State.END
            else:
                self.game_state = State.RUNNING

        self.running_last_frame = timer_running
   
    def update(self):
        #60 fps
        self.clock.tick(FPS)

        self.load_camera()

        #Draw landmarks and process hand positions in videocam
        self.frame = self.hand_tracking.process_hands(self.frame)

        #Process hand gestures, 
        timerRunning = self.hand_tracking.process_hand_gestures()
        
        #Timer for start/end gesture
        self.timer_start_end(timerRunning)

        #Update player pos
        self.player.move_player()

        #Drawing all object in the game
        self.draw()       
        
        #Controlling if the player have collied with a block, true -> end game
        if self.map.block_collision(self.player.hitbox):
            self.game_state = State.END
        
        #Show webcam with landmarks on screen
        cv2.imshow("Frame", cv2.flip(self.frame, 1))
        cv2.waitKey(1) 

        pygame.display.update()