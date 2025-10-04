import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# --- Part 1: Load and Prepare Data (from previous step) ---
os.chdir(r"C:\Users\tazee\.spyder-py3")
df = pd.read_csv('vehicle_data.csv')
df['start_time'] = pd.to_datetime(df['start_time'])
df['hour_of_day'] = df['start_time'].dt.hour
df['day_of_week'] = df['start_time'].dt.dayofweek

# --- Part 2: Build and Train the Model (New Step) ---

# 1. Select your features (inputs) and target (output)
features = ['distance_km', 'hour_of_day', 'day_of_week']
target = 'travel_time_minutes'

X = df[features]
y = df[target]

# 2. Split data into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Choose and train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# 4. Make predictions on the test data and evaluate the model
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)

# --- Verification ---
print("Model training complete.")
print(f"Mean Absolute Error (MAE): {mae:.2f} minutes")
print("\nThis means, on average, the model's prediction for travel time is off by about", f"{mae:.2f} minutes.")

# Optional: See a few sample predictions vs actual values
results = pd.DataFrame({'Actual Time': y_test, 'Predicted Time': predictions.round(2)})
print("\nSample Predictions:")
print(results.head())