# %%
## Libraries
import numpy as np
import pandas as pd


# %%
## Data Import
divvy_202201 = pd.read_csv("divvy_tripdata_202201.csv")
divvy_202202 = pd.read_csv("divvy_tripdata_202202.csv")
divvy_202203 = pd.read_csv("divvy_tripdata_202203.csv")
divvy_202204 = pd.read_csv("divvy_tripdata_202204.csv")
divvy_202205 = pd.read_csv("divvy_tripdata_202205.csv")
divvy_202206 = pd.read_csv("divvy_tripdata_202206.csv")
divvy_202207 = pd.read_csv("divvy_tripdata_202207.csv")
divvy_202208 = pd.read_csv("divvy_tripdata_202208.csv")
divvy_202209 = pd.read_csv("divvy_tripdata_202209.csv")
divvy_202210 = pd.read_csv("divvy_tripdata_202210.csv")
divvy_202211 = pd.read_csv("divvy_tripdata_202211.csv")
divvy_202212 = pd.read_csv("divvy_tripdata_202212.csv")


## Combine the Dataframes
divvy_2022_original = pd.concat([divvy_202201, divvy_202202, divvy_202203, divvy_202204, divvy_202205, 
                        divvy_202206, divvy_202207, divvy_202208, divvy_202209, divvy_202210, 
                        divvy_202211, divvy_202212], axis=0)

# Reset the row indices
divvy_2022_original = divvy_2022_original.reset_index(drop=True)


# %%
## Change the Dtype for started_at and ended_at since they are originally "object"
divvy_2022_original['started_at'] = pd.to_datetime(divvy_2022_original['started_at'], format='%Y-%m-%d %H:%M:%S')
divvy_2022_original['ended_at'] = pd.to_datetime(divvy_2022_original['ended_at'], format='%Y-%m-%d %H:%M:%S')

# divvy_2022_original.info()


# %%
# Just in case, let's convert all "NULL" or "NA" or "NaN" or "N/A" string values to actually empty values. 
# I don't think they have these string values, but again, just in case.
divvy_2022_original.replace({
    '(?i)^NULL$': np.nan, 
    '(?i)^N/A$': np.nan, 
    '(?i)^NAN$': np.nan,
    '(?i)^NA$': np.nan,
}, regex=True, inplace=True)


# %%
## Sort the dataframe based on "started_at" column ascendingly.
divvy_2022_sorted = divvy_2022_original.sort_values(by='started_at', ascending=True).copy()


# %%
## Create ride_length, which is the difference between ended_at and started_at in seconds
divvy_2022_sorted['ride_length'] = (divvy_2022_sorted['ended_at'] - divvy_2022_sorted['started_at']) \
                                    .dt.total_seconds()

## create day_of_week where Monday is 0 and Sunday is 6
divvy_2022_sorted['day_of_week'] = divvy_2022_sorted['started_at'].dt.weekday


# %%
## Data Cleaning Part 1 - ride_length. Divvy Data shows any trips that were below 60 seconds in length should be removed
divvy_2022_cleaned_1 = divvy_2022_sorted.query('ride_length >= 60')

# %%
## Data Cleaning Part 2 - drop rows if we find empty values by using dropna()
divvy_2022_cleaned_2 = divvy_2022_cleaned_1.dropna()

# %%
## Data Cleaning Part 3 - Before we continue, let's check and investigate potential problems

# Let's start by checking uppercase or lowercase values from the station names to find naming inconsistencies.

# First, let's just select the column names that we want to check exclusively
test_df = divvy_2022_cleaned_2[['ride_id', 'start_station_name', 'end_station_name', \
                                  'start_station_id', 'end_station_id']]

# Next, let's check the uppercase values from start_station_name 
check_df = test_df[test_df['start_station_name']. \
                                  str.upper() == test_df['start_station_name']]
# I found something interest. check_df shows rows where start_station_name has the value "WEST CHI-WATSON", 
# and these same rows show start_station_id as "DIVVY 001 - Warehouse test station".

# let's check further if all start_station_id with "DIVVY" are test stations or not
check_df_2 = test_df.query('start_station_id.str.contains("DIVVY") == True')
# One row has the value "DIVVY 001" while the other rows have the value "DIVVY 001 - Warehouse test station".
# While it's likely "DIVVY 001" is also a test station, let's bypass it for now. Later, let's just clean up the
# rows where the start_station_id has the word "test" , not "DIVVY"

