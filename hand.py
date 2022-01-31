import mediapipe as mp
import cv2
import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

class Hand:

    def __init__(self):
        
        self.hands = mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

        self.hand_center_x = 0
        self.hand_center_y = 0

        self.results = None

        #self.rect_hitbox = pygame.draw.circle(self.)

    def draw_marker(self, surface):
        color = (255,255,0)
        marker = pygame.Rect(30, 30, 60, 60)
        marker.center = (self.hand_center_x, self.hand_center_y)

        pygame.draw.rect(surface, color, marker)
        #Draw 

    def process_hands(self, frame):
                   
        #Prestanda
        frame.flags.writeable = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(frame)
            
        #Draw the hand annotations on the image.
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                #Get position of landmark 9 (mittenknogen (vid långfingret)) 
                x, y = hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y
                
                #Store position of hand in game window
                self.hand_center_x = SCREEN_WIDTH - int(x * SCREEN_WIDTH)
                self.hand_center_y = int(y * SCREEN_HEIGHT)
                
                #draw the the landmarks on the hand in the video
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())  
        return frame 
