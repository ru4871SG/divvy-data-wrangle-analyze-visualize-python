# import numpy as np
import pandas as pd

import streamlit as st

from math import pi
from bokeh.plotting import figure
from bokeh.models import FactorRange, ColumnDataSource, HoverTool, NumeralTickFormatter, ColorBar,\
                    LinearColorMapper, Range1d, FixedTicker
from bokeh.transform import transform, cumsum
from bokeh.palettes import viridis

import pydeck as pdk

### Import Data
station_name_count_member_w_location = pd.read_pickle('station_name_count_member_w_location.pkl')
station_name_count_casual_w_location = pd.read_pickle('station_name_count_casual_w_location.pkl')
popular_month_count_member = pd.read_pickle('popular_month_count_member.pkl')
popular_month_count_casual = pd.read_pickle('popular_month_count_casual.pkl')
day_of_week_count = pd.read_pickle('day_of_week_count.pkl')
ride_length_avg = pd.read_pickle('ride_length_avg.pkl')
popular_hours_count = pd.read_pickle('popular_hours_count.pkl')
rideable_type_count_member = pd.read_pickle('rideable_type_count_member.pkl')
rideable_type_count_casual = pd.read_pickle('rideable_type_count_casual.pkl')


### Define Plots
def viz_popular_month_count_member(sizing_mode="fixed"):
    
    days_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    popular_month_count_member_copy = popular_month_count_member.copy()

    months_int = sorted(popular_month_count_member_copy['month'].unique(), key=int)
    months_str = [str(month) for month in months_int]

    month_to_index = {month: index for index, month in enumerate(months_int)}
    
    popular_month_count_member_copy['original_month'] = popular_month_count_member_copy['month']
    popular_month_count_member_copy['month'] = popular_month_count_member_copy['month'].astype(int).map(month_to_index)
    
    #set the theme color
    colors = viridis(256)
    
    mapper = LinearColorMapper(palette=colors, low=popular_month_count_member_copy['count'].min(), high=popular_month_count_member_copy['count'].max())

    p = figure(title="Popular Month Count by Day of Week Heatmap - Member",
               x_range=Range1d(-0.5, len(months_str)-0.5), y_range=days_labels,
               width=900, height=400,
               tools="hover,save,pan,box_zoom,reset,wheel_zoom",
               sizing_mode=sizing_mode, #for mobile responsiveness
               tooltips=[('Month', '@original_month'), ('Day of Week', '@day_of_week'), ('Count', '@count')])

    p.xaxis.ticker = FixedTicker(ticks=list(range(len(months_int))))
    p.xaxis.major_label_overrides = {i: str(month) for i, month in enumerate(months_int)}

    popular_month_count_member_copy['day_of_week'] = popular_month_count_member_copy['day_of_week'].map(lambda x: days_labels[x])

    p.rect(x='month', y='day_of_week', width=1, height=1, source=popular_month_count_member_copy,
           fill_color=transform('count', mapper),
           line_color=None)

    color_bar = ColorBar(color_mapper=mapper, location=(0, 0))
    p.add_layout(color_bar, 'right')

    return p