# Now, let's check the uppercase values from end_station_name
check_df_3 = test_df[test_df['end_station_name']. \
                                  str.upper() == test_df['end_station_name']]
# There are several rows with value "DIVVY CASSETTE REPAIR MOBILE STATION", which means this is just 
# used for maintenance, not for actual trips. This needs to be filtered as well later.

# Just like check_df2, let's check any end_station_id that contains the word "DIVVY"
check_df_4 = test_df.query('end_station_id.str.contains("DIVVY") == True')
# Nothing special here, let's move on

# Now, let's check the lowercase values from both start_station_name and _end_station_name
check_df_5 = test_df[test_df['start_station_name']. \
                                  str.lower() == test_df['start_station_name']]

check_df_6 = test_df[test_df['end_station_name']. \
                                  str.lower() == test_df['end_station_name']]
# No results for both check_df_5 and check_df_6    

# Now that we know that some rows have the word "test" in start_station_id (check check_df), we should check
# all the station columns for the word "test". Let's check regardless of its case
check_df_7 = test_df.query('start_station_name.str.lower().str.contains("test") | \
                            end_station_name.str.lower().str.contains("test") | \
                            start_station_id.str.lower().str.contains("test") | \
                            end_station_id.str.lower().str.contains("test")')
# there seems to be a lot of test stations here, let's filter them out later

# After checking check_df_7, I also found out that certain station names ended up with "*", "(Temp)", and "- Charging". 
# To avoid unwated analysis during the analysis stage later on, these findings should be cleaned as well with str.replace()


# %%
## Data Cleaning Part 4 - data cleaning steps that include the findings from Data Cleaning part 3 above
# Findings that need filtering (query) operation include: check_df, check_df_3, and check_df_7    
divvy_2022_cleaned_4 = divvy_2022_cleaned_2.query('start_station_name.str.upper() != start_station_name') \
                                          .query('end_station_name.str.upper() != end_station_name') \
                                          .query('~(start_station_name.str.lower().str.contains("test") | \
                                                   end_station_name.str.lower().str.contains("test") | \
                                                   start_station_id.str.lower().str.contains("test") | \
                                                   end_station_id.str.lower().str.contains("test"))').copy()
                                              
# Next, let's delete the unwanted characters and words per our finding, "*", "(Temp)", and "- Charging"
divvy_2022_cleaned_4['start_station_name'] = divvy_2022_cleaned_4['start_station_name'] \
                                                .str.replace('\\*', '', regex=True) \
                                                .str.replace('\\(Temp\\)', '', regex=True) \
                                                .str.replace('\\ - Charging', '', regex=True)
                                              
                                                
divvy_2022_cleaned_4['end_station_name'] = divvy_2022_cleaned_4['end_station_name'] \
                                                .str.replace('\\*', '', regex=True) \
                                                .str.replace('\\(Temp\\)', '', regex=True) \
                                                .str.replace('\\ - Charging', '', regex=True)


# Let's remove duplicate ride_id as well
divvy_2022_cleaned_4 = divvy_2022_cleaned_4.drop_duplicates(subset='ride_id')
#Apparently, there are exact same number of rows as before. All good! I keep this last code line above, just in case


# %%
## Data Cleaning Part 5 - let's eliminate unnecessary white spaces in all columns

divvy_2022_cleaned_5 = divvy_2022_cleaned_4.copy()

divvy_2022_cleaned_5 = divvy_2022_cleaned_5.applymap(lambda x: x.strip() \
                                                     if isinstance(x, str) else x)


# %%
## Data Analysis Part 1 - New Dataframe for Analysis, New Column(s), and Boolean Masking

# First of all, let's create a new dataframe, so later we can modify it whenever needed for analysis purposes
divvy_2022_analysis_1 = divvy_2022_cleaned_5.copy()

# Let's create the month column for later analysis
divvy_2022_analysis_1['month'] = pd.to_datetime(divvy_2022_analysis_1['started_at']).dt.month

# Boolean Masking for Separating Members and Casuals
mask_1 = divvy_2022_analysis_1['member_casual'] == 'member'
mask_2 = divvy_2022_analysis_1['member_casual'] == 'casual'

