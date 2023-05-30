import os
import json
import glob


def read_latest_scrapped_data():
    list_of_scrapped = glob.glob('./scrapped_data/*.json')
    latest_scrap = max(list_of_scrapped, key=os.path.getctime)
    with open(latest_scrap, "r") as jsondata:
        data = json.load(jsondata)
    return data
