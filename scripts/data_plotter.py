import matplotlib.pyplot as plt
import json
from datetime import datetime
from random import randint


def plot():
    with open('./pyplant/pots/generated_data/data.json', "r") as file:
        data = json.load(file)

    plot_chart(num_data_points=data['num_data_points'],
               moisture_data=data['moisture_data'],
               temp_data=data['temp_data'],
               expected_levels=data['expected_levels'])
    plot_table(moisture_data=data['moisture_data'],
               temp_data=data['temp_data'],
               ph_data=data['ph_data'],
               salt_data=data['salt_data'],
               expected_levels=data['expected_levels'])


def plot_chart(num_data_points, moisture_data, temp_data, expected_levels):
    # visualize data
    fig, ax1 = plt.subplots()
    ax1.scatter(range(num_data_points),
                moisture_data, color='lightgreen')
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
    temp_low, temp_high, moist_low, moist_high = _parse_expedted_levels(
        expected_levels)
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


def _get_parsed_time_list(length):
    hh = datetime.now().strftime("%H")
    mm = int(datetime.now().strftime("%M")) + 10
    date_stamp = datetime.now().strftime("%d.%m")
    _list = []

    for _ in range(length):
        hh = int(hh)
        mm = int(mm)
        mm = mm - 10
        if mm < 0:
            mm = mm + 60
            hh = hh - 1
        if mm < 10:
            mm = "0" + str(mm)
        if hh < 10:
            hh = "0" + str(hh)
        _str = date_stamp + " " + \
            str(hh) + ":" + str(mm) + ":" + str(randint(10, 59))
        _list.append(_str)

    _list.reverse()
    print(_list)
    return _list


def plot_table(moisture_data, temp_data, ph_data, salt_data, expected_levels):
    # Create the table data
    _number_or_readings = len(moisture_data)
    readings_time_list = _get_parsed_time_list(_number_or_readings)

    table_data = [
        # [''] + ['reading {}'.format(i + 1)
        #         for i in range(len(moisture_data))],
        [''] + readings_time_list,
        ['moisture [%RH]'] + [str(val) for val in moisture_data],
        ['temp [degC]'] + [str(val) for val in temp_data],
        ['pH [pH]'] + [str(val) for val in ph_data],
        ['salt [%]'] + [str(val) for val in salt_data]
    ]

    # Create the table plot
    fig, ax = plt.subplots()

    # Hide the axes
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=table_data, colLabels=None,
                     cellLoc='center', loc='center')
    _all_list = []
    for i in range(_number_or_readings+1):
        _all_list.append(i)
    table.auto_set_column_width(col=_all_list)

    # Color the moisture data outside the range in red
    temp_low, temp_high, moist_low, moist_high = _parse_expedted_levels(
        expected_levels)
    for i, val in enumerate(moisture_data):
        if val < moist_low or val > moist_high:
            table[(1, i + 1)].set_facecolor('red')

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


def _parse_expedted_levels(expected_levels):
    return expected_levels[0], expected_levels[1], expected_levels[2], expected_levels[3]


if __name__ == "__main__":
    plot()
