from random import randint, choice, random, uniform
# from pyplant.pots.data import water_levels, light_levels
import matplotlib.pyplot as plt
import numpy as np

light_levels = [
    {
        'id': 1,
        'description': 'full sun (+21,500 lux /+2000 fc )',
        'temp': {
            'low_level': 21,
            'high_level': 40
        }
    },
    {
        'id': 2,
        'description': 'strong light ( 21,500 to 3,200 lux/2000 to 300 fc)',
        'temp': {
            'low_level': 16,
            'high_level': 28
        }
    },
    {
        'id': 3,
        'description': 'diffuse light ( Less than 5,300 lux / 500 fc)',
        'temp': {
            'low_level': 12,
            'high_level': 24
        }
    }
]

water_levels = [
    {
        'id': 1,
        'description': 'keep moist between watering  &  must not dry between watering',
        'moisture': {
            'low_level': 50,
            'high_level': 100
        }
    },
    {
        'id': 2,
        'description': 'change water regularly in the cup  &  water when soil is half dry',
        'moisture': {
            'low_level': 40,
            'high_level': 100
        }
    },
    {
        'id': 3,
        'description': 'keep moist between watering  &  water when soil is half dry',
        'moisture': {
            'low_level': 40,
            'high_level': 60
        }
    },
    {
        'id': 4,
        'description': 'must dry between watering  &  water only when dry',
        'moisture': {
            'low_level': 10,
            'high_level': 100
        }
    },
    {
        'id': 5,
        'description': 'do not water',
        'moisture': {
            'low_level': 0,
            'high_level': 30
        }
    },
]


class IotReading():

    def __init__(self, water_id, light_id, careful=False):
        self.water_id = water_id
        self.light_id = light_id
        self.careful = careful
        self.generate_fresh_data()

    def generate_fresh_data(self, num_data_points=5):
        # generate list of data
        moisture_data = []
        temp_data = []
        for _ in range(num_data_points):
            _temp, _moisture = self.new_readings()
            moisture_data.append(_moisture)
            temp_data.append(_temp)

        # visualize data
        fig, ax1 = plt.subplots()
        ax1.scatter(range(num_data_points), moisture_data, color='lightgreen')
        ax1.set_xlabel('Reading id')
        ax1.set_ylabel('Soil Moisture Level', color='lightgreen')
        ax1.set_title('Pyplant IoT readings')

        # Plot for Temperature
        ax2 = ax1.twinx()
        ax2.scatter(range(num_data_points), temp_data, color='coral')
        ax2.set_ylabel('Temp Level', color='coral')

        # connect the dots
        for i in range(num_data_points - 1):
            ax1.plot([i, i + 1], [moisture_data[i],
                     moisture_data[i + 1]], color='lightgreen')
            ax2.plot([i, i + 1], [temp_data[i],
                     temp_data[i + 1]], color='coral')

        # Set color for dots outside expected
        temp_low, temp_high = self._get_temp_expected_levels()
        moist_low, moist_high = self._get_moisture_expected_levels()
        for i in range(num_data_points):
            if moisture_data[i] < moist_low:
                ax1.scatter(
                    i, moisture_data[i], color='blue', marker='^', s=50)
            if moisture_data[i] > moist_high:
                ax1.scatter(
                    i, moisture_data[i], color='red', marker='^', s=50)
            if temp_data[i] < temp_low:
                ax2.scatter(i, temp_data[i], color='blue',
                            marker='x', s=50)
            if temp_data[i] > temp_high:
                ax2.scatter(i, temp_data[i], color='red',
                            marker='x', s=50)

        # Set x-axis tick labels
        x_labels = [
            f'({i+1})' for i in range(num_data_points)]
        ax1.set_xticks(range(num_data_points))
        ax1.set_xticklabels(x_labels)

        # Create a custom legend for error markers
        error_markers = [plt.Line2D([], [], color='blue', marker='x', markersize=8, linestyle='None'),
                         plt.Line2D([], [], color='red', marker='^', markersize=8, linestyle='None')]
        error_labels = ['Moisture Error', 'Temperature Error']
        ax1.legend(error_markers, error_labels)

        # save to svg
        plt.savefig('./pyplant/static/chart.svg')

        # table
        # Create the table data
        table_data = [
            [''] + ['reading {}'.format(i + 1)
                    for i in range(len(moisture_data))],
            ['moisture'] + [str(val) for val in moisture_data],
            ['temp'] + [str(val) for val in temp_data]
        ]

        # Create the table plot
        fig, ax = plt.subplots()

        # Hide the axes
        ax.axis('off')

        # Create the table
        table = ax.table(cellText=table_data, colLabels=None,
                         cellLoc='center', loc='center')

        # Color the moisture data outside the range in red
        for i, val in enumerate(moisture_data):
            if val < moist_low or val > moist_high:
                table[(1, i + 1)].set_facecolor('red')

        print(temp_low, temp_high)
        for i, val in enumerate(temp_data):
            if val < temp_low or val > temp_high:
                table[(2, i + 1)].set_facecolor('red')

        # Adjust the table appearance
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)  # Adjust the table size

        # Hide the axes
        ax.set_axis_off()

        # save
        plt.savefig('./pyplant/static/table.svg',
                    bbox_inches='tight', pad_inches=0)

    def print_levels(self):
        for level in water_levels:
            if level["id"] == self.water_id:
                print(
                    f"Plant water level: {level['description']}, in range {level['moisture']['low_level']}-{level['moisture']['high_level']}%RH")
        for level in light_levels:
            if level["id"] == self.light_id:
                print(
                    f"Plant light level: {level['description']}, in range {level['temp']['low_level']}-{level['temp']['high_level']}degC")

    def update_level(self, plant_level):
        self.plant_level = plant_level
        self.print_level()

    def update_care(self, careful):
        self.careful = careful
        print("Nice, you commited to care about the plant. chances are it will live") if careful else print(
            "Your plant is now in hands of Gods...")

    def new_readings(self):
        return self.read_temp(), self.read_moisture()

    def current_readings(self):
        return self.current_air_temp, self.current_soil_moisture

    def read_moisture(self):
        expected_low_trashold, expected_high_trashold = self._get_moisture_expected_levels()
        self.current_soil_moisture = self._generate_dummy(
            expected_low_trashold, expected_high_trashold, 4, 100)
        print(f"Read moisture: {self.current_soil_moisture}%RH")
        return self.current_soil_moisture

    def read_temp(self):
        expected_low_trashold, expected_high_trashold = self._get_temp_expected_levels()
        self.current_air_temp = self._generate_dummy(
            expected_low_trashold, expected_high_trashold, 4, 44)
        print(f"Read temp: {self.current_air_temp}degC")
        return self.current_air_temp

    def _generate_dummy(self, expected_low_trashold, expected_high_trashold, range_min, range_max):
        if not self.careful:
            return randint(range_min, range_max)
        else:
            _probability = random()
            if _probability < 0.75:
                # 75% probability to be within range
                return randint(expected_low_trashold, expected_high_trashold)
            else:
                # 25% probabiliy to be out of expected range
                return choice(list(range(range_min, expected_low_trashold)) + list(range(expected_high_trashold, range_max)))

    def _get_moisture_expected_levels(self):
        for level in water_levels:
            if level['id'] == self.water_id:
                return level['moisture']['low_level'], level['moisture']['high_level']

    def _get_temp_expected_levels(self):
        for level in light_levels:
            if level['id'] == self.light_id:
                return level['temp']['low_level'], level['temp']['high_level']


p = IotReading(water_id=1, light_id=1, careful=False)
