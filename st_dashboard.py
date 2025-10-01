import streamlit as st
import pandas as pd 
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static 
from keplergl import KeplerGl
from datetime import datetime as dt
import plotly.express as px
from pathlib import Path

# Page config
st.set_page_config(page_title="NYC Bike Dashboard", layout="wide")
st.title("New York City Bike Dashboard")
st.write("This dashboard shows the most popular bike stations and trends of bike trips vs temperature.")

# setting dataframe path
data = Path("C:/Users/faisa/Desktop/Data analysis/Python Specialization/Achievement 2/02 Data/Updated Data/df_2.4.csv")

# loading the merged dataframe of weather + trips
df = pd.read_csv(data, index_col=0)

# create trips column
df['trips'] = 1

# Top stations bar chart
top_stations = df['start_station_name'].value_counts().head(10).reset_index()
top_stations.columns = ['station', 'trips']

fig_bar = px.bar(top_stations, x='station', y='trips', 
                 color='trips', color_continuous_scale='Viridis',
                 title='Top 10 Most Popular Bike Stations')
fig_bar.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig_bar, use_container_width=True)

# Dual-axis line chart
daily_data = df.groupby('date').agg({'trips':'sum', 'temperature':'mean'}).reset_index()

fig_line = go.Figure()
fig_line.add_trace(go.Scatter(x=daily_data['date'], y=daily_data['trips'], name='Trips', yaxis='y1', mode='lines+markers'))
fig_line.add_trace(go.Scatter(x=daily_data['date'], y=daily_data['temperature'], name='Temperature', yaxis='y2', mode='lines', line=dict(dash='dash')))

fig_line.update_layout(
    title='Daily Bike Trips vs Temperature',
    xaxis=dict(title='Date'),
    yaxis=dict(title='Number of Trips'),
    yaxis2=dict(title='Temperature (°C)', overlaying='y', side='right')
)

st.plotly_chart(fig_line, use_container_width=True)

# Kepler map
st.subheader("NYC Bike Trips Map")
st.write("Interactive map of bike trips.")

# Load pre-generated Kepler HTML
with open("2.5_Citibike_bike_trips.html", "r", encoding="utf-8") as f:
    kepler_html = f.read()

st.components.v1.html(kepler_html, height=600, scrolling=True)