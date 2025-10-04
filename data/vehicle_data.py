# First, make sure you have pandas installed:
# pip install pandas numpy haversine

import pandas as pd
import numpy as np
from haversine import haversine
import random
from datetime import datetime, timedelta

# --- Configuration ---
NUM_TRIPS = 500  # Number of trips to generate
DELHI_CENTER = (28.6139, 77.2090) # Center point for generating coordinates (Delhi)

# --- Data Generation ---
data = []
for i in range(NUM_TRIPS):
    # Generate random start and end points around a central location
    start_lat = DELHI_CENTER[0] + random.uniform(-0.2, 0.2)
    start_lon = DELHI_CENTER[1] + random.uniform(-0.2, 0.2)
    end_lat = DELHI_CENTER[0] + random.uniform(-0.2, 0.2)
    end_lon = DELHI_CENTER[1] + random.uniform(-0.2, 0.2)

    # Calculate distance
    distance = haversine((start_lat, start_lon), (end_lat, end_lon))

    # Generate a random start time within the last year
    start_time = datetime.now() - timedelta(days=random.randint(0, 365), hours=random.randint(0, 23))

    # Simulate travel time: base it on distance + some randomness for traffic
    # Assume an average speed between 20 to 40 km/h
    avg_speed = random.uniform(20, 40)
    base_travel_time = (distance / avg_speed) * 60  # in minutes

    # Add extra time for rush hour (8-10 AM and 5-8 PM)
    if 8 <= start_time.hour <= 10 or 17 <= start_time.hour <= 20:
        traffic_factor = random.uniform(1.3, 1.8) # 30-80% extra time
    else:
        traffic_factor = random.uniform(1.0, 1.2) # 0-20% extra time
        
    travel_time = base_travel_time * traffic_factor

    data.append({
        'trip_id': i,
        'start_lat': start_lat,
        'start_lon': start_lon,
        'end_lat': end_lat,
        'end_lon': end_lon,
        'start_time': start_time,
        'distance_km': round(distance, 2),
        'travel_time_minutes': round(travel_time, 2)
    })

# Create a pandas DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('vehicle_data.csv', index=False)

print("Successfully created 'vehicle_data.csv' with 500 simulated trips!")
print(df.head())