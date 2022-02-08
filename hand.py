import mediapipe as mp
import cv2
import pygame
import math
from settings import PINCH_THRESHOLD, SCREEN_HEIGHT, SCREEN_WIDTH

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

class Hand:

    def __init__(self):
        #Complexity of the hand landmark model: 0 or 1. 
        #Landmark accuracy as well as inference latency 
        #generally go up with the model complexity. Default to 1.
        self.hands = mp_hands.Hands(
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

        self.index_finger_pos = [0, 0]
        self.thumb_pos = [0, 0]

        self.results = None

        self.rect_hitbox = pygame.Rect(0, 0, 30, 30)
        self.color = (255, 255, 0)
        self.color_org = (255, 255, 0)
        self.color_pinch = (255, 255, 255)
        self.pinching = False

        self.selected_box = False

        self.selected_point = (0, 0)
        self.start_pinch = False

    def draw_marker(self, surface):
        
        pygame.draw.circle(surface, self.color, (self.index_finger_pos[0], self.index_finger_pos[1]),15)
        self.rect_hitbox.center = (self.index_finger_pos[0] , self.index_finger_pos[1])
        #pygame.draw.rect(surface, (255, 255, 255), self.rect_hitbox, 2)

    def check_pinching(self):
        #Calculating the distance between index finger and thumb
        dist = math.hypot(self.index_finger_pos[0]-self.thumb_pos[0], 
        self.index_finger_pos[1]-self.thumb_pos[1])
        #print(dist)
        if dist < PINCH_THRESHOLD:
            self.pinching = True
            self.color =  self.color_pinch 

            if not self.start_pinch:
                self.start_pinch = True
                self.selected_point = (self.index_finger_pos[0], self.index_finger_pos[1])
                #print("Updating selected point : ", self.selected_point)
            
        else:
            self.pinching = False
            self.color =  self.color_org
            self.start_pinch = False
            
        return self.pinching
            

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
                #Get position of landmark 9 (Toppen på pekfingret)) 
                x, y = hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y
                
                #Store position of index finger in game window
                self.index_finger_pos[0] = SCREEN_WIDTH - int(x * SCREEN_WIDTH)
                self.index_finger_pos[1] = int(y * SCREEN_HEIGHT)

                x, y = hand_landmarks.landmark[4].x, hand_landmarks.landmark[4].y

                #Store position of thumb in game window
                self.thumb_pos[0] = SCREEN_WIDTH - int(x * SCREEN_WIDTH)
                self.thumb_pos[1] = int(y * SCREEN_HEIGHT)
  
                #draw the the landmarks on the hand in the video
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())  
        return frame 