def viz_popular_month_count_casual(sizing_mode="fixed"):
    
    days_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    popular_month_count_casual_copy = popular_month_count_casual.copy()

    months_int = sorted(popular_month_count_casual_copy['month'].unique(), key=int)
    months_str = [str(month) for month in months_int]

    month_to_index = {month: index for index, month in enumerate(months_int)}
    
    popular_month_count_casual_copy['original_month'] = popular_month_count_casual_copy['month']
    popular_month_count_casual_copy['month'] = popular_month_count_casual_copy['month'].astype(int).map(month_to_index)
    
    #set the theme color
    colors = viridis(256)
    mapper = LinearColorMapper(palette=colors, low=popular_month_count_casual_copy['count'].min(), high=popular_month_count_casual_copy['count'].max())

    p = figure(title="Popular Month Count by Day of Week Heatmap - Casual",
               x_range=Range1d(-0.5, len(months_str)-0.5), y_range=days_labels,
               width=900, height=400,
               tools="hover,save,pan,box_zoom,reset,wheel_zoom",
               sizing_mode=sizing_mode, #for mobile responsiveness
               tooltips=[('Month', '@original_month'), ('Day of Week', '@day_of_week'), ('Count', '@count')])

    p.xaxis.ticker = FixedTicker(ticks=list(range(len(months_int))))
    p.xaxis.major_label_overrides = {i: str(month) for i, month in enumerate(months_int)}

    popular_month_count_casual_copy['day_of_week'] = popular_month_count_casual_copy['day_of_week'].map(lambda x: days_labels[x])

    p.rect(x='month', y='day_of_week', width=1, height=1, source=popular_month_count_casual_copy,
           fill_color=transform('count', mapper),
           line_color=None)

    color_bar = ColorBar(color_mapper=mapper, location=(0, 0))
    p.add_layout(color_bar, 'right')

    return p



def viz_day_of_week_count(sizing_mode="fixed"):
    ## map day_of_week where Monday is 0 and Sunday is 6
    day_mapping = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    
    sorted_data = day_of_week_count.sort_values(by=['day_of_week', 'member_casual'])
    
    x = [(day_mapping[row['day_of_week']], row['member_casual']) for _, row in sorted_data.iterrows()]
    counts = list(sorted_data['count'])
    
    colors = viridis(len(sorted_data['member_casual'].unique()))
    color_map = {category: color for category, color in zip(sorted_data['member_casual'].unique(), colors)}
    colors = [color_map[category] for category in sorted_data['member_casual']]
    
    p = figure(x_range=FactorRange(*x), height=350, title="Day of Week Count",
               sizing_mode=sizing_mode,
               toolbar_location=None, tools="", x_axis_label="Day of Week", y_axis_label="Count")
    
    p.vbar(x=x, top=counts, width=0.9, color=colors)
    
    hover = HoverTool()
    hover.tooltips = [
        ("Day of Week, Type", "@x"),
        ("Count", "@top")
    ]
    p.add_tools(hover)
    
    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.xaxis.major_label_orientation = 1
    p.yaxis.formatter = NumeralTickFormatter(format="0,0")
    
    return p


def viz_ride_length_avg(sizing_mode="fixed"):
    colors = viridis(2)
    color_map = {category: color for category, color in zip(ride_length_avg['member_casual'].unique(), colors)}
    ride_length_avg['color'] = ride_length_avg['member_casual'].map(color_map)

    p = figure(y_range=FactorRange(*ride_length_avg['member_casual'].unique()), \
               width=400, height=200, sizing_mode=sizing_mode,
                   title="Ride Length Average")

    p.hbar(y='member_casual', right='avg_ride_length_in_minutes', source=ride_length_avg, height=0.4, color='color')
    
    hover = HoverTool()
    hover.tooltips = [
        ("Type", "@member_casual"),
        ("Average Ride Length", "@avg_ride_length_in_minutes")
    ]
    p.add_tools(hover)

    p.xaxis.formatter = NumeralTickFormatter(format="0,0")
    
    return p


def viz_popular_hours_count(sizing_mode="fixed"):
    # Filtering data for 'member' and 'casual' values
    member_data = popular_hours_count[popular_hours_count['member_casual'] == 'member'].sort_values(by='hour')
    casual_data = popular_hours_count[popular_hours_count['member_casual'] == 'casual'].sort_values(by='hour')
    member_source = ColumnDataSource(member_data)
    casual_source = ColumnDataSource(casual_data)
    
    p = figure(width=600, height=400, title="Popular Hours Count", \
               sizing_mode=sizing_mode, #for mobile responsiveness\
                   x_axis_label="Hour", y_axis_label="Count")

    # Using member_source for 'member' data
    p.line('hour', 'count', source=member_source, line_width=2, color='#fde724', legend_label='Member', name="Member")
    p.circle('hour', 'count', source=member_source, fill_color="#fde724", size=8, color='#fde724')

    # Using casual_source for 'casual' data
    p.line('hour', 'count', source=casual_source, line_width=2, color='#440154', legend_label='Casual', name="Casual")
    p.circle('hour', 'count', source=casual_source, fill_color="#440154", size=8, color='#440154')
    
    hover = HoverTool()
    hover.tooltips = [
        ("Hour", "@hour"),
        ("Count", "@count")
    ]
    p.add_tools(hover)

    p.legend.location = "top_left"
    
    p.yaxis.formatter = NumeralTickFormatter(format="0,0")

    return p


