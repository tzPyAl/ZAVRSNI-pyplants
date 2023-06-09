PH_MIN = 0
PH_MAX = 8
SALT_MIN = 0
SALT_MAX = 35
MOIST_MIN = 0
MOIST_MAX = 100
TEMP_MIN = -4
TEMP_MAX = 40
CAREFUL_PYPLANTER = False


light_levels = [
    {
        'id': 1,
        'description': 'full sun (+21,500 lux /+2000 fc )',
        'temp': {
            'low_level': 21,
            'high_level': 30
        }
    },
    {
        'id': 2,
        'description': 'strong light ( 21,500 to 3,200 lux/2000 to 300 fc)',
        'temp': {
            'low_level': 16,
            'high_level': 30
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
            'low_level': 60,
            'high_level': 80
        }
    },
    {
        'id': 2,
        'description': 'change water regularly in the cup  &  water when soil is half dry',
        'moisture': {
            'low_level': 40,
            'high_level': 80
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

plant_status = {
    0: "Sweet, Your plant is happy",
    1: "Temperature is too low! Heat up the room..",
    2: "Your plant needs help. Temperature is too high!",
    3: "Time to water Your plant!",
    4: "Water the plant and heat up the room!",
    5: "Ups, Cool down the room and put some water in the soil!",
    6: "Too much water! Soil needs some drying up!",
    7: "Your plant is cold and drowning in water!",
    8: "Funny, overwatering the plant in such a hot room won't help Your plant!"
}
