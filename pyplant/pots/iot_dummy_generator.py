from random import randint, choice, random
from pyplant.pots.data import PH_MIN, PH_MAX, SALT_MIN, SALT_MAX, MOIST_MIN, MOIST_MAX, TEMP_MIN, TEMP_MAX, water_levels, light_levels
import json
import os


class IotReading():

    def __init__(self, water_id, light_id, careful=False, num_data_points=5):
        self.water_id = water_id
        self.light_id = light_id
        self.careful = careful
        try:
            self.generate_fresh_data(num_data_points=num_data_points)
        except Exception as ex:
            print(f"ERROR on creating visual data, ex: {ex}")

    def generate_fresh_data(self, num_data_points):
        # generate lists of data
        moisture_data = []
        temp_data = []
        ph_data = []
        salt_data = []
        for _ in range(num_data_points):
            _temp, _moisture, _ph, _salt = self.new_readings()
            moisture_data.append(_moisture)
            temp_data.append(_temp)
            ph_data.append(_ph)
            salt_data.append(_salt)

        data = {
            'num_data_points': num_data_points,
            'moisture_data': moisture_data,
            'temp_data': temp_data,
            'ph_data': ph_data,
            'salt_data': salt_data,
            'expected_levels': self.get_expected_levels_list()
        }

        # matplotlib wouldnot work if it's not run from main
        # save to json file so it can be consumed by plotter
        with open("./pyplant/pots/generated_data/data.json", 'w') as file:
            json.dump(data, file, indent=4)
        # generate chart and table from json file
        script_path = os.path.join(os.getcwd(), "scripts", "data_plotter.py")
        os.system('{} {}'.format('python', script_path))

    def print_levels(self):
        for level in water_levels:
            if level["id"] == self.water_id:
                print(
                    f"Plant water level: {level['description']}, in range {level['moisture']['low_level']}-{level['moisture']['high_level']}%RH")
        for level in light_levels:
            if level["id"] == self.light_id:
                print(
                    f"Plant light level: {level['description']}, in range {level['temp']['low_level']}-{level['temp']['high_level']}degC")

    def print_current_levels(self):
        try:
            print(f"Current temp: {self.current_air_temp}")
            print(f"Current moist: {self.current_soil_moisture}")
            print(f"Current pH: {self.current_ph}")
            print(f"Current salt: {self.current_salt}")
        except Exception as ex:
            print(f"get the readings first, ex: {ex}")

    def update_level(self, plant_level):
        self.plant_level = plant_level
        self.print_level()

    def update_care(self, careful):
        self.careful = careful
        print("Nice, you commited to care about the plant. chances are it will live") if careful else print(
            "Your plant is now in hands of Gods...")

    def new_readings(self):
        return self.read_temp(), self.read_moisture(), self.read_ph(), self.read_salt()

    def current_readings(self):
        return self.current_air_temp, self.current_soil_moisture, self.current_ph, self.current_salt

    def read_moisture(self, moist_low=None, moist_high=None):
        expected_low_trashold, expected_high_trashold = self._get_moisture_expected_levels()
        _moist_low = moist_low if moist_low else MOIST_MIN
        _moist_high = moist_high if moist_high else MOIST_MAX
        self.current_soil_moisture = self._generate_dummy(expected_low_trashold, expected_high_trashold,
                                                          _moist_low, _moist_high)
        return self.current_soil_moisture

    def read_temp(self, temp_min=None, temp_max=None):
        expected_low_trashold, expected_high_trashold = self._get_temp_expected_levels()
        _temp_min = temp_min if temp_min else TEMP_MIN
        _temp_max = temp_max if temp_max else TEMP_MAX
        self.current_air_temp = self._generate_dummy(expected_low_trashold, expected_high_trashold,
                                                     _temp_min, _temp_max)
        return self.current_air_temp

    def read_ph(self, ph_min=None, ph_max=None):
        _ph_min = ph_min if ph_min else PH_MIN
        _ph_max = ph_max if ph_max else PH_MAX
        self.current_ph = self._generate_dummy(PH_MIN, PH_MAX,
                                               _ph_min, _ph_max)
        return self.current_ph

    def read_salt(self, salt_min=None, salt_max=None):
        _salt_min = salt_min if salt_min else SALT_MIN
        _salt_max = salt_max if salt_max else SALT_MAX
        self.current_salt = self._generate_dummy(SALT_MIN, SALT_MAX,
                                                 _salt_min, _salt_max)
        return self.current_salt

    def _generate_dummy(self, expected_low_trashold, expected_high_trashold, range_min, range_max):
        if not self.careful:
            return randint(range_min, range_max)
        else:
            _probability = random()
            if _probability < 0.85:
                # 85% probability to be within range
                ret = randint(expected_low_trashold, expected_high_trashold)
            elif _probability > 0.9:
                # 10% probability to be higher than range
                ret = randint(expected_high_trashold, range_max)
            else:
                # 5% probabiliy to be lower than range
                ret = randint(range_min, expected_low_trashold)
            return ret

    def get_expected_levels_list(self):
        _t_min, _t_max = self._get_temp_expected_levels()
        _m_min, _m_max = self._get_moisture_expected_levels()
        print(f"t max= {_t_max}")
        print(f"t min= {_t_min}")
        print(f"m max= {_m_max}")
        print(f"m min= {_m_min}")
        return [_t_min, _t_max, _m_min, _m_max]

    def _get_moisture_expected_levels(self):
        for level in water_levels:
            if level['id'] == self.water_id:
                return level['moisture']['low_level'], level['moisture']['high_level']

    def _get_temp_expected_levels(self):
        for level in light_levels:
            if level['id'] == self.light_id:
                return level['temp']['low_level'], level['temp']['high_level']


if __name__ == "__main__":
    iot = IotReading(water_id=1, light_id=1)
