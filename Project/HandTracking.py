import mediapipe as mp
import cv2
import pygame
import math
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

        self.player_new_pos = [0, 0]

        self.right_hand_landmarks = []
        self.left_hand_landmarks = []

        self.current_gesture = Gesture.DEFAULT

    #Not the best solution, TODO: fix
    def draw_hands(self, surface):
        size = 10
        left_color = (0,0,0)
        right_color = (0,0,0)

        #Set color depending on current gesture
        if self.current_gesture == Gesture.START_END:
            left_color = (0, 255, 0)
            right_color = (0, 255, 0)
        elif self.current_gesture == Gesture.PEACE:
            right_color = (255, 0, 255)
        elif self.current_gesture == Gesture.CLOSE:
            right_color = (10, 10, 255)
            
        if not self.results.multi_hand_landmarks:
            return

        #If hand label is right or if two hands are in play, draw right hand
        if (self.results.multi_handedness[0].classification[0].label == "Right"
            or len(self.results.multi_hand_landmarks) > 1):

            for i in self.right_hand_landmarks:
                pygame.draw.rect(surface, right_color, pygame.Rect(i[0], i[1], size, size))

        #If hand label is left or if two hands are in play, draw left hand
        if (self.results.multi_handedness[0].classification[0].label == "Left"
            or len(self.results.multi_hand_landmarks) > 1):

             for inx, i in enumerate(self.left_hand_landmarks):
                if inx == 8:
                    pygame.draw.rect(surface, (255,0,0), pygame.Rect(i[0], i[1], size, size))
                else:
                    pygame.draw.rect(surface, left_color, pygame.Rect(i[0], i[1], size, size))
                

    def scale_landmarks(self, landmarks):   
        tempList = [] #Empty list
        #Scale based on settings
        for i in landmarks:
            #tempList.append([SCREEN_WIDTH - int(i.x * SCREEN_WIDTH), int(i.y * SCREEN_HEIGHT)])
            tempList.append([X_SCALE - int(i.x* X_SCALE) + X_DISPLACEMENT, int(i.y * Y_SCALE) + Y_DISPLACEMENT])
        
        return tempList
    
    #Retuning the position of right hand (pekfingres knoge)
    def retrieve_player_pos(self):
        return [SCREEN_WIDTH - int(self.player_new_pos[0] * SCREEN_WIDTH), int(self.player_new_pos[1] * SCREEN_HEIGHT)]

    def start_end_gesture(self):
        if not self.results.multi_hand_landmarks or len(self.results.multi_hand_landmarks) < 2:
            return Gesture.DEFAULT

        distRight = math.hypot(self.right_hand_landmarks[8][0] - self.right_hand_landmarks[4][0],
            self.right_hand_landmarks[8][1] - self.right_hand_landmarks[4][1])
        distLeft = math.hypot(self.left_hand_landmarks[8][0] - self.left_hand_landmarks[4][0],
            self.left_hand_landmarks[8][1] - self.left_hand_landmarks[4][1])
            
        distStartEnd = math.hypot(self.left_hand_landmarks[4][0] - self.right_hand_landmarks[4][0],
            self.left_hand_landmarks[4][1] - self.right_hand_landmarks[4][1])
         
        conditionRight = (self.right_hand_landmarks[12][1] < self.right_hand_landmarks[9][1] and
                     self.right_hand_landmarks[16][1] < self.right_hand_landmarks[13][1] and
                     self.right_hand_landmarks[20][1] < self.right_hand_landmarks[17][1])
        conditionLeft = (self.left_hand_landmarks[12][1] < self.left_hand_landmarks[9][1] and
                     self.left_hand_landmarks[16][1] < self.left_hand_landmarks[13][1] and
                     self.left_hand_landmarks[20][1] < self.left_hand_landmarks[17][1])
        
        if (distRight < PINCH_THRESHOLD and distLeft < PINCH_THRESHOLD and
             distStartEnd < START_END_THRESHOLD and conditionRight and conditionLeft): 
            return Gesture.START_END
        return Gesture.DEFAULT

    def peace_hand_gesture(self):
        #dist =  math.hypot(self.right_hand_landmarks[14][0] - self.right_hand_landmarks[4][0],
        #self.right_hand_landmarks[14][1] - self.right_hand_landmarks[4][1])

        isPeace = (self.right_hand_landmarks[8][1] < self.right_hand_landmarks[7][1] and
                   self.right_hand_landmarks[7][1] < self.right_hand_landmarks[6][1] and
                   self.right_hand_landmarks[6][1] < self.right_hand_landmarks[5][1] and
                   
                   self.right_hand_landmarks[12][1] < self.right_hand_landmarks[11][1] and 
                   self.right_hand_landmarks[11][1] < self.right_hand_landmarks[10][1] and
                   self.right_hand_landmarks[10][1] < self.right_hand_landmarks[9][1] and
                   
                   self.right_hand_landmarks[16][1] > self.right_hand_landmarks[13][1] and
                   self.right_hand_landmarks[20][1] > self.right_hand_landmarks[17][1])
        
        if isPeace: #and dist < PEACE_THRESHOLD :
            return Gesture.PEACE
        return Gesture.DEFAULT
    
    
    def closed_hand_gesture(self):
        
        #dist =  math.hypot(self.right_hand_landmarks[14][0] - self.right_hand_landmarks[4][0],
        #self.right_hand_landmarks[14][1] - self.right_hand_landmarks[4][1])
        
        isClosed = (self.right_hand_landmarks[8][1] > self.right_hand_landmarks[5][1] and
                    self.right_hand_landmarks[12][1] > self.right_hand_landmarks[9][1] and 
                    self.right_hand_landmarks[16][1] > self.right_hand_landmarks[13][1] and
                    self.right_hand_landmarks[20][1] > self.right_hand_landmarks[17][1])
             #self.right_hand_landmarks[4][0] < self.right_hand_landmarks[6][0])
        
        if isClosed : #and dist < CLOSE_THRESHOLD: 
            return Gesture.CLOSE
        return Gesture.DEFAULT
       
    def process_hand_gestures(self):
        #Make sure landmarks is not empty
        if len(self.left_hand_landmarks) == 0 or len(self.right_hand_landmarks) == 0:
            return
          
        if self.start_end_gesture() == Gesture.START_END:
            self.current_gesture = Gesture.START_END
                 
        elif self.peace_hand_gesture() == Gesture.PEACE:
            #print("peace hand gest")
            self.current_gesture = Gesture.PEACE
        elif self.closed_hand_gesture() == Gesture.CLOSE: 
            #print("stängd hand gest")
            self.current_gesture = Gesture.CLOSE
        else:
            #print("default gest")
            self.current_gesture = Gesture.DEFAULT
            
    
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
                    self.player_new_pos = [hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y]
                    self.left_hand_landmarks = self.scale_landmarks(hand_landmarks.landmark)
                
                #draw the the landmarks on the hand in the video
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())  
                       
        return frame 


