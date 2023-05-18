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
