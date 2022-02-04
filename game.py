import pygame
import time
import random
import cv2
import mediapipe as mp
from hand import Hand
from box import Box

class Game:
    def __init__(self, surface):
        self.surface = surface
        self.surface.fill((255,255,255))

        #Load camera (webcam)
        self.cap = cv2.VideoCapture(0) 

        self.start_time = time.time()

        self.hands = Hand()

        self.box1 = Box(100, 100, 50, 50, pygame.Color(220, 0, 0))
        self.box2 = Box(200, 100, 40, 40, pygame.Color(0, 220, 0))
        self.box3 = Box(250, 100, 100, 100, pygame.Color(0, 0, 220))


    def load_camera(self):
        #Store the current frame from webcam
        _, self.frame = self.cap.read()
    
    def draw(self):
        #Draw
        curr_time = time.time() - self.start_time

        # Initialing Color
        self.surface.fill((0,0,0))

        # Drawing Rectangle, Rect(left, top, width, height)
        self.box1.draw(self.surface)
        self.box2.draw(self.surface)
        self.box3.draw(self.surface)
    
    def check_hand_pos(self):
        self.box1.collide(self.hands.rect_hitbox)
        self.box2.collide(self.hands.rect_hitbox)
        self.box3.collide(self.hands.rect_hitbox)     
        
    def update(self):
        self.load_camera()

        #Draw landmarks and process hand positions
        self.frame = self.hands.process_hands(self.frame)

        #Compare hand position to boxes
        #Change color saturation if marker is covering one of the boxes
        self.check_hand_pos()

        self.draw()       
        
        #Draw hand marker based on hand position
        self.hands.draw_marker(self.surface)
        
        #Show webcam with landmarks on screen
        cv2.imshow("Frame", cv2.flip(self.frame, 1))
        cv2.waitKey(1)
        
        pygame.display.update()