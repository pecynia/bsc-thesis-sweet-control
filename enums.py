import json
import pygame
import python.data_processing.distributions as distributions

DATA_PATH_OLD = "C:/Users/verhe/OneDrive/Uni/bachelor thesis/glucose/glucose_15min.xlsx"
DATA_PATH = "C:/Users/verhe/OneDrive/Uni/bachelor thesis/data/glucose_15min.xlsx"
NEW_DATA_PATH = "C:/Users/verhe/OneDrive/Uni/bachelor thesis/python/visualization/data/data_2.csv"

#  ------------------------------------------------------------ Data  --------------------------------------------------------------------------------

# Insulin activity, if changed, reprocess the data
INSULIN_ACTIVITY_FUNCTION = distributions.gamma
INSULIN_ACTIVITY_DELAY = 0  # 20 minutes
INSULIN_STEP_SIZE = 0.05
INSULIN_LOW = 3
INSULIN_HIGH = 10
GLUCOSE_BASELINE_LEVEL = 4.5  # mmol/L

with open('C:/Users/verhe/OneDrive/Uni/bachelor thesis/python/visualization/python/data_processing/config.json', 'r') as json_file:
    json_load = json.load(json_file)



#  ------------------------------------------------------------ Visuals  --------------------------------------------------------------------------------

WHITE = (255, 255, 255)                 # tuple(map(lambda x: int(float(x)), re.findall('\d+', json_load["settings"]["colors"]["white"])))
GRAY = (100, 120, 140)                  # tuple(map(lambda x: int(float(x)), re.findall('\d+', json_load["settings"]["colors"]["gray"])))
DARK_GRAY = (60, 70, 80)
LIGHT_GRAY = (170, 180, 190)
BLACK = (15, 17, 20)                    # tuple(map(lambda x: int(float(x)), re.findall('\d+', json_load["settings"]["colors"]["black"])))

RED = (255, 69, 0)                      # tuple(map(lambda x: int(float(x)), re.findall('\d+', json_load["settings"]["colors"]["red"])))
GREEN = (0, 128, 0)                     # tuple(map(lambda x: int(float(x)), re.findall('\d+', json_load["settings"]["colors"]["green"])))
BLUE = (0, 0, 128)

# Component colors
BACKGROUND = WHITE
LINES = LIGHT_GRAY
TEXT_COLOR = DARK_GRAY

BUTTONS = LIGHT_GRAY
BUTTONS_HOVER = WHITE
BUTTONS_TEXT = BLACK

POPUP = DARK_GRAY
POPUP_LINES = GRAY

# Bars
DOWN_BAR_COLOR = GRAY
UP_BAR_COLOR = WHITE

# Screen
HORIZONTAL_OFFSET = json_load["settings"]["HORIZONTAL_OFFSET"]
VERTICAL_OFFSET = json_load["settings"]["VERTICAL_OFFSET"]
X_AXIS_TEXT = 30
X_AXIS_LINE = 40
FONT_SIZE = 12
MIN_CELLS = 50  # on chart
SENSITIVITY = json_load["settings"]["sensitivity"]

# Text
pygame.init()
font = pygame.font.SysFont('lucidaconsole', FONT_SIZE)
font_bold = pygame.font.SysFont('lucidaconsole', FONT_SIZE, bold=True)
font_big_bold = pygame.font.SysFont('lucidaconsole', round(FONT_SIZE * 1.3), bold=True)
font_medium = pygame.font.SysFont('lycidaconsole', round(FONT_SIZE * 1.5))

# ---------------------------------------------------------------------------------------------------------------------------------------------------

