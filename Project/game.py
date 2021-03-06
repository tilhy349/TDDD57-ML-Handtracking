import pygame
import cv2
from hand_tracking import HandTracking
from settings import *
from player import Player
from map import Map
from powerup import PowerupHandler
from ui import UI

class Game:
    def __init__(self, surface):
        self.surface = surface
       
        #Load camera (webcam)
        self.cap = cv2.VideoCapture(0) 

        self.clock = pygame.time.Clock()

        self.game_state = State.MENU

        self.hand_tracking = HandTracking()
        self.player = Player()
        self.map = Map()
        self.powerup = PowerupHandler()
        self.ui = UI(self.surface)

        self.game_speed = GAME_SPEED_INITIAL
        self.last_time = 0
        self.timer = 0

        self.image_point = pygame.transform.scale( pygame.image.load("Project\Images\Point.png"), (10, 10)).convert_alpha()
        self.IMAGE_HAND_FRAME = pygame.transform.scale(pygame.image.load("Project\Images\Hand_frame.png"), (X_SCALE, Y_SCALE)).convert_alpha()

    def load_camera(self):
        #Store the current frame from webcam
        _, self.frame = self.cap.read()
    
    def draw_running(self):
        #Draw map
        self.map.draw(self.surface)

        blit_alpha(self.surface, self.IMAGE_HAND_FRAME, [X_DISPLACEMENT, Y_DISPLACEMENT], 100)

        #Draw pointer
        blit_alpha(self.surface, self.image_point, self.hand_tracking.retrieve_player_pos(), 140)

        #Draw the player 
        self.player.draw_player(self.surface)
        
    def update_player_movement(self):
        #Update player position according to right hand
        end_pos = self.hand_tracking.retrieve_player_pos()
        self.player.update_moving_dir(end_pos)
    
    def timer_start_end(self, dt):
        
        if self.hand_tracking.current_gesture == Gesture.START_END:
            self.timer += dt / 60
        else:
            self.timer = 0
        
        if self.timer > TIMER_LIMIT:
            self.timer = 0

            if self.game_state == State.RUNNING:
                self.game_state = State.END
            else:
                self.game_state = State.RUNNING
                self.reset_game() 

    def run_game(self, dt):
        self.draw_running()
        self.ui.draw_ui_game(self.map.n_coins, self.map.total_distance, self.powerup.available_powerups)
            
        #Update player pos
        self.player.move_player(dt) 
            
        #Set and process current power up
        self.powerup.set(self.hand_tracking.current_gesture)
        self.map.n_coins = self.powerup.process(dt, self.map.n_coins)

        #Update player color depending on powerup
        self.player.player_image = self.powerup.player_image
            
        #Controlling if the player have collided with a block, true -> end game
        if self.map.block_collision(self.player.hitbox, self.powerup.current_powerup == Powerup.INVISIBLE):
            self.game_state = State.END   

        if self.powerup.current_powerup != Powerup.SLOWMOTION:
            #Check time and update movement speed
            self.map.update_map_movement(self.game_speed, dt)
        else:
            self.map.update_map_movement(SLOWMOTION_SPEED, dt)

    def reset_game(self):
        self.map = Map()
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.powerup = PowerupHandler()
        
        self.last_time = pygame.time.get_ticks() * 0.001
            
    def update(self):

        self.load_camera()

        #calculating dt, the time between this frame and the last frame
        dt = pygame.time.get_ticks() * 0.001 - self.last_time
        dt *= 60
        self.last_time = pygame.time.get_ticks() * 0.001

        #Draw landmarks and process hand positions in videocam
        self.frame = self.hand_tracking.process_hands(self.frame)

        #Process hand gestures, 
        self.hand_tracking.process_hand_gestures()
        
        #Timer for start/end gesture
        self.timer_start_end(dt)

        #Draw depending on the current state
        if self.game_state == State.MENU:
            self.ui.draw_ui_menu(self.timer)
        elif self.game_state == State.RUNNING:
            self.run_game(dt)
        else:
            self.ui.draw_ui_end(self.map.total_distance, self.timer)

        #Draw hand marker based on hand position
        self.hand_tracking.draw_hands(self.surface) 
        
        #Show webcam with landmarks on screen
        #cv2.imshow("Frame", cv2.flip(self.frame, 1))
        #cv2.waitKey(1) 

        pygame.display.update()
        self.clock.tick(FPS)