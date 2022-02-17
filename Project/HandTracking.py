import mediapipe as mp
import cv2
import pygame
from settings import *

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

class HandTracking:

    def __init__(self):
        #Variables for hand tracking
        self.hands = mp_hands.Hands(
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

        self.results = None

        self.right_hand_landmarks = []
        self.left_hand_landmarks = []

    #Not the best solution, TODO: fix
    def draw_hands(self, surface):
        if not self.results.multi_hand_landmarks:
            return

        if len(self.results.multi_hand_landmarks) > 1:
            for i in self.right_hand_landmarks:
                pygame.draw.rect(surface, (0,0,0), pygame.Rect(i[0], i[1], 20, 20))
            for i in self.left_hand_landmarks:
                pygame.draw.rect(surface, (0,0,0), pygame.Rect(i[0], i[1], 20, 20))
        elif self.results.multi_handedness[0].classification[0].label == "Right":
            for i in self.right_hand_landmarks:
                pygame.draw.rect(surface, (0,0,0), pygame.Rect(i[0], i[1], 20, 20))
        else:
            for i in self.left_hand_landmarks:
                pygame.draw.rect(surface, (0,0,0), pygame.Rect(i[0], i[1], 20, 20))
                

    def scale_landmarks(self, landmarks):   
        tempList = [] #Empty list
        
        for i in landmarks:
            tempList.append([SCREEN_WIDTH - int(i.x * SCREEN_WIDTH), int(i.y * SCREEN_HEIGHT)])
        
        return tempList
    
    #Retuning the position of right hand (pekfingres knoge)
    def retrieve_player_pos(self):
        if len(self.left_hand_landmarks) > 4 :
            return self.left_hand_landmarks[5]
        return [0,0]
    
    def process_hands(self, frame):
                   
        #Prestanda
        frame.flags.writeable = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(frame)
            
        #Draw the hand annotations on the image.
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        if self.results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(self.results.multi_hand_landmarks):
                
                #Get the label of the hand (Right or Left), it is mirrored!!
                hand_label = self.results.multi_handedness[idx].classification[0].label

                #Do deep copy of the landmarks and scale them, inserting int to the correct hand
                if hand_label == "Right": 
                    self.right_hand_landmarks = self.scale_landmarks(hand_landmarks.landmark)          
                else:
                    self.left_hand_landmarks = self.scale_landmarks(hand_landmarks.landmark)

                
                #draw the the landmarks on the hand in the video
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())  
                        
        return frame 


