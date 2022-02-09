# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#FPS
FPS = 60

#STATE
PINCH_TO_SELECT = True

#Hand settings
PINCH_THRESHOLD = 0.07

import enum
class Gesture(enum.Enum):
    PINCH = 1
    OPEN = 2
    CLOSE = 3
    ROTATE = 4