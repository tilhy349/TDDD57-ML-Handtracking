import pygame
import time

from settings import PINCH_TO_SELECT

class Box:

    def __init__(self, xcoord, ycoord, width, height, color):
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.width = width
        self.height = height
        self.rect = pygame.Rect(xcoord, ycoord, height, width)
        
        self.color = color
        self.color_org = color
        self.selected_color = self.color_org + pygame.Color(100, 100, 100)
        self.hover_color = pygame.Color(255, 60, 60)
        self.hover = False

        self.selected = False

        BORDER = 50

        self.deselect_rect_top = pygame.Rect(xcoord, ycoord - BORDER, self.width, BORDER)
        self.deselect_rect_right = pygame.Rect(xcoord + width, ycoord - BORDER, BORDER, height + BORDER * 2)
        self.deselect_rect_bottom = pygame.Rect(xcoord, ycoord + height, self.width, BORDER)
        self.deselect_rect_left = pygame.Rect(xcoord - BORDER, ycoord - BORDER, BORDER, height + BORDER * 2)

    def hover(self, state):
        if state:
            self.color = self.hover_color
        else:
            self.color = self.color_org
         
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
        pygame.draw.rect(surface, (100, 0, 100), self.deselect_rect_top, 1)
        pygame.draw.rect(surface, (100, 0, 100), self.deselect_rect_right, 1)
        pygame.draw.rect(surface, (100, 0, 100), self.deselect_rect_bottom, 1)
        pygame.draw.rect(surface, (100, 0, 100), self.deselect_rect_left, 1)
        
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

        #State (b-delen)
        # if PINCH_TO_SELECT:
        #     #Inside box and pinching
        #     activation = collision_activate and hands.check_pinching()
        #     #Outside box (inside border) or not pinching
        #     deactivation = coll_deact and hands.check_pinching() == False
        #     #Inside border
        #     #(a-delen)
        # else:
        #     activation = collision_activate
        #     deactivation = coll_deact 

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
            if collision_activate and hands.check_pinching():
                self.selected = True
                self.hover = False
            elif coll_deact or collision_activate:
                self.hover = True
                self.selected = False
            else:
                self.hover = False


        print(self.hover)
        
        
     
         