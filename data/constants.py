ISOTOPE_DATA = {
    "Tc-99m": {
        "half_life_hours": 6.01,
        "energy_kev": 140.5,
        "description": "Technetium-99m (metastable)"
    },
    "F-18": {
        "half_life_hours": 1.83,
        "energy_kev": 511.0,
        "description": "Fluorine-18 (positron emitter)"
    },
    "I-131": {
        "half_life_hours": 192.5,
        "energy_kev": 364.0,
        "description": "Iodine-131"
    },
    "Ga-67": {
        "half_life_hours": 78.3,
        "energy_kev": 93.3,
        "description": "Gallium-67"
    },
    "Tl-201": {
        "half_life_hours": 73.1,
        "energy_kev": 167.0,
        "description": "Thallium-201"
    }
}

ATTENUATION_COEFFICIENTS = {
    "Plomo": {
        100: 5.549,
        200: 1.525,
        300: 0.7854,
        400: 0.5423,
        511: 0.4103,
        600: 0.3547,
        800: 0.2683,
        1000: 0.2269,
        1500: 0.1738,
        2000: 0.1485,
        3000: 0.1216,
        5000: 0.0951,
        10000: 0.0685
    },
    "Agua": {
        100: 0.1707,
        200: 0.1370,
        300: 0.1186,
        400: 0.1061,
        511: 0.0966,
        600: 0.0896,
        800: 0.0786,
        1000: 0.0706,
        1500: 0.0575,
        2000: 0.0493,
        3000: 0.0396,
        5000: 0.0301,
        10000: 0.0221
    },
    "Hormigón": {
        100: 0.3454,
        200: 0.2706,
        300: 0.2318,
        400: 0.2066,
        511: 0.1877,
        600: 0.1741,
        800: 0.1527,
        1000: 0.1373,
        1500: 0.1117,
        2000: 0.0957,
        3000: 0.0769,
        5000: 0.0585,
        10000: 0.0429
    }
}