def viz_rideable_type_count_member(sizing_mode="fixed"):
    
    rideable_type_count_member_copy = rideable_type_count_member.copy()
    rideable_type_count_member_copy['angle'] = rideable_type_count_member_copy['count'] / rideable_type_count_member_copy['count'].sum() * 2 * pi
    rideable_type_count_member_copy['color'] = viridis(len(rideable_type_count_member_copy))
    
    #Calculate the percentages
    rideable_type_count_member_copy['percentage'] = rideable_type_count_member_copy['count'] / rideable_type_count_member_copy['count'].sum() * 100
    
    source = ColumnDataSource(rideable_type_count_member_copy)

    p = figure(plot_height=255, title="Rideable Type Count (Members)", toolbar_location=None,
               x_range=(-0.5, 1.0), sizing_mode=sizing_mode)

    p.wedge(x=0, y=1, radius=0.25,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", line_width=2, fill_color='color', legend_field='rideable_type', source=source)

    hover = HoverTool()
    hover.tooltips = [("Type", "@rideable_type"), ("Count", "@count"), ("Percentage", "@percentage{0.2f}%")]
    p.add_tools(hover)

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    return p

def viz_rideable_type_count_casual(sizing_mode="fixed"):
    
    rideable_type_count_casual_copy = rideable_type_count_casual.copy()
    rideable_type_count_casual_copy['angle'] = rideable_type_count_casual_copy['count'] / rideable_type_count_casual_copy['count'].sum() * 2 * pi
    rideable_type_count_casual_copy['color'] = viridis(len(rideable_type_count_casual_copy))
    
    #Calculate the percentages
    rideable_type_count_casual_copy['percentage'] = rideable_type_count_casual_copy['count'] / rideable_type_count_casual_copy['count'].sum() * 100
    
    source = ColumnDataSource(rideable_type_count_casual_copy)

    p = figure(plot_height=255, title="Rideable Type Count (Casuals)", toolbar_location=None,
               x_range=(-0.5, 1.0), sizing_mode=sizing_mode)

    p.wedge(x=0, y=1, radius=0.25,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", line_width=2, fill_color='color', legend_field='rideable_type', source=source)

    hover = HoverTool()
    hover.tooltips = [("Type", "@rideable_type"), ("Count", "@count"), ("Percentage", "@percentage{0.2f}%")]
    p.add_tools(hover)

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    return p

#generate legends for popular stations map
def generate_color_legend(data, num_colors=10):
    min_val = data['count_total'].min()
    max_val = data['count_total'].max()
    step = (max_val - min_val) / num_colors
    values = [(min_val + i*step, min_val + (i+1)*step) for i in range(num_colors)]
    
    # Add the title for the legend
    st.write("Station Name Counts")

    for lower, upper in values:
        norm_val = (lower - min_val) / (max_val - min_val)
        color = viridis(256)[int(norm_val * 255)]
        st.write(
            f"<div style='display: inline-block; margin-right: 10px;'>"
            f"<div style='background-color: {color}; width: 40px; height: 10px; display: inline-block;'></div>"
            f"<span style='margin-left: 10px; font-size: 13px;'>{int(lower)} - {int(upper)}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

#generate map for popular stations map using pydeck
def viz_pydeck_map(data, num_colors=10):

    # Compute viridis colors, bin the data into 10 bins, and assign color for each bin
    min_val = data['count_total'].min()
    max_val = data['count_total'].max()
    step = (max_val - min_val) / num_colors
    
    bins = pd.cut(data['count_total'], bins=[min_val + i*step for i in range(num_colors+1)], labels=False, include_lowest=True)

    colors = [viridis(256)[int(i * 255 / (num_colors-1))] for i in bins]
    data['colors'] = [[int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)] for color in colors]
    
    layer = pdk.Layer(
        'ScatterplotLayer',
        data,
        get_position='[Longitude, Latitude]',
        get_radius=200,
        get_fill_color="colors",
        pickable=True,
        opacity=0.8
    )
    
    avg_latitude = data['Latitude'].mean()
    avg_longitude = data['Longitude'].mean()

    view_state = pdk.ViewState(latitude=avg_latitude, longitude=avg_longitude, zoom=10)
    
    # Return the Deck object
    return pdk.Deck(
        layers=[layer], 
        initial_view_state=view_state, 
        map_style="light",
        tooltip={"html": "<b>{station_name}</b><br>Total Count: {count_total}"}
    )


### Custom Functions for Chart Displays
def display_popular_hours():
    st.subheader("Popular Hours")
    st.bokeh_chart(viz_popular_hours_count(sizing_mode="scale_width"))
    st.markdown("From the above data visualization, you can see how both casuals and members\
            like to use Divvy bikes between 15-18 (3 PM - 6 PM).\
            However, casuals have higher trip counts later at night.\
            On the other hand, morning time is more popular for members, but not so much for casuals.")

def display_popular_days():
    st.subheader("Popular Days")
    st.bokeh_chart(viz_day_of_week_count(sizing_mode="scale_width"))
    st.markdown("Members use Divvy bikes more on weekdays, whereas casuals prefer to use them on weekends.\
                One theory about this is that casuals use Divvy bikes more for hobbies and leisure, whereas members \
                    are more likely to use the bikes more for work commutes and other weekday routines. \
                        This theory makes sense because in the previous visualization we can see that the morning time \
                            is more popular for members")
    
def display_popular_months():
    st.subheader("Popular Months")    
    tab1, tab2 = st.tabs(["Member", "Casual"])
    
    with tab1:
        st.bokeh_chart(viz_popular_month_count_member(sizing_mode="scale_width"))
            
    with tab2:
        st.bokeh_chart(viz_popular_month_count_casual(sizing_mode="scale_width"))
    
    st.caption('You can change the heatmap visualization above by using the tabs. Select the tab Casual to check\
                the heatmap for casuals, and select the tab Member to check the heatmap for members')
    
    st.markdown("""
    Both heatmaps show\
        that casuals and members like to use Divvy bikes between June and September, which are basically \
            the summer months. It is understandable, considering bike services are typically more popular \
                during summertime.
        
    However, there is a big difference between casuals and members. Casuals love to use the bikes from Friday \
        to Sunday (weekends), whereas members’ busiest days are between Tuesday and Thursday. This information \
            strengthen my narrative about how casuals may use Divvy service more for hobbies and leisure.
         
         
    You can also check between November and January, where trip counts for casuals go much lower, but trip counts \
        for members still look considerably higher. Daily routines (e.g., work commute) don't always change throughout \
            the year, but people may not really use bikes for leisure and hobbies in the winter months.
        """)
    
def display_popular_stations():
    st.subheader("Popular Stations")
    tab1, tab2 = st.tabs(["Member", "Casual"])
    
    with tab1:
        col1, col2 = st.columns([3, 1])
    
        with col1:
            st.pydeck_chart(viz_pydeck_map(station_name_count_member_w_location))
        
        with col2:
            generate_color_legend(station_name_count_member_w_location)
            
    with tab2:
        col1, col2 = st.columns([3, 1])
    
        with col1:
            st.pydeck_chart(viz_pydeck_map(station_name_count_casual_w_location))
        
        with col2:
            generate_color_legend(station_name_count_casual_w_location)
            
    st.caption('You can change the Pydeck interactive map above by using the tabs. Select the tab Casual to check\
                the interactive map for casuals, and select the tab Member to check the interactive map for members')
    
    st.markdown("""
    The interactive map for members shows popular stations for members. Here we can see that the most popular stations \
        are Kingsbury St & Kinzie St, Clark St & Elm St, and Wells St & Concord Ln. And interestingly, the station \
            counts are more spread out compared to the interactive map for members.
    
    
    Meanwhile, the interactive map for casuals shows that Streeter Dr & Grand Ave is the most popular station, \
        much more popular than every other station. Considering that Streeter Dr & Grand Ave is located right next \
            to the Navy Pier, this analysis has proven my previous point on how casuals use the bikes for hobbies and\
                leisure. The Navy Pier is a tourist attraction in Chicago.
        """)
            
def average_ride_length():
    st.subheader("Average Ride Length (Minutes)")
    st.bokeh_chart(viz_ride_length_avg(sizing_mode="scale_width"))
    
    st.markdown("""
    Average ride lengths from casuals and members differ greatly. Casuals' average ride length in minutes is \
        24.28 minutes, while members' average ride length in minutes is only 12.68 minutes.
    
    
    The fact that casuals spend more time with the bikes shows that casuals often use them to go to far locations. \
        This is understandable because leisure destinations such as Navy Pier may be a bit too far away from the \
            casual riders' starting stations.
        """)
    
def bike_types():
    st.subheader("Bike Types")
    st.bokeh_chart(viz_rideable_type_count_member(sizing_mode="scale_width"))
    st.bokeh_chart(viz_rideable_type_count_casual(sizing_mode="scale_width"))
    
    st.markdown("""
    There is a difference between casuals and members when it comes to bike types. Members like classic bikes much \
        more than electric bikes. As for casuals, they also like classic bikes more than electric ones, but the gap \
            is not as big as the member group.
    
    
    Another interesting find, it looks like all docked bikes were only reserved for casuals in 2022.
        """)


### Streamlit App Layout

## Sidebar menu
selection_menu = st.sidebar.radio(
    'Choose a Specific Report:',
    ('All', 'Popular Hours', 'Popular Days', 'Popular Months', 'Popular Stations', 'Average Ride Length', 'Bike Types')
)

## Display selected charts using the custom functions for chart displays, and put additional titles and notes
if selection_menu == 'All':
    st.title("Divvy Data Analysis Report with Interactive Visualizations")
    st.markdown("*by: Ruddy Setiadi Gunawan*")
    st.markdown("""
    I used Divvy Bikes public data (https://divvybikes.com/system-data) to create this analysis report. \
        The goal of this report is to analyze the differences between members and casual riders throughout the year of \
            2022.
    
    
    The original data has been made available under this license: https://divvybikes.com/data-license-agreement
    
    
    Divvy trip datasets from January 2022 to December 2022 were used, cleaned, transformed and analyzed using Python \
        libraries like ***numpy*** and ***pandas***. As for the data visualizations below, ***bokeh*** and ***pydeck*** \
            were used (all visualizations here are interactive). If you want to check how I cleaned and transformed the original data, you can check my github \
                repo here. I also have the Python script for the visualizations in the same github repo.
        """)

    st.header("Data Analysis Report:")
    display_popular_hours()
    display_popular_days()
    display_popular_months()
    display_popular_stations()
    average_ride_length()
    bike_types()
elif selection_menu == 'Popular Hours':
    display_popular_hours() 
elif selection_menu == 'Popular Days':
    display_popular_days()
elif selection_menu == 'Popular Months':
    display_popular_months()
elif selection_menu == 'Popular Stations':
    display_popular_stations()
elif selection_menu == 'Average Ride Length':
    average_ride_length()
elif selection_menu == 'Bike Types':
    bike_types()


if __name__ == '__main__':
    pass