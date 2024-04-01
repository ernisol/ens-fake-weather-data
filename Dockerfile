FROM python:3.9-slim

WORKDIR /app

# Creating a virtual environment and installing dependencies first to leverage caching.
RUN python3 -m venv venv
RUN pip install -U pip wheel setuptools
COPY pyproject.toml setup.py requirements.txt /app/
RUN pip install -r requirements.txt

# Installing the module
COPY ens_fake_weather_data /app/ens_fake_weather_data/
RUN pip install . --no-deps

# Configuring environment variables
ENV SAMPLING_FREQUENCY "1h"
ENV PERCENTAGE_MISSING_DATA "10"


# Run the service on port 9865
CMD ["uvicorn", "ens_fake_weather_data.main:app", "--host", "0.0.0.0", "--port", "9865"]