only_members = divvy_2022_analysis_1[mask_1]
only_casuals = divvy_2022_analysis_1[mask_2]


# %%

## Data Analysis Part 2 - Most Popular Station Names for Members

# Count start_station_name total counts
start_station_name_count_member = only_members.groupby('start_station_name') \
                                              .size() \
                                              .reset_index(name='count') \
                                              .sort_values(by='count', ascending=False)

# Count end_station_name total counts
end_station_name_count_member = only_members.groupby('end_station_name') \
                                              .size() \
                                              .reset_index(name='count') \
                                              .sort_values(by='count', ascending=False)

# Merge the two DataFrames on the start_station_name and end_station_name columns
station_name_count_member = pd.merge(start_station_name_count_member, end_station_name_count_member, \
                                     how='outer', left_on='start_station_name', \
                                     right_on='end_station_name')

# Combine the total counts from count_x and count_y
station_name_count_member['count_total'] = np.where(~np.isnan(station_name_count_member['count_x']) & \
                                                    ~np.isnan(station_name_count_member['count_y']), \
                                                        station_name_count_member['count_x'] + \
                                                            station_name_count_member['count_y'], \
                                                            np.where(np.isnan(station_name_count_member\
                                                            ['count_y']), station_name_count_member\
                                                            ['count_x'], station_name_count_member['count_y']))

# Let's reorganize it, rename the station name, and delete unnecessary columns
station_name_count_member = station_name_count_member.rename(columns={'start_station_name': 'station_name'}) \
                                                   .drop(columns=['count_x', 'count_y', 'end_station_name'])
                                                   
                                                   
# %%
## Data Analysis Part 3 - Most Popular Station Names for Casuals

# Count start_station_name total counts
start_station_name_count_casual = only_casuals.groupby('start_station_name') \
                                              .size() \
                                              .reset_index(name='count') \
                                              .sort_values(by='count', ascending=False)

# Count end_station_name total counts
end_station_name_count_casual = only_casuals.groupby('end_station_name') \
                                            .size() \
                                            .reset_index(name='count') \
                                            .sort_values(by='count', ascending=False)

# Merge the two DataFrames on the start_station_name and end_station_name columns
station_name_count_casual = pd.merge(start_station_name_count_casual, end_station_name_count_casual, \
                                     how='outer', left_on='start_station_name', \
                                     right_on='end_station_name')

# Combine the total counts from count_x and count_y
station_name_count_casual['count_total'] = np.where(~np.isnan(station_name_count_casual['count_x']) & \
                                                     ~np.isnan(station_name_count_casual['count_y']), \
                                                         station_name_count_casual['count_x'] + \
                                                             station_name_count_casual['count_y'], \
                                                             np.where(np.isnan(station_name_count_casual\
                                                             ['count_y']), station_name_count_casual\
                                                             ['count_x'], station_name_count_casual['count_y']))

# Let's reorganize it, rename the station name, and delete unnecessary columns
station_name_count_casual = station_name_count_casual.rename(columns={'start_station_name': 'station_name'}) \
                                                     .drop(columns=['count_x', 'count_y', 'end_station_name'])


# %%
## Data Analysis Part 4 - Most Popular Days and Months

# Let's check the most popular days for both members and casuals
day_of_week_count = divvy_2022_analysis_1.groupby(['day_of_week', 'member_casual']) \
                                            .size() \
                                            .reset_index(name='count') \
                                            .sort_values(by='count', ascending=False)

# Refactor the day_of_week column to show the actual day name using map()
#This is not really needed, I do this just to make it easier to check the day names at a quick glance
day_of_week_count['day_name'] = day_of_week_count['day_of_week'].map({
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
})

# Let’s analyze the most popular months and the most popular days for each month (members only)
popular_month_count_member = only_members.groupby(['month', 'day_of_week']) \
                                              .size() \
                                              .reset_index(name='count') \
                                              .sort_values(by='count', ascending=False)

# Let’s analyze the most popular months and the most popular days for each month (casuals only)
popular_month_count_casual = only_casuals.groupby(['month', 'day_of_week']) \
                                              .size() \
                                              .reset_index(name='count') \
                                              .sort_values(by='count', ascending=False)
                                              
                                              
#### SAMPE SINI, Analyze Most Popular Hours of the Day BELUM