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
    st.markdown("There is an obvious correlation between the rise and drop of temperatures and their relationship with the frequency of bike trips taken daily. As temperatures plunge, so does bike usage. This insight indicates that the shortage problem may be prevalent merely in the warmer months, approximately from May to October.")

  
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
        ### Add the map ###
    st.write("Interactive map showing aggregated bike trips over New York")

    path_to_html = "Citibike_bike_trips.html" 

    # Read file and keep in variable
    with open(path_to_html,'r') as f: 
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
