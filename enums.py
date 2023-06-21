import json
import pygame
import python.data_processing.distributions as distributions

DATA_PATH_OLD = ""
DATA_PATH = ""  # Where to import from
NEW_DATA_PATH = ""  # Where to put the processed data

#  ------------------------------------------------------------ Data  --------------------------------------------------------------------------------

# Insulin activity, if changed, reprocess the data
INSULIN_ACTIVITY_FUNCTION = distributions.gamma
INSULIN_ACTIVITY_DELAY = 0  # 12.28 minutes, we already incorperate it in the activation function
INSULIN_STEP_SIZE = 0.05
INSULIN_LOW = 3
INSULIN_HIGH = 10
GLUCOSE_BASELINE_LEVEL = 4.5  # mmol/L

with open('./config.json', 'r') as json_file:
    json_load = json.load(json_file)
