"""Main module, defines FastAPI endpoints."""

from fastapi import FastAPI, Query
from datetime import datetime
import random
import os

import ens_fake_weather_data.constants as cst
from ens_fake_weather_data.fake_data import generate_temperature

# Retrieve parameters from environment variables
sampling_interval = os.environ.get(cst.SAMPLING_FREQUENCY, default=cst.DEFAULT_SAMPLING_INTERVAL)
percentage_missing_data = float(os.environ.get(cst.PERCENTAGE_MISSING_DATA, default=cst.DEFAULT_PERCENTAGE_MISSING_DATA))/100
GENERATION_PARAMETERS = {
    cst.SAMPLING_FREQUENCY: sampling_interval,
    cst.PERCENTAGE_MISSING_DATA: percentage_missing_data,
}

app = FastAPI()


@app.get("/weather/")
async def get_weather(
    start_date: datetime = Query(..., description="The start date of the data."),
    end_date: datetime = Query(..., description="The end date of the data."),
    latitude: float = Query(..., description="The latitude of the location."),
    longitude: float = Query(..., description="The longitude of the location."),
):
    data = generate_temperature(
        start_date=start_date,
        end_date=end_date,
        latitude=latitude,
        longitude=longitude,
        generation_parameters=GENERATION_PARAMETERS,
    )
    return data
