import pygame
import time

from settings import PINCH_TO_SELECT

class Box:

    def __init__(self, xcoord, ycoord, width, height, color):
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.width = width
        self.height = height
        self.rect = pygame.Rect(xcoord, ycoord, width, height)
        
        self.color = color
        self.color_org = color
        self.selected_color = self.color_org + pygame.Color(100, 100, 100)
        self.hover_color = self.color_org + pygame.Color(60, 60, 60)
        self.hover = False

        self.selected = False

        self.BORDER = (self.width if self.width < self.height else self.height ) * 0.66

        #low limit and high limit for hover-border
        self.BORDER = 10 if self.BORDER < 10 else self.BORDER
        self.BORDER = 40 if self.BORDER > 40 else self.BORDER

        self.deselect_rect_top = pygame.Rect(xcoord, ycoord - self.BORDER, self.width, self.BORDER)
        self.deselect_rect_right = pygame.Rect(xcoord + width, ycoord - self.BORDER, self.BORDER, height + self.BORDER * 2)
        self.deselect_rect_bottom = pygame.Rect(xcoord, ycoord + height, self.width, self.BORDER)
        self.deselect_rect_left = pygame.Rect(xcoord - self.BORDER, ycoord - self.BORDER, self.BORDER, height + self.BORDER * 2)

    def hover(self, state):
        if state:
            self.color = self.hover_color
        else:
            self.color = self.color_org

    def update_pos_selected(self, hands):
        #print("current pos = ", curr_pos)
        #print("selected = ", selected_pos)

        if self.selected:
            curr_pos = (hands.index_finger_pos[0], hands.index_finger_pos[1])
            selected_pos = (hands.selected_point[0], hands.selected_point[1])

            #print("Selected point: ", hands.selected_point)
            #print("Offset = ", (selected_pos[0] - curr_pos[0], selected_pos[1] - curr_pos[1]))

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

        if self.selected:
            self.color = self.selected_color
        #Set hover on box that indecate that it can be selected
        elif self.hover:
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
        if self.selected:
            pygame.draw.rect(surface, (255, 255, 255), self.rect, 4)


    def collide(self, hands):
        marker_hitbox = hands.rect_hitbox
        #Controll if marker is on the Box
        collision_activate = self.rect.colliderect(marker_hitbox) 
        
        #Controll if marker is in any of the deactivation hitboxes
        coll_deact1 = self.deselect_rect_top.colliderect(marker_hitbox)
        coll_deact2 = self.deselect_rect_right.colliderect(marker_hitbox)
        coll_deact3 = self.deselect_rect_bottom.colliderect(marker_hitbox)
        coll_deact4 = self.deselect_rect_left.colliderect(marker_hitbox)

        coll_deact = coll_deact1 or coll_deact2 or coll_deact3 or coll_deact4 

        #HOVER TO SELECT MODE
        if not PINCH_TO_SELECT:
            if collision_activate:
                self.selected = True
                self.hover = False
            elif coll_deact:
                self.selected = False
                self.hover = True
            else:
                self.hover = False
        #PINCH TO SELECT MODE
        else:
            #Block user from picking up multiple boxes
            allowed = self.selected or not hands.selected_box

            if collision_activate and hands.check_pinching() and allowed:
                self.selected = True
                hands.selected_box = True
                self.hover = False

            elif (coll_deact or collision_activate) and allowed:
                self.xcoord = self.rect.x
                self.ycoord = self.rect.y

                self.hover = True
                self.selected = False
                hands.selected_box = False
            else:
                #self.xcoord = self.rect.x
                #self.ycoord = self.rect.y

                self.hover = False
        #print(hands.selected_box)


        
        
     
         