"""Module to generate fake data."""

import numpy as np
from typing import Any, Dict
import pandas as pd
import hashlib
from datetime import datetime, timedelta

import ens_fake_weather_data.constants as cst


def generate_temperature(start_date: datetime, end_date: datetime, latitude:float, longitude: float, generation_parameters: Dict[str,Any]) -> Dict[str, float]:
    """
    Generates temperature sequence using a random walk.

    Parameters
    ----------
    start_date: datetime
        start date of the generation.
    end_date: datetime
        end date of the generation.
    latitude: float
        latitude
    longitude: float
        longitude
    generation_parameters
        Extra arguments for generation:
        - SAMPLING_INTERVAL
        - SAMPLING_INTERVAL_UNIT
        - PERCENTAGE_MISSING_DATA
    
    Returns
    -------
    Dict[str, Any]
        Randomly generated temperatures, one key for each date.
    """
    # First, generate the dates.
    dates = pd.date_range(start=start_date, end=end_date, freq=generation_parameters[cst.SAMPLING_FREQUENCY])

    generated_temperatures = {}
    temperature = cst.MIN_TEMPERATURE + (cst.MAX_TEMPERATURE - cst.MIN_TEMPERATURE) * np.random.rand()
    for date in dates:
        seed = generate_seed(date=date, latitude=latitude, longitude=longitude)
        np.random.seed(seed)
        perturbation = np.random.normal(loc=0, scale=1.5)
        temperature = get_max_temperature(date=date, latitude=latitude, longitude=longitude) + perturbation
        temperature = np.clip(temperature, a_min=cst.MIN_TEMPERATURE, a_max=cst.MAX_TEMPERATURE)

        # Adding a chance of not returning a value.
        return_point = np.random.rand() > generation_parameters[cst.PERCENTAGE_MISSING_DATA]
        if return_point:
            generated_temperatures[str(date)] = temperature
        else:
            generated_temperatures[str(date)] = None
    return generated_temperatures


def generate_seed(date, latitude, longitude):
    """
    Generates a deterministic seed based on date, latitude, and longitude.
    """
    seed_input = f"{date}{latitude}{longitude}".encode('utf-8')
    hashed = hashlib.sha256(seed_input).hexdigest()
    seed = int(hashed, 16) % (2**32)
    return seed

def get_max_temperature(date, latitude, longitude):
    time_of_day_radians = (3600 * date.hour + 60* date.minute + date.second) / 86400 * np.pi
    return cst.MIN_TEMPERATURE + np.sin(time_of_day_radians)**2 * (cst.MAX_TEMPERATURE - cst.MIN_TEMPERATURE)
