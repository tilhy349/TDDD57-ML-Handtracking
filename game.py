import pygame
import time
import random
import cv2
import mediapipe as mp
from hand import Hand

class Game:
    def __init__(self, surface):
        self.surface = surface
        self.surface.fill((255,255,255))

        #Load camera (webcam)
        self.cap = cv2.VideoCapture(0) 

        self.start_time = time.time()

        self.hands = Hand()


    def load_camera(self):
        #Store the current frame from webcam
        _, self.frame = self.cap.read()
    
    def draw(self):
        #Draw
        curr_time = time.time() - self.start_time

        # Initialing Color
        #color = (255,0,0)
        #self.surface.fill((255,255,255))
        # Drawing Rectangle
        #pygame.draw.rect(self.surface, color, pygame.Rect(30 * curr_time, 30, 60, 60))

        
    def update(self):
        self.load_camera()
        self.draw()

        #Draw landmarks and process hand positions
        self.frame = self.hands.process_hands(self.frame)
        
        #Draw hand marker based on hand position
        self.hands.draw_marker(self.surface)
        
        #Show webcam with landmarks on screen
        cv2.imshow("Frame", cv2.flip(self.frame, 1))
        cv2.waitKey(1)
        
        pygame.display.update()