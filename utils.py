import json, os
from datetime import datetime, timedelta

from concurrent.futures import ThreadPoolExecutor, as_completed

DATA_FOLDER = ["data/risk_scoring", "data/rapid_succession"]




def load_data(data_path):
    with open (data_path) as data:
        data = json.load(data)
    return data

def write_data(data_path, data):
    with open(data_path, 'w') as f:
        json.dump(data, f, indent=4)
