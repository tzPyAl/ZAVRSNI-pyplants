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
