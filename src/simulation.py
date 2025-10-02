import numpy as np

# Crop data
CROPS = {
    "Rice": {
        "base_yield": 5.0,  # tons/ha
        "water_need": 1200,  # mm/season
        "fertilizer_opt": 100,  # kg/ha
        "drought_resistant": False
    },
    "Maize": {
        "base_yield": 8.0,
        "water_need": 500,
        "fertilizer_opt": 150,
        "drought_resistant": True
    }
}

def calculate_yield(crop, irrigation, fertilizer, rainfall, temperature):
    """
    Calculate crop yield based on decisions and climate.
    """
    crop_data = CROPS[crop]
    base = crop_data["base_yield"]

    # Fertilizer effect: optimal gives +20%, over/under reduces
    fert_factor = 1 + 0.2 * (1 - abs(fertilizer - crop_data["fertilizer_opt"]) / crop_data["fertilizer_opt"])

    # Water effect: irrigation supplements rainfall
    total_water = rainfall + irrigation
    water_factor = min(1.5, total_water / crop_data["water_need"])
    if total_water > crop_data["water_need"] * 1.2:  # Overuse penalty
        water_factor *= 0.8

    # Climate: high temp reduces yield
    temp_factor = 1 - max(0, (temperature - 25) / 50)  # Penalty above 25C

    yield_val = base * fert_factor * water_factor * temp_factor
    return max(0, yield_val)

def calculate_sustainability(irrigation, fertilizer, crop, rainfall):
    """
    Calculate sustainability score (0-100).
    """
    score = 100

    # Water overuse penalty
    crop_data = CROPS[crop]
    total_water = rainfall + irrigation
    if total_water > crop_data["water_need"] * 1.5:
        score -= 30

    # Fertilizer overuse
    if fertilizer > crop_data["fertilizer_opt"] * 1.5:
        score -= 20

    # Drought consideration
    if rainfall < crop_data["water_need"] * 0.5 and not crop_data["drought_resistant"]:
        score -= 10

    return max(0, score)

def simulate_season(crop, irrigation, fertilizer, avg_rainfall, avg_temp):
    """
    Simulate a farming season.
    """
    yield_val = calculate_yield(crop, irrigation, fertilizer, avg_rainfall, avg_temp)
    sustain = calculate_sustainability(irrigation, fertilizer, crop, avg_rainfall)
    return yield_val, sustain