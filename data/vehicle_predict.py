# First, make sure you have folium installed:
# pip install folium
import os
import pandas as pd
from sklearn.linear_model import LinearRegression
from haversine import haversine
from datetime import datetime
import folium
os.chdir(r"C:\Users\tazee\.spyder-py3")
# --- Part 1: Load Data and Train Model (condensed from previous steps) ---
df = pd.read_csv('vehicle_data.csv')
df['start_time'] = pd.to_datetime(df['start_time'])
df['hour_of_day'] = df['start_time'].dt.hour
df['day_of_week'] = df['start_time'].dt.dayofweek

features = ['distance_km', 'hour_of_day', 'day_of_week']
target = 'travel_time_minutes'
X = df[features]
y = df[target]

model = LinearRegression()
model.fit(X, y)
print("Model is trained and ready to make predictions.")


# --- Part 2: Predict and Visualize a New Trip (New Step) ---

# 1. Define a new, hypothetical trip
start_point = (28.5273, 77.2199) # Location: Saket, Delhi
end_point = (28.6315, 77.2167)   # Location: Connaught Place, Delhi
trip_time = datetime.now() # Use the current time

# 2. Prepare the features for the model
distance = haversine(start_point, end_point)
hour = trip_time.hour
day = trip_time.weekday()

# The model expects a 2D array, so we wrap our data in double brackets [[...]]
new_trip_data = [[distance, hour, day]]

# 3. Use the trained model to predict the travel time
predicted_minutes = model.predict(new_trip_data)
predicted_minutes = round(predicted_minutes[0], 2) # Get the single value from the array

print(f"\n--- New Trip Prediction ---")
print(f"Predicted travel time from Saket to Connaught Place: {predicted_minutes} minutes.")

# 4. Create an interactive map with the route and prediction
m = folium.Map(location=start_point, zoom_start=12)

# Add markers for start and end points
folium.Marker(
    location=start_point,
    popup='Start Point',
    icon=folium.Icon(color='green')
).add_to(m)

folium.Marker(
    location=end_point,
    popup=f'End Point<br><b>Predicted ETA: {predicted_minutes} mins</b>',
    icon=folium.Icon(color='red')
).add_to(m)

# Add a line for the route
folium.PolyLine(locations=[start_point, end_point], color='blue', weight=5).add_to(m)

# Save the map to an HTML file
m.save('trip_prediction_map.html')

print("\nSuccessfully created 'trip_prediction_map.html'. Open this file in your browser!")