# -*- coding: utf-8 -*-
"""
Created on Sat Oct  4 11:47:01 2025

@author: tazee
"""

import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import folium
from streamlit_folium import st_folium

# --- App Configuration ---
st.set_page_config(page_title="Vehicle Tracking Dashboard", layout="wide")
st.title("Vehicle ETA Prediction Dashboard 🗺️")

# --- Model Training (cached to run only once) ---
@st.cache_resource
def train_model():
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
    
    return model, df

model, df = train_model()

# --- Interactive Sidebar ---
st.sidebar.header("Select a Trip")
# Create a slider to select a trip ID from 0 to 499
trip_id = st.sidebar.slider("Trip ID", 0, len(df) - 1, 0)

# --- Main Panel ---
# Get the data for the selected trip
trip_data = df.iloc[trip_id]

# Use the model to predict ETA for the selected trip
features_for_prediction = [
    [trip_data['distance_km'], trip_data['hour_of_day'], trip_data['day_of_week']]
]
predicted_time = model.predict(features_for_prediction)[0]

# Display metrics
st.subheader(f"Analysis for Trip ID: {trip_id}")
col1, col2 = st.columns(2)
col1.metric("Actual Travel Time", f"{trip_data['travel_time_minutes']:.2f} min")
col2.metric("Predicted Travel Time", f"{predicted_time:.2f} min")

# Display the map for the selected trip
st.subheader("Trip Route")
start_point = (trip_data['start_lat'], trip_data['start_lon'])
end_point = (trip_data['end_lat'], trip_data['end_lon'])

m = folium.Map(location=start_point, zoom_start=12)
folium.Marker(location=start_point, popup='Start', icon=folium.Icon(color='green')).add_to(m)
folium.Marker(location=end_point, popup='End', icon=folium.Icon(color='red')).add_to(m)
folium.PolyLine(locations=[start_point, end_point], color='blue').add_to(m)

# Render the map in the Streamlit app
st_folium(m, width=1200, height=500)