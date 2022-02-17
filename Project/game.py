import pygame
import time
import random
import cv2
import mediapipe as mp
from HandTracking import HandTracking
from player import Player

class Game:
    def __init__(self, surface):
        self.surface = surface
        self.surface.fill((255,255,255))

        #Load camera (webcam)
        self.cap = cv2.VideoCapture(0) 

        self.start_time = time.time()

        self.hand_tracking = HandTracking()

        self.player = Player()

    def load_camera(self):
        #Store the current frame from webcam
        _, self.frame = self.cap.read()
    
    #Drawing all object in the game
    def draw(self):

        # Initialing Color
        self.surface.fill((255,255,255))
        
        #Draw hand marker based on hand position
        self.hand_tracking.draw_hands(self.surface)
        
        #Draw the player 
        self.player.draw_player(self.surface)        
    
    def update_player_movement(self):
        #Update player position according to right hand
        end_pos = self.hand_tracking.retrieve_player_pos()
        self.player.update_moving_dir(end_pos)
   
    def update(self):
        self.load_camera()

        #Draw landmarks and process hand positions in videocam
        self.frame = self.hand_tracking.process_hands(self.frame)

        #Updat player pos
        self.player.move_player()

        #Drawing all object in the game
        self.draw()       
        
        #Show webcam with landmarks on screen
        cv2.imshow("Frame", cv2.flip(self.frame, 1))
        cv2.waitKey(1)
        
        pygame.display.update()