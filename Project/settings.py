# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#Limits for the player movement area
PLAYER_LIMIT_UP = 200
PLAYER_LIMIT_DOWN = 370

#Scaling for the hand display
X_SCALE = 400
Y_SCALE = 300

Y_DISPLACEMENT = 300
X_DISPLACEMENT = 200

#Specified delay for updating player movement
DELAY = 300

#Settings for gesture
import enum
class Gesture(enum.Enum):
    START_END = 1
    DEFAULT = 2
    CLOSE = 3
    PEACE = 4

class State(enum.Enum):
    MENU = 1
    RUNNING = 2
    END = 3

#Thresholds for hand gestures
PEACE_THRESHOLD = 30
CLOSE_THRESHOLD = 25
PINCH_THRESHOLD = 30
START_END_THRESHOLD = 45