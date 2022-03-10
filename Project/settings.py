import enum
import pygame

#---- General settings ---
# Define constants for the screen width and height
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

GAME_WIDTH = SCREEN_WIDTH - 500
GAME_DISPLACEMENT = int((SCREEN_WIDTH - GAME_WIDTH) /2) # 250

#FPS
FPS = 60

#Settings for game state
class State(enum.Enum):
    MENU = 1
    RUNNING = 2
    END = 3

#Timer limit for starting/ending game
TIMER_LIMIT = 3

#------ Player settings -----

#Specified delay for updating player movement
DELAY = 200

COLOR_ORIGINAL = (0, 0, 0)

PLAYER_WIDTH = 30
PLAYER_HEIGHT = PLAYER_WIDTH * 1.1

class PlayerImage(enum.Enum):
    DEFAULT = 1
    PEACE = 2
    CLOSE = 3

#--- Handgestures setting ---
#Settings for gesture

class Gesture(enum.Enum):
    START_END = 1
    DEFAULT = 2
    CLOSE = 3
    PEACE = 4
    
#Colors for different hand gestures
COLOR_PEACE = (236, 64, 122)
COLOR_CLOSE = (48, 79, 254)
COLOR_START_END = (118, 255, 3)

#Size for hand rects
SIZE_HAND_RECT = 10

#Thresholds for hand gestures
PEACE_THRESHOLD = 50
CLOSE_THRESHOLD = 25
PINCH_THRESHOLD = 30
START_END_THRESHOLD = 45

#Scaling for the hand display
X_SCALE = 400
Y_SCALE = 300

Y_DISPLACEMENT = 300
X_DISPLACEMENT = (SCREEN_WIDTH - X_SCALE) / 2

#--- Map settings ---
#Map settings
MAP_NUMBER_COLS = 5

MAP_BLOCK_WIDTH = int(GAME_WIDTH / MAP_NUMBER_COLS)
MAP_BLOCK_HEIGHT = 50

#Spawn rates
SPAWN_RATE_OBJECT = 0.3
SPAWN_RATE_COIN = 0.3
SPAWN_RATE_BLOCK = 0.7

#Map movement settings
GAME_SPEED_INITIAL = 1
GAME_SPEED_UPDATE = 3000
SPEED_UPDATE_STEP = 0.1

class CoinImage(enum.Enum):
    FRONT1 = 1
    FRONT2 = 2
    FRONT3 = 3
    FRONT4 = 4
    SIDE = 5
    BACK1 = 6
    BACK2 = 7
    BACK3 = 8

#--- Powerup settings ---
class Powerup(enum.Enum):
    INVISIBLE = 1
    SLOWMOTION = 2
    SPAWN_COINS = 3
    DEFAULT = 4

#Number of powerups the player can have
MAX_POWERUPS = 3

#Number of coins that is needed to get a powerup
POWERUP_COST = 8

#Variables to change color on the player when the power is reaching its end
POWERUP_TIME_LIMIT = 5
POWERUP_ENDING_LIMIT = POWERUP_TIME_LIMIT - 2 #When 2 seconds remain
POWERUP_BLINK_STEP = 0.3 #Blink every 1/4 second

#The game speed the game should get when using the power slowmotion
SLOWMOTION_SPEED = 0.5

def blit_alpha(target, source, location, opacity):
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-location[0], -location[1]))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        target.blit(temp, location)


