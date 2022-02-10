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

        self.boxes = [Box(100, 100, 50, 100, pygame.Color(220, 20, 20)), 
                      Box(250, 100, 60, 40, pygame.Color(220, 20, 180)), 
                      Box(500, 100, 100, 100, pygame.Color(20, 20, 220))]
        
        self.areas = [pygame.Rect(300, 400, 150, 150), 
                      pygame.Rect(500, 400, 70, 50), 
                      pygame.Rect(600, 400, 80, 120)]

    def load_camera(self):
        #Store the current frame from webcam
        _, self.frame = self.cap.read()
    
    def draw(self):
        #Draw
        #curr_time = time.time() - self.start_time

        # Initialing Color
        #self.surface.fill((0,0,0))
        
        #Draw rectangles to insert the boxes in
        pygame.draw.rect(self.surface, (66, 150, 178), self.areas[0], 1)
        pygame.draw.rect(self.surface, (66, 150, 178), self.areas[1], 1)
        pygame.draw.rect(self.surface, (66, 150, 178), self.areas[2], 1)
    
    def process_boxes(self):
        #Check accuracy of the boxes
        self.check_accuracy()

        for i in range(len(self.boxes)):
            self.boxes[i].process_state(self.hands)
            self.boxes[i].draw(self.surface)

    #Set the background to green if all boxes is inside a rectangle
    def check_accuracy(self):
        nr_of_boxes_true = 0

        for i in self.boxes:
            for j in self.areas:
                if j.contains(i):
                    nr_of_boxes_true += 1

        if nr_of_boxes_true == len(self.boxes):
            self.surface.fill((0, 100, 0))
        else:
            self.surface.fill((0, 0, 0))
            
   
    def update(self):
        self.load_camera()

        #Draw landmarks and process hand positions
        self.frame = self.hands.process_hands(self.frame)

        #Process boxes
        self.process_boxes()

        #Draw
        self.draw()       
        
        #Draw hand marker based on hand position
        self.hands.draw_marker(self.surface)
        
        #Show webcam with landmarks on screen
        cv2.imshow("Frame", cv2.flip(self.frame, 1))
        cv2.waitKey(1)
        
        pygame.display.update()