import enum
from unittest.mock import DEFAULT
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
#Limits for the player movement area
PLAYER_LIMIT_UP = 40
PLAYER_LIMIT_DOWN = 400

#Specified delay for updating player movement
DELAY = 200
PLAYER_VELOCITY = 4
MAX_TAIL = 4

COLOR_ORIGINAL = (0, 0, 0)

PLAYER_WIDTH = 30
PLAYER_HEIGHT = PLAYER_WIDTH * 1.1

IMAGE_PLAYER_DEFAULT = pygame.transform.scale( pygame.image.load("Project\Images\Dino_default.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
IMAGE_PLAYER_PEACE = pygame.transform.scale( pygame.image.load("Project\Images\Dino_peace.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
IMAGE_PLAYER_CLOSE = pygame.transform.scale( pygame.image.load("Project\Images\Dino_close.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))

IMAGE_PLAYER_DEFAULT_MIRROR = pygame.transform.scale( pygame.image.load("Project\Images\Dino_default_mirrored.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
IMAGE_PLAYER_PEACE_MIRROR = pygame.transform.scale( pygame.image.load("Project\Images\Dino_peace_mirrored.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
IMAGE_PLAYER_CLOSE_MIRROR = pygame.transform.scale( pygame.image.load("Project\Images\Dino_close_mirrored.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))

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

#----- UI settings -------
IMAGE_BLOCK1 = pygame.transform.scale( pygame.image.load("Project\Images\Block1.png"), (MAP_BLOCK_WIDTH, MAP_BLOCK_HEIGHT))
IMAGE_BLOCK2 = pygame.transform.scale( pygame.image.load("Project\Images\Block2.png"), (MAP_BLOCK_WIDTH, MAP_BLOCK_HEIGHT))
IMAGE_BLOCK3 = pygame.transform.scale( pygame.image.load("Project\Images\Block3.png"), (MAP_BLOCK_WIDTH, MAP_BLOCK_HEIGHT))
IMAGE_COIN = pygame.transform.scale( pygame.image.load("Project\Images\Coin.png"), (MAP_BLOCK_HEIGHT, MAP_BLOCK_HEIGHT))

IMAGE_BACKGROUND = pygame.transform.scale(pygame.image.load("Project\Images\Background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
IMAGE_BACKGROUND_MENU = pygame.transform.scale(pygame.image.load("Project\Images\Background_menu.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
IMAGE_CLOUDS_HEIGHT = 1400
IMAGE_CLOUDS = pygame.transform.scale(pygame.image.load("Project\Images\Clouds.png"), (498, IMAGE_CLOUDS_HEIGHT))
IMAGE_CLOUDS_MIRROR = pygame.transform.scale(pygame.image.load("Project\Images\Clouds_mirrored.png"), (498, IMAGE_CLOUDS_HEIGHT))

IMAGE_FRAME_LARGE = pygame.transform.scale(pygame.image.load("Project\Images\Frame.png"), (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 100))

IMAGE_HAND_FRAME = pygame.transform.scale(pygame.image.load("Project\Images\Hand_frame.png"), (X_SCALE, Y_SCALE))

#Font settings
FONT_HEIGHT = 80
FONT_SMALL_HEIGHT = 20
FONT_XS_HEIGHT = 15

# Initialize pygame
pygame.font.init()

#create fonts
UI_FONT = pygame.font.Font(pygame.font.get_default_font(), FONT_HEIGHT)
UI_FONT_SMALL = pygame.font.Font(pygame.font.get_default_font(), FONT_SMALL_HEIGHT)
UI_FONT_XS = pygame.font.Font(pygame.font.get_default_font(), FONT_XS_HEIGHT)

#Image sizes
IMAGE_START_END_WIDTH = 289/2.1
IMAGE_START_END_HEIGHT = 188/2.1
IMAGE_PEACE_WIDTH = 455/6.675
IMAGE_PEACE_HEIGHT = 767/7.67
IMAGE_CLOSE_WIDTH = 376/4.7
IMAGE_CLOSE_HEIGHT = 473/4.7

#Gesture images
IMAGE_START_END = pygame.transform.scale( pygame.image.load("Project\Images\Start_end.png"), (IMAGE_START_END_WIDTH, IMAGE_START_END_HEIGHT))
IMAGE_PEACE = pygame.transform.scale( pygame.image.load("Project\Images\Peace.png"), (IMAGE_PEACE_WIDTH, IMAGE_PEACE_HEIGHT))
IMAGE_CLOSE = pygame.transform.scale( pygame.image.load("Project\Images\Close.png"), (IMAGE_CLOSE_WIDTH, IMAGE_CLOSE_HEIGHT))

IMAGE_FRAME_SMALL = pygame.transform.scale(pygame.image.load("Project\Images\Frame.png"), (180, 160))
IMAGE_FRAME_SMALL_WIDTH = 180
IMAGE_FRAME_SMALL_HEIGHT = 160

def blit_alpha(target, source, location, opacity):
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-location[0], -location[1]))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        target.blit(temp, location)
