import pygame
import time
import random
import cv2
import mediapipe as mp


class Game:
    def __init__(self, surface):
        self.surface = surface

        #Load camera (webcam)
        self.cap = cv2.VideoCapture(0) 

        self.start_time = time.time()


    def load_camera(self):
        _, self.frame = self.cap.read()
    
    def draw(self):
        #Draw
        hej = 1
        curr_time = time.time() - self.start_time

        ##surface = pygame.display.set_mode((400,300))
        # Initialing Color
        color = (255,0,0)
        self.surface.fill((255,255,255))
        # Drawing Rectangle
        pygame.draw.rect(self.surface, color, pygame.Rect(30 * curr_time, 30, 60, 60))

        def process_hands(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_hands = mp.solutions.hands

        with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
            
            #Prestanda
            self.frame.flags.writeable = False
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

            results = hands.process(self.frame)
            
            #Draw the hand annotations on the image.
            self.frame.flags.writeable = True
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        self.frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
                        
    
    def update(self):
        self.load_camera()
        self.draw()
        self.process_hands()

        cv2.imshow("Frame", self.frame)
        cv2.waitKey(1)
        pygame.display.update()