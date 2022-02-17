import pygame
import time
import enum
import math

from settings import *

class State(enum.Enum):
    SELECTED = 1
    HOVERED = 2
    UNSELECTED = 3

class Box:

    def __init__(self, xcoord, ycoord, width, height, color):
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.width = width
        self.height = height
        self.rect = pygame.Rect(xcoord, ycoord, width, height)

        self.width_org = width
        self.height_org = height

        self.current_state = State.UNSELECTED
        
        self.color = color
        self.color_org = color
        self.selected_color = self.color_org + pygame.Color(100, 100, 100)
        self.hover_color = self.color_org + pygame.Color(60, 60, 60)

        self.BORDER = (self.width if self.width < self.height else self.height ) * 0.66

        #low limit and high limit for hover-border
        self.BORDER = 10 if self.BORDER < 10 else self.BORDER
        self.BORDER = 40 if self.BORDER > 40 else self.BORDER

        self.deselect_rect_top = pygame.Rect(xcoord, ycoord - self.BORDER, self.width, self.BORDER)
        self.deselect_rect_right = pygame.Rect(xcoord + width, ycoord - self.BORDER, self.BORDER, height + self.BORDER * 2)
        self.deselect_rect_bottom = pygame.Rect(xcoord, ycoord + height, self.width, self.BORDER)
        self.deselect_rect_left = pygame.Rect(xcoord - self.BORDER, ycoord - self.BORDER, self.BORDER, height + self.BORDER * 2)

    def collide_box(self, hands):
        #Controll if marker is on the Box
        return self.rect.colliderect(hands.rect_hitbox) 

    def collide_border(self, hands):
        #Controll if marker is in any of the deactivation hitboxes
        coll_deact1 = self.deselect_rect_top.colliderect(hands.rect_hitbox)
        coll_deact2 = self.deselect_rect_right.colliderect(hands.rect_hitbox)
        coll_deact3 = self.deselect_rect_bottom.colliderect(hands.rect_hitbox)
        coll_deact4 = self.deselect_rect_left.colliderect(hands.rect_hitbox)

        return coll_deact1 or coll_deact2 or coll_deact3 or coll_deact4 

    def process_state(self, hands):
        if PINCH_TO_SELECT:

            allowed_to_select = self.current_state == State.SELECTED or not hands.selected_box

            #If marker is inside the box, and the left hand is pinching
            if self.collide_box(hands) and hands.left_hand_gesture == Gesture.PINCH and allowed_to_select:
                self.current_state = State.SELECTED 
                self.update_pos_selected(hands)
                hands.selected_box = True
            #If the marker is inside the border of the box, or inside the box BUT NOT pinching
            elif not hands.selected_box and (self.collide_border(hands) or self.collide_box(hands)):
                self.current_state = State.HOVERED 
                self.xcoord = self.rect.x
                self.ycoord = self.rect.y
                hands.selected_box = False
            elif (not self.collide_box(hands) or hands.left_hand_gesture != Gesture.PINCH) and self.current_state == State.SELECTED:
                print("UNSELECTED")
                self.current_state = State.UNSELECTED
                self.xcoord = self.rect.x
                self.ycoord = self.rect.y  
                hands.selected_box = False
            else:
                self.current_state = State.UNSELECTED         

    def update_size(self, angle):
        value = math.cos(angle - math.pi/2) + 1 #0 - 1 --> degrees -90 to 90

        self.rect.update(self.xcoord, self.ycoord, self.width_org * value, self.height_org * value)

        self.width = self.rect.width
        self.height = self.rect.height
        
        self.deselect_rect_top.update(self.xcoord, 
                self.ycoord - self.BORDER, self.width, self.BORDER)
        self.deselect_rect_right.update(self.xcoord + self.width, 
                self.ycoord - self.BORDER, self.BORDER, self.height + self.BORDER * 2)
        self.deselect_rect_bottom.update(self.xcoord, 
                self.ycoord + self.height, self.width, self.BORDER)
        self.deselect_rect_left.update(self.xcoord - self.BORDER, 
                self.ycoord - self.BORDER , self.BORDER, self.height + self.BORDER * 2)
        

    def update_pos_selected(self, hands):
        #print("current pos = ", curr_pos)
        
        curr_pos = (hands.marker_pos[0], hands.marker_pos[1])
        selected_pos = (hands.selected_point[0], hands.selected_point[1])

        self.deselect_rect_top.update(self.xcoord - (selected_pos[0] - curr_pos[0]), 
                self.ycoord - self.BORDER - (selected_pos[1] - curr_pos[1]), self.width, self.BORDER)
        self.deselect_rect_right.update(self.xcoord + self.width - (selected_pos[0] - curr_pos[0]), 
                self.ycoord - self.BORDER - (selected_pos[1] - curr_pos[1]), self.BORDER, self.height + self.BORDER * 2)
        self.deselect_rect_bottom.update(self.xcoord - (selected_pos[0] - curr_pos[0]), 
                self.ycoord + self.height - (selected_pos[1] - curr_pos[1]), self.width, self.BORDER)
        self.deselect_rect_left.update(self.xcoord - self.BORDER - (selected_pos[0] - curr_pos[0]), 
                self.ycoord - self.BORDER - (selected_pos[1] - curr_pos[1]), self.BORDER, self.height + self.BORDER * 2)

        #Also make it imposible to have multiple boxes selected at once
        self.rect.update(self.xcoord - (selected_pos[0] - curr_pos[0]), self.ycoord - (selected_pos[1] - curr_pos[1]), self.width, self.height)
            
    def draw(self, surface):
        
        #Set the right color
        if self.current_state == State.SELECTED:
            self.color = self.selected_color
        #Set hover on box that indecate that it can be selected
        elif self.current_state == State.HOVERED:
            self.color = self.hover_color
        else:
            self.color = self.color_org
        
        #Draw all hitbox
        #pygame.draw.rect(surface, (100, 0, 100), self.deselect_rect_top, 1)
        #pygame.draw.rect(surface, (100, 0, 100), self.deselect_rect_right, 1)
        #pygame.draw.rect(surface, (100, 0, 100), self.deselect_rect_bottom, 1)
        #pygame.draw.rect(surface, (100, 0, 100), self.deselect_rect_left, 1)
        
        #Draw the box
        pygame.draw.rect(surface, self.color, self.rect)

        #If selected, draw border
        if self.current_state == State.SELECTED:
            pygame.draw.rect(surface, (255, 255, 255), self.rect, 4)
     