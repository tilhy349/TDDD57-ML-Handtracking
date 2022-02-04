import pygame
import time

class Box:

    def __init__(self, xcoord, ycoord, width, height, color):
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.width = width
        self.height = height
        self.color = color
        self.color_org = color
        self.hover_color = self.color + pygame.Color(60, 60, 60)
        self.rect = pygame.Rect(xcoord, ycoord, height, width)

        self.start_clock = False
        self.time_hover = 0
        self.selected = False

    def hover(self, state):
        if state:
            self.color = self.hover_color
        else:
            self.color = self.color_org
         
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        if self.selected:
            #Draw frame
            pygame.draw.rect(surface, (255, 255, 255), self.rect, 1)

    def collide(self, hitbox):
        
        collision = self.rect.colliderect(hitbox)
        #collision = False
        print("Coords: ", hitbox.center)

        self.hover(collision)
        print("Collision: ", collision)
        #First time hover over, set start time 
        if collision and self.start_clock == False:
            self.start_time_hover = time.time()
            #print("Start clock:  = ", self.start_time_hover)
            self.start_clock == True
        elif collision:
            #continue counting
            print("Collision = ", collision)
            self.time_hover = time.time() - self.start_time_hover            
        else:
            #reset time
            self.start_clock = False
            self.time_hover = 0
            
        #If hover long enough, select box
        #print("Current hover time = ", self.time_hover)
        if self.time_hover > 3000:
            self.selected = True

         