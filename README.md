# Divvy Data Wrangle, Analyze, and Visualize with Python

Welcome to the GitHub repo for my Divvy Data Analysis Report. You can check the analysis report in my Streamlit web app here: [https://divvy-data-analysis-report.streamlit.app](https://divvy-data-analysis-report.streamlit.app)

I used Divvy Bikes public data [https://divvybikes.com/system-data](https://divvybikes.com/system-data) to create the analysis report. The goal is to analyze the differences between members and casual riders throughout 2022.

The original data has been made available under this license: [https://divvybikes.com/system-data](https://divvybikes.com/data-license-agreement)

Divvy trip data from January 2022 to December 2022 were cleaned, transformed, and analyzed using Python libraries like numpy and pandas. As for the data visualizations, bokeh and pydeck were used (all visualizations in the Streamlit web app are interactive). 

## Repository Contents:##
There are two Python scripts in this repo:

**divvy.py** - This script provides all the data wrangling and analysis steps, transforming raw data into analyzable data frames. The Pickle files are the result of this script's operation.

**app.py** - This script is used to create interactive data visualizations and to establish the web app.
