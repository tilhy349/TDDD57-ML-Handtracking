import mediapipe as mp
import cv2
import pygame
import math
from settings import *

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

class Hand:

    def __init__(self):
        #Variables for hand tracking
        self.hands = mp_hands.Hands(
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

        self.results = None

        #Variables for right hand 
        self.marker_pos = [0, 0]

        self.pinching = False
        self.start_pinch = False

        self.is_rockNroll = False

        self.right_hand_gesture = Gesture.OPEN
        self.left_hand_gesture = Gesture.OPEN

        self.rect_hitbox = pygame.Rect(0, 0, 30, 30)

        #Variables for color handling
        self.color = (255, 255, 0)
        self.color_org = (255, 255, 0)
        self.color_pinch = (255, 255, 255)
        self.color_close = (0, 255, 255)
        
        self.selected_box = False
        self.selected_point = (0, 0)  

        self.tracking = [0, 0]  

    def draw_marker(self, surface):

        #Change color on marker depending on hand gesture
        if self.left_hand_gesture == Gesture.PINCH:
            self.color = self.color_pinch
        elif self.left_hand_gesture == Gesture.CLOSE:
            self.color = self.color_close
        else:
            self.color = self.color
        
        pygame.draw.circle(surface, self.color, (self.marker_pos[0], self.marker_pos[1]),15)
        self.rect_hitbox.center = (self.marker_pos[0] , self.marker_pos[1])
        #pygame.draw.rect(surface, (255, 255, 255), self.rect_hitbox, 2)

    #PLAN FOR ROTATION
    #STORE Initial thumb value when doing pose first time
    #Compare angle between (vector from new thumb pos to base of hand)
    #and vector from initial thumb pos to base of hand
    #angle = cos-1(len(a)/len(b))
    #0 to 180 degrees --> angle sets color value
    
    #Obs: hand_label is mirrored!
    def process_gesture(self, hand_landmarks, hand_label):
       
        #If the gesture on the left hand is pinch --> update gesture
        if hand_label == "Left" and self.gesture_pinch(hand_landmarks):
           self.left_hand_gesture = Gesture.PINCH
        
        #If the left hand is closed--> update gesture
        elif hand_label == "Left" and self.gesture_close(hand_landmarks):
            self.left_hand_gesture = Gesture.CLOSE
       
        # elif hand_label == "Right" and self.gesture_rotate(hand_landmarks):
        #     self.right_hand_gesture = Gesture.ROTATE
            
        elif hand_label == "Left":
            self.left_hand_gesture = Gesture.OPEN  
       
        elif hand_label == "Right":
            self.right_hand_gesture = Gesture.OPEN  

        #-------------
        #If the gesture on the left hand is not close, update marker after left hand
        if hand_label == "Left" and self.left_hand_gesture != Gesture.CLOSE:
            
            #Get position of landmark 5 (Toppen på pekfingret knoge)) 
            x, y = hand_landmarks.landmark[5].x, hand_landmarks.landmark[5].y

            #Store position of index finger in game window
            self.marker_pos[0] = SCREEN_WIDTH - int(x * SCREEN_WIDTH)
            self.marker_pos[1] = int(y * SCREEN_HEIGHT) 
        
        #If the gesture on the left hand is close, store the indexfinger pos
        elif hand_label == "Right" and self.left_hand_gesture == Gesture.CLOSE:
            x, y = hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y  

            self.tracking[0] = SCREEN_WIDTH - int(x * SCREEN_WIDTH)
            self.tracking[1] = int(y * SCREEN_HEIGHT) 

            
        
    def gesture_pinch(self, hand_landmarks):
        dist = math.hypot(hand_landmarks.landmark[8].x - hand_landmarks.landmark[4].x,
        hand_landmarks.landmark[8].y - hand_landmarks.landmark[4].y)
         
        condition = (hand_landmarks.landmark[12].y < hand_landmarks.landmark[9].y and
                     hand_landmarks.landmark[16].y < hand_landmarks.landmark[13].y and
                     hand_landmarks.landmark[20].y < hand_landmarks.landmark[17].y)
        
        if dist < PINCH_THRESHOLD and condition:
            #self.color =  self.color_pinch 
            
            if not self.start_pinch:
                self.start_pinch = True
                self.selected_point = (self.marker_pos[0], self.marker_pos[1])
                
            return True
        else:
            self.color =  self.color_org
            self.start_pinch = False
            
            return False
    
    def gesture_close(self, hand_landmarks):
        condition = (hand_landmarks.landmark[8].y > hand_landmarks.landmark[5].y and
            hand_landmarks.landmark[12].y > hand_landmarks.landmark[9].y and
            hand_landmarks.landmark[16].y > hand_landmarks.landmark[13].y and
            hand_landmarks.landmark[20].y > hand_landmarks.landmark[17].y)
        
        #self.selected_point = (self.marker_pos[0], self.marker_pos[1])

        return condition

    def gesture_rotate(self, hand_landmarks):
        
        return False


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
                
                #Get the lable of the hand (Right or Left), it is mirrored!!
                hand_label = self.results.multi_handedness[idx].classification[0].label

                # Process the hands landmark points,
                self.process_gesture(hand_landmarks, hand_label)
                
                #draw the the landmarks on the hand in the video
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())  
                        
        #print("Left hand gesture = ", self.left_hand_gesture)   
        #print("Right hand gesture = ", self.right_hand_gesture, "\n")     
        return frame 


