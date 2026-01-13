# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Install system dependencies (needed for some python packages like matplotlib)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     libgl1-mesa-glx \
#  && rm -rf /var/lib/apt/lists/*
# Matplotlib generic backend shouldn't need heavy libs if we stick to 'Agg' for saving files,
# but keeping this comment for future robustness.

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual code
COPY simulation.py .

# Run simulation.py when the container launches
CMD ["python", "simulation.py"]
