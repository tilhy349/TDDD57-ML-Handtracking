import enum

#---- General settings ---
# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

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
#Limits for the player movement area
PLAYER_LIMIT_UP = 50
PLAYER_LIMIT_DOWN = 370

#Specified delay for updating player movement
DELAY = 200
PLAYER_VELOCITY = 5

COLOR_ORIGINAL = (255, 0, 0)

#--- Handgestures setting ---
#Settings for gesture

class Gesture(enum.Enum):
    START_END = 1
    DEFAULT = 2
    CLOSE = 3
    PEACE = 4
    
#Colors for different hand gestures
COLOR_PEACE = (250, 0, 250)
COLOR_CLOSE = (10, 10, 255)
COLOR_START_END = (0, 255, 0)

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
X_DISPLACEMENT = 200

#--- Map settings ---
#Map settings
MAP_NUMBER_COLS = 8

MAP_BLOCK_WIDTH = int(SCREEN_WIDTH / MAP_NUMBER_COLS)
MAP_BLOCK_HEIGHT = 50

#Spawn rates
SPAWN_RATE_OBJECT = 0.3
SPAWN_RATE_COIN = 0.3
SPAWN_RATE_BLOCK = 0.7

#Map movement settings
GAME_SPEED_INITIAL = 2
GAME_SPEED_UPDATE = 3000
SPEED_UPDATE_STEP = 0.1


#--- Powerup settings ---
class Powerup(enum.Enum):
    INVISIBLE = 1
    SLOWMOTION = 2
    SPAWN_COINS = 3
    DEFAULT = 4

#Number of powerups the player can have
MAX_POWERUPS = 3

#Number of coins that is needed to get a powerup
POWERUP_COST = 3

#Variables to change color on the player when the power is reaching its end
POWERUP_TIME_LIMIT = 5
POWERUP_ENDING_LIMIT = POWERUP_TIME_LIMIT - 2 #When 2 seconds remain
POWERUP_BLINK_STEP = 0.25 #Blink every 1/4 second

#The game speed the game should get when using the power slowmotion
SLOWMOTION_SPEED = 0.5

