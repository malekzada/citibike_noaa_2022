import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime as dt
from PIL import Image
import numerize
import streamlit.components.v1 as components
import os

########################### Initial settings for the dashboard ####################################################

st.set_page_config(page_title='Citibike Strategy Dashboard', layout='wide')
st.title("Citibike Bikes Strategy Dashboard")

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Introduction","Weather and bike usage",
   "Popular stations",
   "Interactive map of bike trips", "Recommendations"])

########################## Import data ###########################################################################################

df = pd.read_csv('reduced_data_to_plot_7.csv', index_col=0)
top20 = pd.read_csv('top20.csv', index_col=0)

######################################### DEFINE THE PAGES #####################################################################

### Introduction
if page == "Introduction":
    st.markdown("""
    #### This dashboard serves as a data-driven exploration of New York City’s CitiBike network. 
    It brings together ridership patterns, weather relationships, and station utilization metrics
    to better understand operational dynamics and address supply-and-demand imbalances across the system.

    ### What This Analysis Explores
    This tool examines key factors shaping CitiBike performance, including:
    - Weather Influence	How do temperature and rainfall affect daily usage?
    - Station Utilization	Which stations see the highest demand? Where is capacity underused?
    - Spatial Behavior	Where are trip clusters and geographic demand hotspots?""")

    myImage = Image.open("citibike_image.webp")  # source: https://citibikenyc.com/
    st.image(myImage)

### Weather and bike usage
elif page == 'Weather and bike usage':
    ### Create the dual axis line chart page ###
    df_weather = pd.read_csv('wheather.csv', parse_dates=['date'])
    df_weather.sort_values('date', inplace=True)

    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

    fig_2.add_trace(
        go.Scatter(
            x=df_weather['date'],
            y=df_weather['trip_count'],
            name='Daily Bike Rides',
            line=dict(color='blue')
        ),
        secondary_y=False
    )

    fig_2.add_trace(
        go.Scatter(
            x=df_weather['date'],
            y=df_weather['temperature'],
            name='Avg Temperature (°C)',
            line=dict(color='red')
        ),
        secondary_y=True
    )

    fig_2.update_layout(
        title='Bike Rides and Temperature Over Time in NYC',
        xaxis_title='Date',
        yaxis_title='Trip Count',
        yaxis2_title='Avg Temperature (°C)',
        legend=dict(x=0.01, y=0.99),
        plot_bgcolor='white',
        title_x=0.5
    )

    st.plotly_chart(fig_2, use_container_width=True)
    st.markdown("Bike usage goes up when the weather is warm and drops when temperatures fall. This means the bike shortage issues mainly happen during the warmer months, especially from May to November.")

  
### Popular stations
elif page == 'Popular stations':

    fig = go.Figure(go.Bar(
    x=top20['start_station_name'],
    y=top20['value'],
    marker=dict(color=top20['value'], colorscale='Greens')
    ))

    fig.update_layout(
    title='Top most popular bike stations in NYC',
    xaxis_title='Start stations',
    yaxis_title='Sum of trips',
    width=900, height=600
    )

    st.plotly_chart(fig, use_container_width=True)

### Interactive map of bike trips
elif page == 'Interactive map of bike trips': 
    # Check for map file
    path_to_html = "Citibike_bike_trips.html"
    
    if os.path.exists(path_to_html):
        st.markdown("### Interactive visualization of NYC trip map")
        st.markdown("Interactive map showing aggregated bike trips across New York City")
        
        # Read file and display
        with open(path_to_html, 'r', encoding='utf-8') as f: 
            html_data = f.read()
        
        st.components.v1.html(html_data, height=700)
    st.markdown("In this visualization, the map highlights CitiBike trip flows.")
    st.markdown("Starting points of each journey is highlighter by brown colors and yellow for end of the journey.")
    st.markdown("some routes that are closer to each other have more trips than those that are further apart")
    st.markdown("Busiest trip flows are clearly seen with orange lines, specifically over 500 trips.")

### Recommendations
else:
    st.markdown("### Recommendations for Citibike:")
    st.markdown("- Increase dock capacity in Midtown, Financial District routes and school areas for students.")
    st.markdown("- Expand e-bike availability during summer and reduce idle equipment in winter.")
    st.markdown("- Place micro stations along common trip paths to shorten walk distances and support trip flow.")
    st.markdown("- Prioritize e-bike charging around bridge entrances elevatied zones.")
    st.markdown("- Partner with Mapping companies to add protected bike lanes along top routes.")
  
