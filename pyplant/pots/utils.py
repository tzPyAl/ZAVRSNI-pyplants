import os
import json
import glob
from pyplant.pots.data import water_levels, CAREFUL_PYPLANTER
from pyplant.pots.iot_dummy_generator import IotReading


def read_latest_scrapped_data():
    list_of_scrapped = glob.glob('./scrapped_data/*.json')
    latest_scrap = max(list_of_scrapped, key=os.path.getctime)
    with open(latest_scrap, "r") as jsondata:
        data = json.load(jsondata)
    return data


def get_plant_status(light_level_id, water_level_id, temp_min, temp_max):
    iot_readings = IotReading(water_id=water_level_id,
                              light_id=light_level_id,
                              careful=CAREFUL_PYPLANTER)
    _temp_now = iot_readings.current_air_temp
    _moist_now = iot_readings.current_soil_moisture
    _moist_low, _moist_high = _get_trashold_from_water_levels(water_level_id)

    iot_readings.print_current_levels()

    if _temp_now <= temp_min:
        status = 1
    elif _temp_now >= temp_max:
        status = 2
    else:
        status = 0
    if _moist_now <= _moist_low:
        status = status + 3
    elif _moist_now >= _moist_high:
        status = status + 6

    print(f"STATUS: {status}")

    return status


def _get_trashold_from_water_levels(water_level_id):
    for level in water_levels:
        if water_level_id == level['id']:
            return level['moisture']['low_level'], level['moisture']['high_level']
