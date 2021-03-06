# Game options/settings

TITLE = "Jumpy!"
WIDTH = 480
HEIGHT = 600
FPS = 60
SPRITESHEET = "spritesheet_jumper.png"
FONT_NAME = "arial"

# Player properties

PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_JUMP_VEL = 20

# Player layers

PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER = 0

# Platforms

PLATFORM_LIST = [(0, HEIGHT-60), 
                 (WIDTH/2 - 50, HEIGHT * 3 /4),
                 (125, HEIGHT-350),
                 (350, 200),
                 (175, 100)]

# define colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE