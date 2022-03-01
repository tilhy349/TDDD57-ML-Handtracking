
# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#FPS
FPS = 60

#Limits for the player movement area
PLAYER_LIMIT_UP = 50
PLAYER_LIMIT_DOWN = 370

#Scaling for the hand display
X_SCALE = 400
Y_SCALE = 300

Y_DISPLACEMENT = 300
X_DISPLACEMENT = 200

#Specified delay for updating player movement
DELAY = 200
PLAYER_VELOCITY = 5

#Timer for state changes
TIMER_LIMIT = 2000

#Settings for gesture
import enum
class Gesture(enum.Enum):
    START_END = 1
    DEFAULT = 2
    CLOSE = 3
    PEACE = 4

#Settings for game state
class State(enum.Enum):
    MENU = 1
    RUNNING = 2
    END = 3

#Thresholds for hand gestures
PEACE_THRESHOLD = 30
CLOSE_THRESHOLD = 25
PINCH_THRESHOLD = 30
START_END_THRESHOLD = 45

#Map settings
MAP_NUMBER_COLS = 8

MAP_BLOCK_WIDTH = int(SCREEN_WIDTH / MAP_NUMBER_COLS)
MAP_BLOCK_HEIGHT = 50

#Spawn rates
SPAWN_RATE_OBJECT = 0.3
SPAWN_RATE_COIN = 0.3
SPAWN_RATE_BLOCK = 0.7

#Movement speed
MAP_SPEED = 1
MAP_UPDATE_SPEED = 30 
SPAWN_RATE_ROW = int(2 * MAP_BLOCK_HEIGHT / (MAP_SPEED / MAP_UPDATE_SPEED))

