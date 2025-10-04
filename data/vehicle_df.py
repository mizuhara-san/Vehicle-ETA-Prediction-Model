
import os
import pandas as pd        
os.chdir(r"C:\Users\tazee\.spyder-py3")
# 1. Load the dataset you created in the previous step
df = pd.read_csv('vehicle_data.csv')
# 2. Preprocessing: Convert 'start_time' from text to a real datetime object
# This is crucial for extracting time-based features.
df['start_time'] = pd.to_datetime(df['start_time'])

# 3. Feature Engineering: Create new columns from 'start_time'
# These new features will be the input for our model.

# Extract the hour of the day (0-23)
df['hour_of_day'] = df['start_time'].dt.hour

# Extract the day of the week (Monday=0, Sunday=6)
df['day_of_week'] = df['start_time'].dt.dayofweek

# You can even create a simple 'is_weekend' feature (1 for weekend, 0 for weekday)
# df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)


# --- Verification ---
# Display the first few rows to see your new feature columns
print("DataFrame with new features:")
print(df[['start_time', 'hour_of_day', 'day_of_week', 'distance_km', 'travel_time_minutes']].head())