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

########################### Initial settings for the dashboard ####################################################

st.set_page_config(page_title='Divvy Bikes Strategy Dashboard', layout='wide')
st.title("Divvy Bikes Strategy Dashboard")

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page","Weather component and bike usage",
   "Most popular stations",
   "Interactive map with aggregated bike trips", "Recommendations"])

########################## Import data ###########################################################################################

df = pd.read_csv('reduced_data_to_plot_7.csv', index_col=0)
top20 = pd.read_csv('top20.csv', index_col=0)

######################################### DEFINE THE PAGES #####################################################################

### Intro page
if page == "Intro page":
    st.markdown("#### This dashboard aims at providing helpful insights on the expansion problems Divvy Bikes currently faces.")
    st.markdown("Right now, Divvy bikes runs into a situation where customers complain about bikes not being available at certain times. The analysis is separated into 4 sections:")
    st.markdown("- Most popular stations")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("Use the dropdown menu on the left 'Aspect Selector' to navigate through the different sections.")

    myImage = Image.open("citibike_image.webp")  # source: https://citibikenyc.com/
    st.image(myImage)

### Weather component and bike usage
elif page == 'Weather component and bike usage':
    fig_line = go.Figure()

    # Aggregating daily data
    daily_trips = df.groupby("date")["bike_id"].count().reset_index(name="trip_count")
    daily_temp = df.groupby("date")["avgTemp"].mean().reset_index(name="avgTemp")
    daily = pd.merge(daily_trips, daily_temp, on="date")

    # Trip counts
    fig_line.add_trace(go.Scatter(
        x=daily["date"], y=daily["trip_count"],
        name="Trip Count", yaxis="y1"
    ))

    # Temperature
    fig_line.add_trace(go.Scatter(
        x=daily["date"], y=daily["avgTemp"],
        name="Temperature (°C)", yaxis="y2"
    ))

    # Dual axis
    fig_line.update_layout(
        title="Daily CitiBike Trips vs. Temperature (2022)",
        xaxis=dict(title="Date"),
        yaxis=dict(title="Trip Count"),
        yaxis2=dict(title="Temperature (°C)", overlaying="y", side="right"),
        legend=dict(x=0.1, y=0.9)
    )

    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown("There is an obvious correlation between temperature changes and daily bike trips. Bike usage is higher in warmer months, approximately May to October.")

### Most popular stations
elif page == 'Most popular stations':

    fig = go.Figure(go.Bar(
    x=top20['start_station_name'],
    y=top20['value'],
    marker=dict(color=top20['value'], colorscale='Greens')
    ))

    fig.update_layout(
    title='Top 20 most popular bike stations in Chicago',
    xaxis_title='Start stations',
    yaxis_title='Sum of trips',
    width=900, height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("Top stations: Streeter Drive/Grand Avenue, Canal Street/Adams Street, Clinton Street/Madison Street. The bar chart shows clear preferences for leading stations.")

### Interactive map with aggregated bike trips
elif page == 'Interactive map with aggregated bike trips': 
    st.write("Interactive map showing aggregated bike trips over Chicago")

    path_to_html = "Divvy Bike Trips Aggregated.html" 
    with open(path_to_html, 'r') as f: 
        html_data = f.read()

    st.header("Aggregated Bike Trips in Chicago")
    components.html(html_data, height=1000)
    st.markdown("#### Using the filter on the left-hand side of the map we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown("The most popular start stations are Streeter Drive/Grand Avenue, Canal Street/Adams Street, Clinton Street/Madison Street.")

### Recommendations page
else:
    st.header("Conclusions and recommendations")
    bikes = Image.open("recs_page.png")  # source: Midjourney
    st.image(bikes)
    st.markdown("### Recommendations for Divvy Bikes:")
    st.markdown("- Add more stations along the water line, such as Streeter Dr/Grand Avenue, Millenium Park, Columbus Dr/Randolph Street, Shedd Aquarium, Michigan Avenue/Oak Street, Canal Street/Adams Street")
    st.markdown("- Fully stock bikes in these stations during warmer months to meet higher demand; reduce supply in winter to lower logistics costs")
