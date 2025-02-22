"""

    Cem_Saydam_Streamlit.py

"""


# Standard Library Imports
import os
import math
import warnings
import requests

# Third-party Imports
import numpy as np
import pandas as pd
import streamlit as st
import scipy.stats as stats
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Turn off Warnings for better visualization
warnings.filterwarnings("ignore")


# Display Author info
st.markdown(f"""
### Cem Saydam
""")

#
# # Function to web-scrab Vanderlande Logo
# def vanderlande_logo_adder():
#
#     # Try to retrieve Vanderlande Logo 3 times
#     counter = 3
#
#     # URL of the image
#     url = "https://upload.wikimedia.org/wikipedia/commons/d/da/Logo_Vanderlande.jpg"
#
#     while counter > 0:
#         # Fetch the image
#         response = requests.get(url)
#
#         # Check if the request was successful
#         if response.status_code == 200:
#             break
#         else:
#             counter -= 1
#     return st.image(response.content) if counter != 0 else st.error("Failed to load Vanderlande Logo.")
#
#
# # Function to add Vanderlande Logo from web-scrabbing
# vanderlande_logo_adder()

# Get the directory of the current script (Python file)
script_dir = os.getcwd()

# Set the path to the logo file located in the same directory as the Python file
file_path_logo = os.path.join(script_dir, 'vanderlande_logo.JPG')

# Add Vanderlande Logo from local source
st.image(file_path_logo)

# Introduction
st.markdown(f""" ### Introduction""")

# Load the data
st.markdown(f""" #### Read in the data""")


# Set the path to the CSV file located in the same directory as the Python file
file_path = os.path.join(script_dir, 'Xray_Scan_Data_Jul_2022.csv')

# Read the CSV file
data = pd.read_csv(file_path)

# Check if the DataFrame is not empty
if not data.empty:  # data.empty returns True if the DataFrame is empty
    st.markdown(f"""
    ###### - `{str('Uploaded data Successfully')}`""")
else:
    st.error("Failed to load data. DataFrame is empty.")

# Set default parameters for plots to generalise visuals
width = 800
height = 640
xtick_size = 14
ytick_size = 14
xlabel_size = 18
ylabel_size = 18


# Initial Analysis of the data
st.markdown(f""" #### Look at data
- How many rows are in the dataset?
#### `{len(data):,}`
- How many columns are in this dataset? 
#### `{len(data.columns)}`
- Is the data complete? 
""")


# Calculate the percentage of not null values
not_null_percentage = (data.notnull().sum() / len(data)) * 100
for column, percentage in not_null_percentage.items():
    st.write(f"###### Percentage of not null values in `{column}` column is: `{round(percentage, 2)}`% not null")

st.markdown(f""" ##### Look at data""")
st.dataframe(data.tail(5))

# Describe Possible Goals
st.markdown(f""" #### What are questions that can be addressed using this data?
##### 1. Throughput and Load Distribution
- How many bags are processed each day?
- What is the daily average number of bags processed?
- Which days and hours experience the highest bag processing volumes?
- How many bags are processed at specific time intervals such as hourly and 15-minute intervals?
##### 2. Peak Days of Week Analysis
- What are the busiest days of the week for bag screening?
- Can operator schedules be optimized to align with peak days to improve system performance and reliability?
##### 3. System Bottlenecks and Time-Outs
- How significant is the issue of "time-out" results across machines and clusters?
- Are certain machines more prone to time-out situations than others?
- During which days are time-outs most prevalent?
- During which times are time-outs most prevalent?
##### 4. Machine and Cluster Utilization
- Are bags distributed equitably across machines and clusters?
- Are some machines handling disproportionately higher loads?
- Do machines with higher workloads correlate with higher malfunction rates?
##### 5. Screening Escalations and Level 2 Analysis
- How many bags reach Level 2 screening, and what proportion does this represent relative to the total throughput?
- Are there trends in Level 2 escalations across time?
- Are there machines when Level 2 escalations are disproportionately higher?
##### 6. Single vs Multiple Screenings
- Are there instances of bags being re-screened unnecessarily after being cleared at Level 1 or Level 2?
- How frequently do recirculation incidents occur, and what are their potential causes?
##### 7. Decision-Making Times
- How long does it take on average for operators to examine a bag at each machine?
##### 8. Operator Interventions
- What percentage of bags require operator intervention, and what are the primary reasons for such interventions?
- Are operator interventions more frequent during specific times or at certain machines?
""")

# Initial data manipulation
# Ensure the 'bag_scan_timestamp' column is parsed as datetime
data['bag_scan_timestamp'] = pd.to_datetime(data['bag_scan_timestamp'], errors='coerce')

# Add a new column 'week_of_day' for the day of the week based on the date
data['week_of_day'] = pd.to_datetime(data['bag_scan_timestamp'].dt.date).dt.day_name()

# Convert the bag_scan_timestamp to datetime format for time-based analysis
data['bag_scan_timestamp'] = pd.to_datetime(data['bag_scan_timestamp'])

st.markdown(f"""## Chapter - 1""")
st.markdown(f"""### Throughput and Load Distribution""")
st.write(" - How many bags are processed each day?")
st.write(" - What is the daily average number of bags processed?")
st.write(" - Which days and hours experience the highest bag processing volumes?")
st.write(" - How many bags are processed at specific time intervals such as hourly and 15-minute intervals?")

# Throughput by Day Section
st.write("### Throughput by Day")

# Data Manipulation for Throughput Section
data['day'] = data['bag_scan_timestamp'].dt.date
data['hour'] = data['bag_scan_timestamp'].dt.hour
data['15_min_interval'] = data['bag_scan_timestamp'].dt.floor('15T')

# Aggregate data for visualizations
throughput_by_day = data.groupby('day').size()
throughput_by_hour = data.groupby('hour').size()
throughput_by_15_min = data.groupby('15_min_interval').size()

# Plot throughput by day
fig_throughput_day = px.bar(
    throughput_by_day,
    x=throughput_by_day.index,
    y=throughput_by_day.values,
    labels={'x': 'Day', 'y': 'Number of Bags'},
    title='Throughput by Day'
)
fig_throughput_day.update_traces(text=throughput_by_day.values,
                                 marker=dict(color="#FF0000"),  # Assign color list to bars
                                 textposition='outside')

# Adjust figure
fig_throughput_day.update_layout(
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=xtick_size),
        title=dict(text='Day', font=dict(size=xlabel_size))
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size),
        title=dict(text='Number of Bags', font=dict(size=ylabel_size))
    ),
    width=width,
    height=height
)

# Display the plot
st.plotly_chart(fig_throughput_day)

# Calculate daily throughput and average
daily_throughput = throughput_by_day.sum()
daily_average = throughput_by_day.mean()

# Show the analysis
st.markdown(f""" 
#### Throughput by Day Insights
- How many bags are processed each day?:  
  #### `{daily_throughput:,} number of bags processed.`
- What is the daily average number of bags processed?  
  #### `{daily_average:.2f} average number of bags processed daily.`
""")

# Top 6 busiest days
top_6_days = throughput_by_day.sort_values(ascending=False).head(6)

# Calculate statistics for top 6 busiest days
mean_throughput = throughput_by_day.mean()
std_throughput = throughput_by_day.std()
variance_throughput = throughput_by_day.var()

# Calculate confidence interval for the mean (95% confidence level)
n = len(throughput_by_day)  # Number of days
standard_error = std_throughput / (n ** 0.5)  # Standard error of the mean
confidence_level = 0.95  # 95% confidence interval
degrees_of_freedom = n - 1
critical_value = stats.t.ppf((1 + confidence_level) / 2, df=degrees_of_freedom)  # t-critical value

margin_of_error = critical_value * standard_error  # Margin of error
ci_lower = mean_throughput - margin_of_error  # Lower bound of the confidence interval
ci_upper = mean_throughput + margin_of_error  # Upper bound of the confidence interval

# Assign colors dynamically based on rank
red_gradient = [
    "#FF0000",  # Top 1 Red (Pure Red)
    "#CC0000",  # Top 2 Red (Dark Red)
    "#990000",  # Top 3 Red (Darker Red)
    "#CC3333",  # Top 4 Red (Strong Red)
    "#CC6666",  # Top 5 Red (Moderate Red)
    "#CC9999"  # Top 6 Red (Light Dark Red)
]

bar_colors = ["#D3D3D3"] * len(throughput_by_day)  # Default bar color (light gray)

for idx, (day, _) in enumerate(top_6_days.items()):
    day_idx = throughput_by_day.index.get_loc(day)
    bar_colors[day_idx] = red_gradient[idx]

# Create a Plotly bar chart for throughput with top 6 highlighted
st.write("### Throughput by Day with Top 6 Highlighted")
fig_top_6 = px.bar(
    throughput_by_day,
    x=throughput_by_day.index,
    y=throughput_by_day.values,
    labels={'x': 'Day', 'y': 'Number of Bags'},
    title='Throughput by Day with Top 6 Highlighted'
)

# Add lines for mean and confidence intervals
fig_top_6.add_hline(y=ci_upper, line_dash="dash", line_color="blue", annotation_text="Upper CI (95%)")
fig_top_6.add_hline(y=mean_throughput, line_dash="dash", line_color="green", annotation_text="Mean Throughput")
fig_top_6.add_hline(y=ci_lower, line_dash="dash", line_color="orange", annotation_text="Lower CI (95%)")

fig_top_6.update_traces(
    marker=dict(color=bar_colors),  # Dynamically assign bar colors
    text=throughput_by_day.values,
    textposition='outside'
)

fig_top_6.update_layout(
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=xtick_size),
        title=dict(text='Day', font=dict(size=xlabel_size))
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size),
        title=dict(text='Number of Bags', font=dict(size=ylabel_size))
    ),
    width=width,
    height=height
)

# Display the plot
st.plotly_chart(fig_top_6)

# Show the analysis
st.markdown(f""" 
##### Statistical Insights for Throughput by Day
- **Mean:** `{mean_throughput:,.2f}`
- **Standard Deviation:** `{std_throughput:,.2f}`
- **Variance:** `{variance_throughput:,.2f}`
- **95% Confidence Interval for Mean:** `({ci_lower:,.2f}, {ci_upper:,.2f})`
#### What are the peak days when the most bags are processed?
- Top 6 Days by Throughput
""")

# Create two rows of columns for metrics
col1, col2, col3 = st.columns(3)  # First row
col4, col5, col6 = st.columns(3)  # Second row


# Define custom HTML for metrics
def top_metric(label, value, delta, color, bg_color):
    return f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;
                padding: 10px; margin: 5px; border-radius: 10px; background-color: {bg_color}; width: 100%;">
        <h4 style="color: {color}; margin: 5px 0;">{label}</h4>
        <p style="font-size: 20px; font-weight: bold; margin: 0px 0;">{value}</p>
        <p style="font-size: 16px; margin: 0;">{delta}</p>
    </div>
    """


# Loop through top 6 days and assign metrics to the columns
for idx, (day, count) in enumerate(top_6_days.items()):
    day_of_week = pd.to_datetime(day).day_name()  # Get the day of the week
    metric_html = top_metric(
        label=f"Top-{idx + 1} Day:",
        value=str(day) + f"\n <br>{day_of_week}",
        delta=f"Number of Bags: {count}",
        color="white",
        bg_color=red_gradient[idx]  # Assign gradient color for the metric
    )

    if idx < 3:
        with [col1, col2, col3][idx]:  # Place in the first row
            st.markdown(metric_html, unsafe_allow_html=True)
    else:
        with [col4, col5, col6][idx - 3]:  # Place in the second row
            st.markdown(metric_html, unsafe_allow_html=True)

# Plot throughput by hour
st.write("### Throughput by Hour")

# Group by hour to find throughput
hourly_throughput = data.groupby('hour').size().reset_index(name='count')

# Throughput by Hour Plot
hourly_fig = px.bar(hourly_throughput, x='hour', y='count',
                    labels={'hour': 'Hour', 'count': 'Number of Bags'},
                    color='count', color_continuous_scale='Oranges')

hourly_fig.update_traces(text=hourly_throughput['count'], textposition='outside')

# Adjust figure
hourly_fig.update_layout(
    xaxis=dict(
        tickmode='linear',
        tickangle=0,
        tickfont=dict(size=xtick_size),  # Rotate x-tick values and set font size
        title=dict(text='Hour', font=dict(size=xlabel_size))  # Set x-axis title and size
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size),  # Set y-tick font size
        title=dict(text='Number of Bags', font=dict(size=ylabel_size))  # Set y-axis title and size
    ),
    width=width,
    height=height
)

st.plotly_chart(hourly_fig)

# Calculate daily throughput and average
hourly_throughput = throughput_by_hour.sum()
hourly_average = throughput_by_hour.mean()

# Show the analysis
st.markdown(f""" 
#### Throughput by Hour Insights
- How many bags are processed each hour?:  
  #### `{hourly_throughput:,} number of bags processed.`
- What is the hourly average number of bags processed?  
  #### `{hourly_average:.2f} average number of bags processed hourly.`
""")

# Top 6 busiest hours
top_6_hours = throughput_by_hour.sort_values(ascending=False).head(6)

# Plot throughput by hour
st.write("### Throughput by Hour with Top 6 Highlighted")

# Calculate statistics for top 6 busiest days
mean_throughput_hour = throughput_by_hour.mean()
std_throughput_hour = throughput_by_hour.std()
variance_throughput_hour = throughput_by_hour.var()

# Calculate confidence interval for the mean (95% confidence level)
n_hour = len(throughput_by_hour)  # Number of days
standard_error_hour = std_throughput_hour / (n_hour ** 0.5)  # Standard error of the mean
confidence_level_hour = 0.95  # 95% confidence interval
degrees_of_freedom_hour = n_hour - 1
critical_value_hour = stats.t.ppf((1 + confidence_level_hour) / 2, df=degrees_of_freedom_hour)  # t-critical value

margin_of_error_hour = critical_value_hour * standard_error_hour  # Margin of error
ci_lower_hour = mean_throughput_hour - margin_of_error_hour  # Lower bound of the confidence interval
ci_upper_hour = mean_throughput_hour + margin_of_error_hour  # Upper bound of the confidence interval

# Assign a color gradient for the top 6 busiest hours
orange_gradient = [
    "#FF4500",  # Top 1 Orange (Orange Red)
    "#FF6347",  # Top 2 Orange (Tomato)
    "#FF8C00",  # Top 3 Orange (Dark Orange)
    "#FFA500",  # Top 4 Orange (Orange)
    "#FFB733",  # Top 5 Orange (Medium Orange)
    "#FFCC66"  # Top 6 Orange (Soft Dark Orange)
]

# Set default color for all bars (light gray)
colors = ["#518ff5"] * len(throughput_by_hour)

# Assign colors based on rank
for idx, (hour, _) in enumerate(top_6_hours.items()):
    colors[hour] = orange_gradient[idx]

# Plot for Throughput by Hour
fig_throughput_hour = px.bar(
    throughput_by_hour,
    x=throughput_by_hour.index,
    y=throughput_by_hour.values,
    labels={'x': 'Hour', 'y': 'Number of Bags'},
    title='Throughput by Hour with Top 6 Highlighted'
)

# Apply colors to bars
fig_throughput_hour.update_traces(
    marker=dict(color=colors),  # Assign color list to bars
    text=throughput_by_hour.values,  # Show values as text on bars
    textposition='outside'
)

# Add lines for mean and confidence intervals
fig_throughput_hour.add_hline(y=ci_upper_hour, line_dash="dash", line_color="red", annotation_text="Upper CI (95%)")
fig_throughput_hour.add_hline(y=mean_throughput_hour, line_dash="dash", line_color="green",
                              annotation_text="Mean Throughput")
fig_throughput_hour.add_hline(y=ci_lower_hour, line_dash="dash", line_color="purple", annotation_text="Lower CI (95%)")

# Adjust the layout
fig_throughput_hour.update_layout(
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=xtick_size),
        title=dict(text='Hour', font=dict(size=xlabel_size))
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size),
        title=dict(text='Number of Bags', font=dict(size=ylabel_size))
    ),
    width=width,
    height=height
)

# Display the plot
st.plotly_chart(fig_throughput_hour)

# Show the analysis
st.markdown(f""" 
##### Statistical Insights for Throughput by Hour
- **Mean:** `{mean_throughput_hour:,.1f}`
- **Standard Deviation:** `{std_throughput_hour:,.1f}`
- **Variance:** `{variance_throughput_hour:,.1f}`
- **95% Confidence Interval for Mean:** `({ci_lower_hour:,.1f}, {ci_upper_hour:,.1f})`
#### What are the peak hours when the most bags are processed?
- Top 6 Hours by Throughput
""")

# Create two rows of columns for hours
col1, col2, col3 = st.columns(3)  # First row
col4, col5, col6 = st.columns(3)  # Second row

# Loop through top 6 hours and assign metrics to the columns
for idx, (hour, count) in enumerate(top_6_hours.items()):
    metric_html = top_metric(
        label=f"Top-{idx + 1} Hour:",
        value=f"{hour}:00",
        delta=f"Number of Bags: {count}",
        color="white",
        bg_color=orange_gradient[idx]
    )

    if idx < 3:
        with [col1, col2, col3][idx]:  # Place in the first row
            st.markdown(metric_html, unsafe_allow_html=True)
    else:
        with [col4, col5, col6][idx - 3]:  # Place in the second row
            st.markdown(metric_html, unsafe_allow_html=True)

st.markdown(f"""
#### Statistical Insights for Throughput by Hour

- **Mean Throughput**: The average number of bags processed per hour is `{mean_throughput_hour:,.1f}`, indicating that
 on average, `{mean_throughput_hour:,.1f}` bags are handled during each hour of operation. This gives us a general 
 sense of throughput during a typical hour. \n

- **Standard Deviation**: The standard deviation is `{std_throughput_hour:,.1f}`, reflecting the extent to which the
 throughput varies across different hours. A higher standard deviation suggests that the throughput can fluctuate
  significantly depending on the time of day. \n

- **Variance**: The variance of `{variance_throughput_hour:,.1f}` further highlights the spread of throughput data.
 A higher variance indicates that the number of bags processed can vary widely, especially during peak hours. \n

- **95% Confidence Interval for the Mean**: The 95% confidence interval for the mean throughput is between 
`{ci_lower_hour:,.1f}` and `{ci_upper_hour:,.1f}`. This means that we are 95% confident that the actual mean 
throughput for each hour lies within this range.

##### Peak Hours for Throughput

When examining the busiest hours for bag processing, we observe the following key peak times:

- **Top 1 Hour:**
  - **Time**: `{top_6_hours.index[0]}` o'clock
  - **Number of Bags**: `{top_6_hours.iloc[0]:,.0f}`
  - This hour sees the highest throughput, with `{top_6_hours.iloc[0]:,.0f}` bags processed, likely corresponding 
  to the morning rush as passengers prepare for early flights. \n

- **Top 2 Hour:**
  - **Time**: `{top_6_hours.index[1]}` o'clock
  - **Number of Bags**:  `{top_6_hours.iloc[1]:,.0f}`
  - At `{top_6_hours.index[1]}` o'clock, `{top_6_hours.iloc[1]:,.0f}` bags are processed, still a high volume, likely due to continued morning
   departures and additional international or domestic flights. \n

- **Top 3 Hour:**
  - **Time**: `{top_6_hours.index[2]}` o'clock
  - **Number of Bags**: `{top_6_hours.iloc[2]:,.0f}`
  - The throughput reaches `{top_6_hours.iloc[2]:,.0f}` at `{top_6_hours.index[2]}` o'clock, continuing the morning rush. 
  This time often sees high-volume flights from major international airports.

- **Top 4 Hour:**
  - **Time**: `{top_6_hours.index[3]}` o'clock
  - **Number of Bags**: `{top_6_hours.iloc[3]:,.0f}`
  - The throughput at `{top_6_hours.index[3]}` o'clock is `{top_6_hours.iloc[3]:,.0f}` bags, showing an early morning peak 
  as passengers start their travel day.

- **Top 5 Hour:**
  - **Time**: `{top_6_hours.index[4]}` o'clock
  - **Number of Bags**: `{top_6_hours.iloc[4]:,.0f}`
  - At `{top_6_hours.index[4]}` o'clock, `{top_6_hours.iloc[4]:,.0f}` bags are processed, indicating a steady stream of 
  passengers with some fluctuations as the late morning progresses.

- **Top 6 Hour:**
  - **Time**: `{top_6_hours.index[5]}` o'clock
  - **Number of Bags**: `{top_6_hours.iloc[5]:,.0f}`
  - The`{top_6_hours.index[5]}` o'clock hour sees `{top_6_hours.iloc[5]:,.0f}` bags processed, suggesting a second peak
   in the afternoon as travelers prepare for evening flights.

#### Observations and Implications:

- **Morning Surge**: The highest throughput occurs during the early morning hours
 (`{top_6_hours.index[0]}` o'clock and `{top_6_hours.index[1]}` o'clock), 
with the throughput reaching `{top_6_hours.iloc[0]:,.0f}` and `{top_6_hours.iloc[1]:,.0f}`, respectively.
 This indicates that the early morning period sees the busiest travel activity, likely driven by a combination of 
 departing flights and early morning connections. \n

- **Mid-Morning Continuity**: The `{top_6_hours.index[2]}` o'clock and `{top_6_hours.index[4]}` o'clock hours also experience high 
throughput, suggesting that the busy period continues through the late morning.
 These hours see `{top_6_hours.iloc[2]:,.0f}` 
 and `{top_6_hours.iloc[4]:,.0f}` bags processed, signaling sustained demand as passengers board flights 
 or connect to international departures.

- **Afternoon Peak**: The `{top_6_hours.index[5]}` o'clock surge, with `{top_6_hours.iloc[5]:,.0f}` bags processed,
 marks the beginning of the afternoon rush. This spike could be attributed to travelers making their 
 way to evening departures or returning from day trips.

#### Recommendations for Operational Adjustments:

- **Optimize Staffing for Peak Hours**: Given the high throughput in the morning (`{top_6_hours.index[0]}` o'clock and 
`{top_6_hours.index[1]}` o'clock) and 
the afternoon `{top_6_hours.index[5]}` o'clock, it's crucial to increase staffing during these times to ensure smooth 
screening operations and avoid delays.

- **Resource Allocation**: Ensure that the necessary screening equipment, such as automated systems, are optimized 
for these peak hours, particularly during the `{top_6_hours.index[0]}` o'clock and 
`{top_6_hours.index[1]}` o'clock period, which shows the most significant demand.

- **Predictive Scheduling**: Use historical data to predict future throughput patterns, allowing for better workforce 
scheduling and resource allocation, especially during peak hours like `{top_6_hours.index[0]}` o'clock and 
`{top_6_hours.index[1]}` o'clock, and `{top_6_hours.index[5]}` o'clock.

By leveraging these insights and recommendations, airport operators can better align their resources to handle peak 
periods efficiently and minimize any potential bottlenecks in the bag screening process. 
""")

# Plot throughput by 15-minute intervals
st.write("### Throughput by 15-Minute Intervals")

fig_throughput_15min = px.line(
    throughput_by_15_min,
    x=throughput_by_15_min.index,
    y=throughput_by_15_min.values,
    labels={'x': 'Time Interval', 'y': 'Number of Bags'},
    title='Throughput by 15-Minute Intervals'
)

# Adjust figure
fig_throughput_15min.update_layout(
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=xtick_size),
        title=dict(text='Time Interval', font=dict(size=xlabel_size))
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size),
        title=dict(text='Number of Bags', font=dict(size=ylabel_size))
    ),
    width=width,
    height=height
)

# Display the plot
st.plotly_chart(fig_throughput_15min)

# Calculate daily throughput and average
fifteen_min_throughput = throughput_by_15_min.sum()
fifteen_min_average = throughput_by_15_min.mean()

# Show the analysis
st.markdown(f""" 
#### Throughput by 15-Minute Intervals Insights
- How many bags are processed each 15-Minute intervals?:  
  #### `{fifteen_min_throughput:,} number of bags processed.`
- What is the 15-Minute average number of bags processed?  
  #### `{fifteen_min_average:.2f} average number of bags processed each 15-Minute.`
""")

# Plot throughput by hour
st.write("### Throughput by 15-Min Intervals with Top 6 Highlighted")

# Top 6 busiest 15-minute intervals
top_6_intervals = throughput_by_15_min.sort_values(ascending=False).head(6)

# Create the initial line plot
fig_throughput_15min = px.line(
    throughput_by_15_min,
    x=throughput_by_15_min.index,
    y=throughput_by_15_min.values,
    labels={'x': 'Time Interval', 'y': 'Number of Bags'},
    title='Throughput by 15-Minute Intervals with Top 6 Highlighted'
)

# Highlight top 6 intervals
fig_throughput_15min.add_trace(
    go.Scatter(
        x=top_6_intervals.index,
        y=top_6_intervals.values,
        mode="markers+text",
        text=[f"{val} bags" for val in top_6_intervals.values],
        textposition="top center",
        marker=dict(color="red", size=10),
        name="Top 6 Intervals"
    )
)

# Adjust figure layout for the line chart
fig_throughput_15min.update_layout(
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=xtick_size),
        title=dict(text='Time Interval', font=dict(size=xlabel_size))
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size),
        title=dict(text='Number of Bags', font=dict(size=ylabel_size))
    ),
    width=width,
    height=height
)

# Display the plot
st.plotly_chart(fig_throughput_15min)

# Display Top 6 15-Minute Intervals as custom metrics
st.markdown(f""" 
#### What are the peak 15-Minute Intervals when the most bags are processed?
- Top 6 15-Minute Intervals by Throughput
""")

# Create two rows of columns for 15-minute intervals
col1, col2, col3 = st.columns(3)  # First row
col4, col5, col6 = st.columns(3)  # Second row

blue_colors = [
    "#0000FF",  # Top 1 Blue (Pure Blue)
    "#0000CC",  # Top 2 Blue (Dark Blue)
    "#0033FF",  # Top 3 Blue (Bright Blue)
    "#3366FF",  # Top 4 Blue (Strong Blue)
    "#66B2FF",  # Top 5 Blue (Sky Blue)
    "#99CCFF"  # Top 6 Blue (Light Sky Blue)
]

# Loop through top 6 intervals and assign metrics to the columns
for idx, (interval, count) in enumerate(top_6_intervals.items()):
    day_of_week = pd.to_datetime(day).day_name()  # Get the day of the week
    metric_html = top_metric(
        label=f"Top-{idx + 1} Interval:",
        value=str(interval) + f"<br>{day_of_week}",  # Convert "interval" timestamp to string for display
        delta=f"Number of Bags: {count}",
        color="white",
        bg_color=blue_colors[idx]
    )

    if idx < 3:
        with [col1, col2, col3][idx]:  # Place in the first row
            st.markdown(metric_html, unsafe_allow_html=True)
    else:
        with [col4, col5, col6][idx - 3]:  # Place in the second row
            st.markdown(metric_html, unsafe_allow_html=True)

st.markdown(f"""## Chapter - 2""")

# Peak Day of Week
st.write("### Peak Days of Week Analysis")
st.write(" - What are the busiest days of the week for bag screening?")
st.write(
    " - Can operator schedules be optimized to align with peak days to improve system performance and reliability?")

# Group data by week_of_day to calculate throughput
throughput_by_weekday = data.groupby('week_of_day').size()

# Sort throughput by days of the week in standard order (Monday to Sunday)
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
throughput_by_weekday = throughput_by_weekday.reindex(weekday_order)

# Identify the busiest day(s)
busiest_day = throughput_by_weekday.idxmax()
busiest_throughput = throughput_by_weekday.max()

# Get the top 3 busiest days
top_3_days = throughput_by_weekday.nlargest(3)

# Calculate mean and standard deviation for the throughput
mean_throughput = throughput_by_weekday.mean()
std_throughput = throughput_by_weekday.std()
n = len(throughput_by_weekday)  # number of days

# Calculate confidence interval bounds (95% CI)
confidence_interval = 1.96 * (std_throughput / np.sqrt(n))
upper_bound = mean_throughput + confidence_interval
lower_bound = mean_throughput - confidence_interval

# Create the bar plot with confidence intervals
fig_week_days = px.bar(
    throughput_by_weekday,
    x=throughput_by_weekday.index,
    y=throughput_by_weekday.values,
    labels={'x': 'Day of the Week', 'y': 'Total Throughput'},
    title='Total Throughput by Day of the Week with a Confidence Interval',
    color=throughput_by_weekday.values,
    color_continuous_scale='Blues'
)

# Add lines for mean and confidence intervals
fig_week_days.add_hline(y=upper_bound, line_dash="dash", line_color="orange", annotation_text="Upper CI (95%)")
fig_week_days.add_hline(y=mean_throughput, line_dash="dash", line_color="green", annotation_text="Mean Throughput")
fig_week_days.add_hline(y=lower_bound, line_dash="dash", line_color="orange", annotation_text="Lower CI (95%)")

# Show values on bars
fig_week_days.update_traces(text=throughput_by_weekday.values)

# Update layout
fig_week_days.update_layout(
    width=width,
    height=height,
    xaxis=dict(tickfont=dict(size=xtick_size), title=dict(text='Week of Day', font=dict(size=xlabel_size))),
    yaxis=dict(tickfont=dict(size=ytick_size), title=dict(text='Throughput', font=dict(size=ylabel_size)))
)

# Display the plot and metrics in Streamlit
st.plotly_chart(fig_week_days)

# Display metrics
st.write("#### Top 3 Day of the Week by Throughput")

# Create three columns for metrics
col1, col2, col3 = st.columns(3)


# Define custom HTML for metrics from your existing code
def top_metric(label, value, delta, color, bg_color):
    return f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;
                padding: 10px; margin: 5px; border-radius: 10px; background-color: {bg_color}; width: 100%;">
        <h5 style="color: {color}; margin: 5px 0;">{label}</h5>
        <p style="font-size: 20px; font-weight: bold; margin: 0px 0;">{value}</p>
        <p style="font-size: 18px; margin: 0;">{delta}</p>
    </div>
    """


# Create cards for the top 3 busiest days
blue_gradient = ["#0033FF",  # Top 1 Blue (Bright Blue)
                 "#3366FF",  # Top 2 Blue (Strong Blue)
                 "#66B2FF"  # Top 3 Blue (Sky Blue)
                 ]

for idx, (day, count) in enumerate(top_3_days.items()):
    # Directly use the day name for display
    day_of_week = day
    metric_html = top_metric(
        label=f"Top-{idx + 1} Day:",
        value=f"{day_of_week}",
        delta=f"Number of Bags: {count}",
        color="white",
        bg_color=blue_gradient[idx]  # Assign gradient color for the metric
    )

    with [col1, col2, col3][idx]:  # Place in the first row
        st.markdown(metric_html, unsafe_allow_html=True)


# Display insights based on the top 3 days
st.markdown(f""" 
### Peak Days of Week Insights
- What are the busiest days of the week for bag screening? \n
Based on the analysis of throughput by the day of the week, the data reveals a clear trend in bag screening activity: \n
`{top_3_days.index[0]}` stands out as the busiest day, with `{top_3_days.values[0]:,}` bags processed. 
This suggests a peak in travel activity, likely due to weekend travelers returning or preparing for weekday commitments. \n
`{top_3_days.index[1]}`, with `{top_3_days.values[1]:,}` bags, ranks as the second busiest day, consistent with a high
 volume of leisure or weekend travelers. \n
`{top_3_days.index[2]}`, processing `{top_3_days.values[2]:,}` bags, is the third busiest day, indicating that the 
weekend travel rush likely starts on Fridays. \n
- **Observations:** \n
**Weekend Dominance**: The data indicates that weekends (Friday through Sunday) consistently experience the
 highest throughput compared to weekdays. \n
**Midweek Stability**: The remaining weekdays likely have lower and more stable screening activity, as people are
 less inclined to travel during these periods. \n
This trend highlights the need for resource optimization during the weekend, particularly on Sundays and Saturdays, 
to handle the increased volume efficiently.
- Can operator schedules be optimized to align with peak hours to improve system performance and reliability? \n
From the analysis of bag throughput, the busiest days for bag screening are clearly concentrated over the weekend,
 specifically: \n
`{top_3_days.index[0]}` : The busiest day, indicating a significant surge in travel activity. \n
`{top_3_days.index[1]}`: A close second, highlighting the sustained high demand over the weekend. \n
`{top_3_days.index[2]}`: A notable increase compared to other weekdays, marking the start of the weekend travel rush. \n
This pattern underscores the need for enhanced staffing during weekends to meet the increased demand,
 especially on these peak days.
- **Recommendations:** \n
**Increase Staffing on Peak Days:** Ensure that operator availability is significantly enhanced 
on `{top_3_days.index[2]}`, `{top_3_days.index[1]}`, and `{top_3_days.index[0]}` to meet the elevated demand
 during these peak days. \n
**Reduce Staffing on Low-Demand Days:** Consider lowering operator allocation on traditionally
 quieter days to improve resource efficiency. \n
**Train Operators for Critical Days:** Provide specialized training and tools to operators working on
`{top_3_days.index[2]}`, `{top_3_days.index[1]}`, and `{top_3_days.index[0]}` to handle increased escalations effectively. \n
**Utilize Predictive Scheduling Models:** Use historical data to predict demand patterns and guide staffing decisions,
 ensuring an optimal match between operator availability and screening needs.
""")

st.markdown(f"""## Chapter - 3""")

st.markdown(f"""### System Bottlenecks and Time-Outs""")
st.write("- How significant is the issue of time-out results across machines and clusters?")
st.write("- Are certain machines more prone to time-out situations than others?")
st.write("- During which days are time-outs most prevalent?")
st.write("- During which times are time-outs most prevalent?")

# Data Manipulation for "Time Out" Section
timeout_data = data[data['scan_machine_result_reason'] == 'Time out']
timeout_percentage = (len(timeout_data) / len(data)) * 100
timeout_by_day = timeout_data.groupby('day').size()
timeout_by_hour = timeout_data.groupby('hour').size()

# Group by machine and cluster to calculate percentages
timeout_by_machine = timeout_data['scan_machine_id'].value_counts(normalize=True) * 100
timeout_by_cluster = timeout_data['scan_machine_cluster'].value_counts(normalize=True) * 100

# Plot "Time Out" Cases by Day
st.write('### "Time Out" Cases by Day')
fig_timeout_day = px.bar(timeout_by_day, x=timeout_by_day.index, y=timeout_by_day.values,
                         labels={'x': 'Day', 'y': 'Number of Time Outs'},
                         title='"Time Out" Cases by Day')
fig_timeout_day.update_traces(marker=dict(color='red'),
                              text=timeout_by_day.values, textposition='outside',
                              hovertemplate='Day: %{x}<br>Time Outs: %{y}<extra></extra>')

# Adjust figure
fig_timeout_day.update_layout(
    margin=dict(t=40, b=40, l=40, r=40),
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=xtick_size),  # Rotate x-tick values and set font size
        title=dict(text='', font=dict(size=xlabel_size))  # Set x-axis title and size
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size),  # Set y-tick font size
        title=dict(text='', font=dict(size=ylabel_size))  # Set y-axis title and size
    ),
    width=width,
    height=height
)

# Display the plot
st.plotly_chart(fig_timeout_day)

# Convert the data to DataFrame for a cleaner presentation
machine_timeout_df = timeout_by_machine.reset_index()
machine_timeout_df.columns = ['Machine', 'Percentage']

cluster_timeout_df = timeout_by_cluster.reset_index()
cluster_timeout_df.columns = ['Cluster', 'Percentage']

# Display the analysis
st.markdown(f"""
#### Time-Out by Day Insights
- How significant is the issue of "time-out" results across machines and clusters?  
###### Initial Analysis: Overall 'time out' percentage is: `{round(timeout_percentage, 2)}%`
Let's conduct a more detailed analysis of 'time-out' cases by examining them for each machine, each cluster,
and breaking them down by day and hour.
""")

# Top 6 Days and Hours with "Time Out"
top_6_timeout_days = timeout_by_day.sort_values(ascending=False).head(6)
top_6_timeout_hours = timeout_by_hour.sort_values(ascending=False).head(6)

# Assign a color gradient for the top 6 busiest days and hours
day_gradient = [
    "#FF4500",  # Top 1 Orange Red
    "#FF6347",  # Top 2 Tomato
    "#FF8C00",  # Top 3 Dark Orange
    "#FFA500",  # Top 4 Orange
    "#FFB733",  # Top 5 Medium Orange
    "#FFCC66"  # Top 6 Light Orange
]

hour_gradient = [
    "#6A5ACD",  # Top 1 Slate Blue
    "#7B68EE",  # Top 2 Medium Slate Blue
    "#9370DB",  # Top 3 Medium Purple
    "#BA55D3",  # Top 4 Orchid
    "#DA70D6",  # Top 5 Pale Violet Red
    "#D8BFD8"  # Top 6 Thistle
]

# Generate colors for days
day_colors = ["#D3D3D3"] * len(timeout_by_day)  # Default color for all bars
for idx, (day, _) in enumerate(top_6_timeout_days.items()):
    day_idx = timeout_by_day.index.get_loc(day)
    day_colors[day_idx] = day_gradient[idx]

# Generate colors for hours
hour_colors = ["#D3D3D3"] * len(timeout_by_hour)  # Default color for all bars
for idx, (hour, _) in enumerate(top_6_timeout_hours.items()):
    hour_idx = timeout_by_hour.index.get_loc(hour)
    hour_colors[hour_idx] = hour_gradient[idx]

# Plot "Time Out" Cases by Day with Highlighted Colors
st.write('### "Time Out" Cases by Day with Top 6 Highlighted')
fig_timeout_day = px.bar(
    timeout_by_day,
    x=timeout_by_day.index,
    y=timeout_by_day.values,
    labels={'x': 'Day', 'y': 'Number of Time Outs'},
    title='"Time Out" Cases by Day with Top 6 Highlighted'
)

# Apply colors to bars
fig_timeout_day.update_traces(
    marker=dict(color=day_colors),  # Assign color list to bars
    text=timeout_by_day.values,  # Show values as text on bars
    textposition='outside'
)

fig_timeout_day.update_layout(
    xaxis=dict(tickangle=0, tickfont=dict(size=12), title="Day"),
    yaxis=dict(title="Number of Time Outs"),
    width=width,
    height=height
)
st.plotly_chart(fig_timeout_day)

st.markdown(f""" 
#### During which days are time-outs most prevalent?
- Top 6 Days by 'Time Out
""")

col1, col2, col3 = st.columns(3)  # First row
col4, col5, col6 = st.columns(3)  # Second row

for idx, (day, count) in enumerate(top_6_timeout_days.items()):
    day_of_week = pd.to_datetime(day).day_name()  # Get the day of the week
    metric_html = top_metric(
        label=f"Top-{idx + 1} Day:",
        value=str(day) + f" {day_of_week}",
        delta=f"Time Outs: {count}",
        color="white",
        bg_color=day_gradient[idx]
    )
    if idx < 3:
        with [col1, col2, col3][idx]:
            st.markdown(metric_html, unsafe_allow_html=True)
    else:
        with [col4, col5, col6][idx - 3]:
            st.markdown(metric_html, unsafe_allow_html=True)

# Plot "Time Out" Cases by Hour
st.write('### "Time Out" Cases by Hour')
fig_timeout_hour = px.bar(timeout_by_hour, x=timeout_by_hour.index, y=timeout_by_hour.values,
                          labels={'x': 'Hour', 'y': 'Number of Time Outs'},
                          title='"Time Out" Cases by Hour')
fig_timeout_hour.update_traces(marker=dict(color='purple'),
                               text=timeout_by_hour.values, textposition='outside',
                               hovertemplate='Hour: %{x}<br>Time Outs: %{y}<extra></extra>')

# Adjust figure
fig_timeout_hour.update_layout(
    margin=dict(t=40, b=40, l=40, r=40),
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=xtick_size),  # Rotate x-tick values and set font size
        title=dict(text='Hour', font=dict(size=xlabel_size))  # Set x-axis title and size
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size),  # Set y-tick font size
        title=dict(text='Number of Time Outs', font=dict(size=ylabel_size))  # Set y-axis title and size
    ),
    width=width,
    height=height
)

st.plotly_chart(fig_timeout_hour)

# Plot "Time Out" Cases by Hour with Top 6 Highlighted
st.write('### "Time Out" Cases by Hour with Top 6 Highlighted')

# Gradient colors for top 6 hours
purple_gradient = [
    "#800080",  # Top 1 Purple (Pure Purple)
    "#660066",  # Top 2 Purple (Dark Purple)
    "#993399",  # Top 3 Purple (Darker Purple)
    "#9966CC",  # Top 4 Purple (Strong Purple)
    "#CC99CC",  # Top 5 Purple (Moderate Purple)
    "#D9B3D9"  # Top 6 Purple (Light Dark Purple)
]

# Default bar color
default_color = "#D3D3D3"  # Light gray for all non-top 6 hours
hour_colors = [default_color] * len(timeout_by_hour)

# Assign gradient colors to top 6 hours
for idx, (hour, _) in enumerate(top_6_timeout_hours.items()):
    hour_colors[hour] = purple_gradient[idx]

# Bar plot with highlighted top 6 hours
fig_timeout_hour = px.bar(
    timeout_by_hour,
    x=timeout_by_hour.index,
    y=timeout_by_hour.values,
    labels={'x': 'Hour', 'y': 'Number of Time Outs'},
    title='"Time Out" Cases by Hour with Top 6 Highlighted'
)

# Apply the color gradient to the bars
fig_timeout_hour.update_traces(
    marker=dict(color=hour_colors),  # Dynamically assign colors
    text=timeout_by_hour.values,  # Show values on bars
    textposition='outside'  # Position text outside bars
)

# Adjust layout for readability
fig_timeout_hour.update_layout(
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=12),
        title="Hour"
    ),
    yaxis=dict(
        title="Number of Time Outs"
    ),
    width=width,
    height=height
)

# Display the bar chart in Streamlit
st.plotly_chart(fig_timeout_hour)

# Display Top 6 Hours as Custom Metrics
st.markdown(f""" 
#### During which hours are time-outs most prevalent?
- Top 6 Hours by 'Time Out'
""")

# Create two rows of columns for the metrics
col1, col2, col3 = st.columns(3)  # First row
col4, col5, col6 = st.columns(3)  # Second row

# Display the metrics with background colors
for idx, (hour, count) in enumerate(top_6_timeout_hours.items()):
    metric_html = top_metric(
        label=f"Top-{idx + 1} Hour:",
        value=f"{hour}:00",
        delta=f"Time Outs: {count}",
        color="white",
        bg_color=purple_gradient[idx]  # Use the purple gradient for metrics
    )
    if idx < 3:
        with [col1, col2, col3][idx]:  # Place in the first row
            st.markdown(metric_html, unsafe_allow_html=True)
    else:
        with [col4, col5, col6][idx - 3]:  # Place in the second row
            st.markdown(metric_html, unsafe_allow_html=True)

# Filter the data for "Time Out" cases
timeout_data = data[data['scan_machine_result_reason'] == 'Time out']

# Group by scan_machine_id to get counts of time-out cases per machine
timeout_by_machine = timeout_data.groupby('scan_machine_id').size()

# Calculate the percentage of time-outs for each machine
total_cases_by_machine = data.groupby('scan_machine_id').size()
timeout_percentage_by_machine = (timeout_by_machine / total_cases_by_machine) * 100

# Prepare a DataFrame for visualization
timeout_df = timeout_percentage_by_machine.reset_index()
timeout_df.columns = ['scan_machine_id', 'timeout_percentage']
timeout_df = timeout_df.sort_values(by='timeout_percentage', ascending=False).round(2)

#  Get top machine by timeout percentage
peak_machine_by_timeout_percentage = timeout_df.head(1)  #

# Extract the top machine's ID and timeout percentage
top_machine_id = peak_machine_by_timeout_percentage['scan_machine_id'].values[0]
top_timeout_percentage = peak_machine_by_timeout_percentage['timeout_percentage'].values[0]

# Plotting with Plotly
fig = px.bar(
    timeout_df,
    x='scan_machine_id',
    y='timeout_percentage',
    title="Percentage of Time-Out Cases by Machine",
    labels={'scan_machine_id': 'Machine', 'timeout_percentage': 'Time-Out Percentage (%)'},
    text='timeout_percentage',
    color='timeout_percentage',
    color_continuous_scale='Viridis'
)

fig.update_layout(
    xaxis_title="X-Ray Machine",
    yaxis_title="Time-Out Percentage (%)",
    width=width,
    height=height
)

st.write("### Time-Out Percentage by Machine")

# Display the plot
st.plotly_chart(fig)

# Calculate the total number of time-outs
total_timeout_cases = timeout_data.shape[0]

# Calculate the percentage of time-outs for each cluster
timeout_percentage_by_cluster = (timeout_by_cluster / total_timeout_cases) * 100

# Prepare a DataFrame for visualization
timeout_cluster_df = timeout_percentage_by_cluster.reset_index()
timeout_cluster_df.columns = ['scan_machine_cluster', 'timeout_percentage']
timeout_cluster_df = timeout_cluster_df.round(2)

# Plotting the pie chart using Plotly
fig = px.pie(
    timeout_cluster_df,
    names='scan_machine_cluster',
    values='timeout_percentage',
    title='Time-Out Percentage by Clusters',
    hole=0.4,  # Creates a donut chart
    color='scan_machine_cluster',
    color_discrete_map={
        'Cluster A': 'blue',
        'Cluster B': 'green'
    }
)

fig.update_traces(textinfo='percent+label')

# Display the chart in Streamlit
st.write("### Time-Out Percentage by Clusters")
st.plotly_chart(fig)

# Display the analysis
st.markdown(f"""
### Time-Out Insights""")

# Display Machine Timeout Table
st.markdown("##### Time-Out Percentage by Machine")
st.dataframe(machine_timeout_df.style.format({'Percentage': '{:.2f}%'}), use_container_width=True)

# Display Cluster Timeout Table
st.markdown("##### Time-Out Percentage by Cluster")
st.dataframe(cluster_timeout_df.style.format({'Percentage': '{:.2f}%'}), use_container_width=True)

st.markdown(f"""
The analysis of "time-out" percentages across Clusters reveals that these cases are distributed relatively evenly among
 all machines. This indicates that no single cluster is disproportionately contributing to the "time-out" occurrences.
  The uniformity suggests that systemic factors, such as overall workflow or operational constraints, may play a 
  more significant role in "time-out" events than cluster-specific issues.
- How significant is the issue of "time-out" results across machines and clusters?  \n
Overall 'time out' percentage is: `{round(timeout_percentage, 2)}%` \n
The issue of "time-out" results across machines and clusters is relatively significant, though not overwhelming. 
With an overall time-out percentage of `{round(timeout_percentage, 2)}%`, this suggests that the vast majority of 
interactions are successful. In practical terms, while almost all processes are completing without issues, a small
 but notable fraction `{round(timeout_percentage, 2)}%` interactions—does lead to a time-out. This means that while 
 the system generally performs well, there is still a subset of interactions that could benefit from further
  investigation to identify the underlying causes of the time-outs. Addressing these could enhance the user
   experience and improve overall system reliability.
- Are certain machines more prone to time-out situations than others? \n
Yes, the analysis indicates that certain machines exhibit a higher propensity for time-out situations than others.
 Specifically, the `{top_machine_id}` is identified as the most susceptible, with the highest time-out percentage of 
 `{top_timeout_percentage}`. This means that, compared to other machines,the `{top_machine_id}` is significantly more
  likely to experience time-outs. Understanding these patterns is crucial for operational efficiency, as frequent
   time-outs can lead to delays and decreased productivity. To mitigate this issue, it would be beneficial to 
   investigate the underlying causes for the `{top_machine_id}`’s higher time-out rate. Factors such as machine age,
    operational load, maintenance schedules, or environmental conditions may play a role. By addressing these aspects, 
    we can enhance the reliability of Machine 7 and improve overall workflow efficiency.
""")

st.markdown(f"""## Chapter - 4""")

st.markdown(f"""### Machine and Cluster Utilization""")
st.write(" - Are bags distributed equitably across machines and clusters?")
st.write(" - Are some machines handling disproportionately higher loads?")
st.write(" - Do machines with higher workloads correlate with higher malfunction rates?")

# Data Manipulation for Bag Distribution Across Machines Section
# Bags per machine
bags_per_machine = data.groupby('scan_machine_id').size()

# Bags per cluster
bags_per_cluster = data.groupby('scan_machine_cluster').size()

# Calculate mean values
mean_bags_per_machine = bags_per_machine.mean()
mean_bags_per_cluster = bags_per_cluster.mean()

# Calculate total number of bags per machine and per cluster
bags_per_machine = data.groupby('scan_machine_id').size()
bags_per_cluster = data.groupby('scan_machine_cluster').size()

# Standard deviation
std_bags_per_machine = bags_per_machine.std()
std_bags_per_cluster = bags_per_cluster.std()

# Coefficient of variation (CV = std / mean)
cv_bags_per_machine = std_bags_per_machine / mean_bags_per_machine
cv_bags_per_cluster = std_bags_per_cluster / mean_bags_per_cluster

# Mean Absolute Deviation (MAD)
mad_bags_per_machine = (bags_per_machine - mean_bags_per_machine).abs().mean()
mad_bags_per_cluster = (bags_per_cluster - mean_bags_per_cluster).abs().mean()

# Plot Bag Distribution Across Machines
st.write("### Bag Distribution Across Machines")
fig_bag_dist_machine = px.bar(bags_per_machine, x=bags_per_machine.index, y=bags_per_machine.values,
                              labels={'x': 'Machine ID', 'y': 'Number of Bags'},
                              title='Bag Distribution Across Machines')
fig_bag_dist_machine.update_traces(marker=dict(color='teal'),
                                   text=bags_per_machine.values, textposition='outside',
                                   hovertemplate='Machine: %{x}<br>Bags: %{y}<extra></extra>')

# Adjust figure
fig_bag_dist_machine.update_layout(
    margin=dict(t=40, b=40, l=40, r=40),
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=xtick_size),  # Rotate x-tick values and set font size
        title=dict(text='Machine ID', font=dict(size=xlabel_size))  # Set x-axis title and size
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size),  # Set y-tick font size
        title=dict(text='Number of Bags', font=dict(size=ylabel_size))  # Set y-axis title and size
    ),
    width=width,
    height=height
)

# Display the plot
st.plotly_chart(fig_bag_dist_machine)

# Display the explanation
st.write("### Bag Distribution Metrics")
st.markdown(f"""
This section presents key metrics that provide insights into the bag distribution across different operational levels 
within the system. \n
The analysis is divided into two tiers: **Machine-Level Metrics** and **Cluster-Level Metrics**.

**Machine-Level Metrics** focus on individual machines and their performance in terms of bag distribution:
- **Mean bags per machine** indicates the average number of bags handled by each machine, revealing the overall 
effectiveness of machine operations. \n
Mean bags per machine: `{mean_bags_per_machine:.2f}`
- **Standard deviation (machines)** measures the variability in bag counts across machines, with a higher value 
indicating more inconsistency in performance. \n
Standard deviation (machines): `{std_bags_per_machine:.2f}`
- **Coefficient of Variation (machines)**, calculated as the ratio of the standard deviation to the mean, expresses
 this variability relative to the mean, allowing for comparisons across different datasets. \n
Coefficient of variation (machines): `{cv_bags_per_machine:.2f}`
- **Mean Absolute Deviation (machines)** quantifies the average deviation of bag counts from the mean, providing
 another measure of dispersion. \n
Mean Absolute Deviation (machines): `{mad_bags_per_machine:.2f}`

**Cluster-Level Metrics** aggregate data across clusters of machines to provide a broader perspective on operational
efficiency:
- **Mean bags per cluster** reflects the average number of bags processed within each cluster. \n
Mean bags per cluster: `{mean_bags_per_cluster:.2f}`
- **Standard deviation (clusters)** highlights the dispersion of bag counts among clusters. \n
Standard deviation (clusters): `{std_bags_per_cluster:.2f}`
- **Coefficient of Variation (clusters)** serves a similar purpose to its machine-level counterpart, offering a view 
of relative variability across clusters. \n
Coefficient of variation (clusters): `{cv_bags_per_cluster:.2f}`
- **Mean Absolute Deviation (clusters)** offers insights into the consistency of bag processing at the cluster level,
indicating how closely individual clusters adhere to the average performance. \n
Mean Absolute Deviation (clusters): `{mad_bags_per_cluster:.2f}`

Together, these metrics provide a comprehensive overview of bag distribution, enabling stakeholders to identify trends, 
assess performance, and implement improvements effectively.
""")

# Highlight machines and clusters with disproportionately higher or lower loads
high_load_threshold_machine = mean_bags_per_machine + 2 * std_bags_per_machine
low_load_threshold_machine = mean_bags_per_machine - 2 * std_bags_per_machine

high_load_threshold_cluster = mean_bags_per_cluster + 2 * std_bags_per_cluster
low_load_threshold_cluster = mean_bags_per_cluster - 2 * std_bags_per_cluster

disproportionate_machines = bags_per_machine[(bags_per_machine > high_load_threshold_machine) |
                                             (bags_per_machine < low_load_threshold_machine)]
disproportionate_clusters = bags_per_cluster[(bags_per_cluster > high_load_threshold_cluster) |
                                             (bags_per_cluster < low_load_threshold_cluster)]

# Plot Bag Distribution Across Machines
st.write("### Bag Distribution Across Machines with Load Confidence Interval")
fig_bag_dist_machine = px.bar(bags_per_machine, x=bags_per_machine.index, y=bags_per_machine.values,
                              labels={'x': 'Machine ID', 'y': 'Number of Bags'},
                              title='Bag Distribution Across Machines')
fig_bag_dist_machine.update_traces(marker=dict(color='teal'),
                                   text=bags_per_machine.values, textposition='outside',
                                   hovertemplate='Machine: %{x}<br>Bags: %{y}<extra></extra>')

fig_bag_dist_machine.add_hline(y=high_load_threshold_machine, line_dash="dash",
                               line_color="red", annotation_text="High Load Threshold")
fig_bag_dist_machine.add_hline(y=mean_bags_per_machine, line_dash="dash",
                               line_color="green", annotation_text="Load Mean (Average)")
fig_bag_dist_machine.add_hline(y=low_load_threshold_machine, line_dash="dash",
                               line_color="blue", annotation_text="Low Load Threshold")

# Adjust figure
fig_bag_dist_machine.update_layout(
    margin=dict(t=40, b=40, l=40, r=40),
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=xtick_size),  # Rotate x-tick values and set font size
        title=dict(text='Machine ID', font=dict(size=xlabel_size))  # Set x-axis title and size
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size),  # Set y-tick font size
        title=dict(text='Number of Bags', font=dict(size=ylabel_size))  # Set y-axis title and size
    ),
    width=width,
    height=height
)

# Display the plot
st.plotly_chart(fig_bag_dist_machine)

# Identify top 6 machines with the highest number of bags
top_6_machines = bags_per_machine.sort_values(ascending=False).head(6)

# Sort all machines by the number of bags in descending order for plotting
sorted_bags_per_machine = bags_per_machine.sort_values(ascending=False)

# Identify the top and last value indices
top_value_label = sorted_bags_per_machine.idxmax()  # Get the label of the max value
last_value_label = sorted_bags_per_machine.idxmin()  # Get the label of the min value

# Convert labels to positional indices
top_value_index = sorted_bags_per_machine.index.get_loc(top_value_label)
last_value_index = sorted_bags_per_machine.index.get_loc(last_value_label)

# Create a color list, defaulting to teal
colors = ['teal'] * len(sorted_bags_per_machine)

# Assign specific colors for the top and last values
colors[top_value_index] = 'green'  # Green for the top value
colors[last_value_index] = 'red'  # Red for the last value

# Create a bar chart for all machines with sorted values
st.write("### Sorted Bag Distribution by Machines with Load Confidence Interval")
fig_bag_dist_machine = px.bar(
    sorted_bags_per_machine,  # Use the sorted series here
    x=sorted_bags_per_machine.index,
    y=sorted_bags_per_machine.values,
    labels={'x': 'Machine ID', 'y': 'Number of Bags'},
    title='Sorted Bag Distribution by Machines'
)

# Apply the custom colors to the bars
fig_bag_dist_machine.update_traces(
    marker=dict(color=colors),  # Dynamically assign colors
    text=sorted_bags_per_machine.values,  # Add values as text on the bars
    textposition='outside'  # Position text outside the bars
)

fig_bag_dist_machine.add_hline(y=high_load_threshold_machine, line_dash="dash",
                               line_color="red", annotation_text="High Load Threshold")
fig_bag_dist_machine.add_hline(y=mean_bags_per_machine, line_dash="dash",
                               line_color="green", annotation_text="Load Mean (Average)")
fig_bag_dist_machine.add_hline(y=low_load_threshold_machine, line_dash="dash",
                               line_color="blue", annotation_text="Low Load Threshold")

# Adjust the layout
fig_bag_dist_machine.update_layout(
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=xtick_size),
        title=dict(text='Machine ID', font=dict(size=xlabel_size))
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size),
        title=dict(text='Number of Bags', font=dict(size=ylabel_size))
    ),
    width=width,
    height=height
)

# Display the chart
st.plotly_chart(fig_bag_dist_machine)

# Bar Plot for Bag Distribution Across Clusters
st.write("### Bag Distribution Across Clusters")
fig_cluster = px.bar(
    bags_per_cluster.sort_values(),
    x=bags_per_cluster.index,
    y=bags_per_cluster.values,
    title="Bag Distribution Across Clusters with Load Confidence Interval",
    labels={'x': 'Cluster', 'y': 'Number of Bags'}
)
fig_cluster.add_hline(y=high_load_threshold_cluster, line_dash="dash",
                      line_color="red", annotation_text="High Load Threshold")
fig_cluster.add_hline(y=mean_bags_per_cluster, line_dash="dash",
                      line_color="green", annotation_text="Load Mean (Average)")
fig_cluster.add_hline(y=low_load_threshold_cluster, line_dash="dash",
                      line_color="blue", annotation_text="Low Load Threshold")

fig_cluster.update_traces(marker=dict(color='gold'))

# Adjust figure
fig_cluster.update_layout(
    margin=dict(t=40, b=40, l=40, r=40),
    width=width,
    height=height
)

# Display the plot
st.plotly_chart(fig_cluster)

# Calculate descriptive statistics manually
bags_per_machine_stats = bags_per_machine.describe()
bags_per_cluster_stats = bags_per_cluster.describe()

# Box Plots to Show Spread and Outliers
st.write("### Distribution Spread and Outliers")

# Machine-Level Box Plot
fig_box_machine = px.box(
    bags_per_machine,
    title="Bag Count Distribution Across Machines",
    labels={'value': 'Number of Bags', 'variable': 'Machines'}
)

# Adding annotations for statistics
machine_annotations = [
    dict(
        x=1,  # Centered on the box plot
        y=bags_per_machine_stats['min'],
        text=f"Min: {bags_per_machine_stats['min']:.2f}",
        showarrow=False,
        yanchor="top"
    ),
    dict(
        x=1,
        y=bags_per_machine_stats['25%'],
        text=f"Q1: {bags_per_machine_stats['25%']:.2f}",
        showarrow=False,
        yanchor="bottom"
    ),
    dict(
        x=1,
        y=bags_per_machine_stats['50%'],
        text=f"Median: {bags_per_machine_stats['50%']:.2f}",
        showarrow=False,
        yanchor="bottom"
    ),
    dict(
        x=1,
        y=bags_per_machine_stats['75%'],
        text=f"Q3: {bags_per_machine_stats['75%']:.2f}",
        showarrow=False,
        yanchor="bottom"
    ),
    dict(
        x=1,
        y=bags_per_machine_stats['max'],
        text=f"Max: {bags_per_machine_stats['max']:.2f}",
        showarrow=False,
        yanchor="bottom"
    ),
]

fig_box_machine.update_layout(annotations=machine_annotations)

# Adjust layout
fig_box_machine.update_layout(
    margin=dict(t=40, b=40, l=40, r=40),
    width=width,
    height=height
)

# Display the plot
st.plotly_chart(fig_box_machine)

# Cluster-Level Box Plot
fig_box_cluster = px.box(
    bags_per_cluster,
    title="Bag Count Distribution Across Clusters",
    labels={'value': 'Number of Bags', 'variable': 'Clusters'}
)

# Adding annotations for statistics
cluster_annotations = [
    dict(
        x=1,
        y=bags_per_cluster_stats['min'],
        text=f"Min: {bags_per_cluster_stats['min']:.2f}",
        showarrow=False,
        yanchor="top"
    ),
    dict(
        x=1,
        y=bags_per_cluster_stats['25%'],
        text=f"Q1: {bags_per_cluster_stats['25%']:.2f}",
        showarrow=False,
        yanchor="bottom"
    ),
    dict(
        x=1,
        y=bags_per_cluster_stats['50%'],
        text=f"Median: {bags_per_cluster_stats['50%']:.2f}",
        showarrow=False,
        yanchor="bottom"
    ),
    dict(
        x=1,
        y=bags_per_cluster_stats['75%'],
        text=f"Q3: {bags_per_cluster_stats['75%']:.2f}",
        showarrow=False,
        yanchor="bottom"
    ),
    dict(
        x=1,
        y=bags_per_cluster_stats['max'],
        text=f"Max: {bags_per_cluster_stats['max']:.2f}",
        showarrow=False,
        yanchor="bottom"
    ),
]

fig_box_cluster.update_layout(annotations=cluster_annotations)

# Adjust layout
fig_box_cluster.update_layout(
    margin=dict(t=40, b=40, l=40, r=40),
    width=width,
    height=height
)

# Display the plot
st.plotly_chart(fig_box_cluster)

# Identify the top machine with the highest number of bags
top_machine = bags_per_machine.sort_values(ascending=False).head(1)

# Display the analysis
st.markdown(f""" ##### Bag Distribution Across Machines and Clusters Insights
- Are bags distributed equitably across machines? \n
The data suggests that bag distribution across machines is NOT equitable. The standard deviation (SD) of bag counts at 
the machine level reveals significant variability, indicating inconsistencies in machine utilization. For example, 
machine `{list(disproportionate_machines.index)[0]}` falls outside the load confidence intervals, highlighting that 
certain machines are handling disproportionate workloads, either too high or too low. \n
- Are bags distributed equitably across clusters? \n
Yes, at the cluster level, bag distribution appears more balanced. The standard deviation (SD) of cluster bag counts,
 combined with all values falling within the calculated load confidence intervals, suggests that clusters as a whole do 
 not exhibit substantial disparities in workload distribution. This indicates better operational uniformity at the 
 cluster level compared to individual machines. \n
- Are some machines handling disproportionately higher loads? \n
No, While there are variations among machines, no machines are handling disproportionately higher loads. This 
conclusion is supported by the observation that the bag count of the top machine
 `{top_machine.index[0]}` (`{top_machine.values[0]}` bags) remains below the calculated high-load threshold of 
 `{int(high_load_threshold_machine)}`. However, it is essential to monitor this threshold closely, as even slight 
 increases could push some machines into disproportionately high-load conditions.
- Do machines with higher workloads correlate with higher malfunction rates? \n
Currently, the dataset does not include information on machine malfunctions or error rates, preventing us from 
drawing any direct conclusions regarding the relationship between higher workloads and malfunction rates. 
To investigate this correlation further, incorporating machine performance and maintenance data would be beneficial. \n
##### Additional Observations and Recommendations:
- Machines with Lower Utilization: \n
Machines below the low-load threshold (`{int(low_load_threshold_machine)}`) may represent underutilized resources.
 Redistributing workloads from overburdened machines to these underutilized ones could improve operational efficiency 
 and extend machine longevity. \n
- Cluster-Level Uniformity: \n
The uniformity observed at the cluster level could serve as a model for optimizing machine-level workload distribution.
 Identifying best practices within consistently balanced clusters and replicating them across machines may help address
  machine-level inequities. \n
- Operational Resilience: \n
Machines or clusters handling significantly higher loads could be at risk of wear and tear or operational delays. 
Regularly assessing workload distribution and performing preventive maintenance on heavily utilized machines is 
crucial for maintaining system resilience. \n
- Future Data Needs: \n
Including data points like processing times, maintenance history, and error occurrences per machine could enhance 
the ability to analyze workload impacts on machine performance and identify further optimization opportunities.
""")

st.markdown(f"""## Chapter - 5""")

st.markdown(f"""### Screening Escalations and Level 2 Analysis""")
st.write(" - How many bags reach Level 2 screening, and what proportion"
         " does this represent relative to the total throughput?")
st.write(" - Are there trends in Level 2 escalations across time?")
st.write(" - Are there machines when Level 2 escalations are disproportionately higher?")

# Data Manipulation for Scan Machine Level Distribution Section
level_counts = data['scan_machine_level'].value_counts()

# Metrics for display
level_2_count = level_counts.get('Level 2', 0)
level_1_count = level_counts.get('Level 1', 0)
total_bags_processed = len(data)
level_2_proportion = level_2_count / total_bags_processed

total_bags = total_bags_processed
progress_level_1 = level_1_count / total_bags
progress_level_2 = level_2_count / total_bags

# Adding a summary of bags in Level 2 with enhanced styling
level_2_count = level_counts.get('Level 2', 0)  # Safely handle cases where 'Level 2' may not exist
level_1_count = level_counts.get('Level 1', 0)  # Get count for Level 1

# Ensure the 'level_counts.index' contains values like 'Level 1', 'Level 2'
level_labels = level_counts.index.tolist()

# Filter data for Level 2 screening
level_2_data = data[data['scan_machine_level'] == 'Level 2']

# Group Level 2 escalations by day
level_2_by_day = level_2_data.groupby(level_2_data['bag_scan_timestamp'].dt.date).size()

# Group data by machine and cluster for Level 2 escalations
level_2_by_machine = level_2_data.groupby('scan_machine_id').size()
level_2_by_cluster = level_2_data.groupby('scan_machine_cluster').size()

# Calculate proportion of Level 2 escalations per machine relative to total processed by each machine
machine_totals = data['scan_machine_id'].value_counts()
level_2_proportions = round((level_2_by_machine / machine_totals), 2).sort_values(ascending=False)

# Bar chart of bags at each screening level
st.write("### Number of Bags by Screening Level")

# Plotly Bar chart
fig_bar = px.bar(
    level_counts,
    x=level_counts.index,
    y=level_counts.values,
    labels={'x': 'Screening Level', 'y': 'Number of Bags'},
    title="Number of Bags by Screening Level",
    color=level_counts.index,
    color_discrete_map={
        'Level 2': 'coral',
        'Level 1': 'orange',
    }
)
fig_bar.update_traces(
    text=level_counts.values,
    textposition='outside',
    hovertemplate='Level: %{x}<br>Bags: %{y}<extra></extra>'
)

# Adjust figure
fig_bar.update_layout(
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=xtick_size),  # Rotate x-tick values and set font size
        title=dict(text='Screening Level', font=dict(size=xlabel_size))  # Set x-axis title and size
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size),  # Set y-tick font size
        title=dict(text='Number of Bags', font=dict(size=ylabel_size))  # Set y-axis title and size
    ),
    width=width,
    height=height
)

st.plotly_chart(fig_bar)

# Pie chart showing the proportion of bags at Level 2
st.write("### Proportion of Bags by Screening Level")

# Create pull values for the pie slices
pull_values = [0.1 if label == 'Level 2' else 0 for label in level_labels]

# Plotly Pie chart
fig_pie = px.pie(
    values=level_counts.values,
    names=level_labels,
    title="Proportion of Bags by Screening Level",
    color=level_labels,
    color_discrete_map={
        'Level 2': 'lightblue',
        'Level 1': 'orange'
    }
)

# Apply pull values to the pie chart to highlight Level 2
fig_pie.update_traces(pull=pull_values)

# Adjust figure
fig_pie.update_layout(
    margin=dict(t=40, b=40, l=40, r=40),
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=xtick_size),  # Rotate x-tick values and set font size
        title=dict(text='', font=dict(size=xlabel_size))  # Set x-axis title and size
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size),  # Set y-tick font size
        title=dict(text='', font=dict(size=ylabel_size))  # Set y-axis title and size
    ),
    width=640,
    height=480
)

# Display the pie chart
st.plotly_chart(fig_pie)

# Display metrics for each screening level
st.write("### Screening Level Bag Distribution Summary")

# Display the textual metrics in markdown
st.markdown(f"""
- How many bags reach Level 2 screening, 
and what proportion does this represent relative to the total throughput?
###### Total Bags Processed: `{total_bags_processed:,}`
###### Level 1 Bags Processed: `{level_1_count:,}`
###### Level 2 Bags Processed: `{level_2_count:,}`
###### Proportion of bags reaching level 2 is :`{level_2_proportion:.2%}.`
""")

# Progress Bar
st.markdown("#### Progress of Bags through Levels:")

# Show progress bars
st.progress(progress_level_1, text=f"Level 1: {level_1_count:,} bags")
st.progress(progress_level_2, text=f"Level 2: {level_2_count:,} bags")


# Custom HTML for display metrics with styling
def custom_metric(label, value, color, bg_color):
    return f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;
                padding: 15px; margin: 10px; border-radius: 10px; background-color: {bg_color}; width: 100%;">
        <h3 style="color: {color}; font-size: 22px; margin: 5px 0;">{label}</h3>
        <p style="font-size: 30px; font-weight: bold; margin: 5px 0;">{value}</p>
    </div>
    """


# Use columns for better layout
col1, col2 = st.columns(2)

# Display each metric with respective colors
with col1:
    st.markdown(custom_metric(
        label="Level 1 Bags",
        value=f"{level_1_count}",
        color="white",
        bg_color="#FFA500"  # Orange for Level 1
    ), unsafe_allow_html=True)

with col2:
    st.markdown(custom_metric(
        label="Level 2 Bags",
        value=f"{level_2_count}",
        color="white",
        bg_color="#FF6347"  # Coral for Level 2
    ), unsafe_allow_html=True)

# Display summary metrics
st.write(f"### Level 2 Escalations Over Days")

# Calculate Central Tendency
mean_level_2 = level_2_by_day.mean()
median_level_2 = level_2_by_day.median()

# Calculate Variability
std_level_2 = level_2_by_day.std()
variance_level_2 = level_2_by_day.var()

# Moving Averages
window_size = 7  # Window size for moving average (7 days for SMA)
sma_level_2 = level_2_by_day.rolling(window=window_size).mean()  # Simple Moving Average
ema_level_2 = level_2_by_day.ewm(span=window_size, adjust=False).mean()  # Exponential Moving Average

# Add moving averages to plot
fig_level2_days = px.line(
    level_2_by_day,
    labels={'index': 'Day', 'value': 'Level 2 Count'},
    title="Level 2 Escalations Over Days"
)

# Add Simple Moving Average (SMA) and Exponential Moving Average (EMA) to the plot
fig_level2_days.add_scatter(
    x=level_2_by_day.index,
    y=sma_level_2,
    mode='lines',
    name='7-Day SMA',
    line=dict(color='blue', dash='dash')
)

fig_level2_days.add_scatter(
    x=level_2_by_day.index,
    y=ema_level_2,
    mode='lines',
    name='7-Day EMA',
    line=dict(color='green', dash='dot')
)

# Display the plot with the moving averages
st.plotly_chart(fig_level2_days)

# Change Detection: Calculate daily differences
level_2_changes = level_2_by_day.diff().fillna(0)  # Difference from previous day

# Display the statistical metrics
st.markdown(f"""
##### Statistical Insights for Level 2 Escalations
- **Mean of Level 2 Escalations:** `{mean_level_2:.2f}`
- **Median of Level 2 Escalations:** `{median_level_2:.2f}`
- **Standard Deviation:** `{std_level_2:.2f}`
- **Variance:** `{variance_level_2:.2f}`
""")

# Trend Analysis using Moving Averages
st.markdown("""
##### Trend Analysis for Level 2 Escalations
- **Simple Moving Average (SMA, 7-day):** Shows the 7-day smoothed trend of Level 2 escalations.
- **Exponential Moving Average (EMA, 7-day):** Gives more weight to recent data for trend detection.

These moving averages help smooth out fluctuations and reveal long-term trends in the data.
""")

# Explanation of the moving averages
st.markdown("""
##### Observations from Trend Analysis:
- The **Simple Moving Average (SMA)** smoothes out the fluctuations and shows the general trend of Level 2 
escalations over a 7-day period. This trend highlights any overall upward or downward trends in the escalations.
- The **Exponential Moving Average (EMA)** places more weight on recent data, making it more sensitive to recent
 changes in the escalation counts. This can help identify sudden shifts or changes in the trend.

By comparing both the SMA and EMA, we can observe how quickly the data reacts to changes and whether the fluctuations
 are short-term or part of a long-term trend.
""")

# Display the analysis
st.markdown(f"""
#### Are there trends in Level 2 escalations across time?
After analyzing the plot "Level 2 Escalations Over Days" above, the data shows that the number of Level 2 escalations 
fluctuates across the observed period without a clear upward or downward trend. This suggests that the 
frequency of escalations to Level 2 remains relatively stable throughout July. \n
The escalation counts vary from day to day, but these variations appear random rather than following a
consistent pattern. While there are occasional spikes or drops in escalations, these do not occur
at regular intervals, nor do they align with specific days of the week or times of the month. \n
Overall, there are no noticeable trends in Level 2 escalations over time. This lack of a pattern
indicates that other factors, such as operational issues or specific characteristics of the bags 
being processed, might be influencing the escalations rather than time-based factors.
""")

# Proportion of Level 2 Escalations by Cluster
st.write("#### Proportion of Level 2 Escalations by Cluster")

# Visualization: Level 2 escalations by cluster
fig_level2_clusters = px.pie(
    values=level_2_by_cluster.values,
    names=level_2_by_cluster.index,
    title="Proportion of Level 2 Escalations by Cluster",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

# Adjust figure
fig_level2_clusters.update_layout(width=640, height=480)

# Display the plot
st.plotly_chart(fig_level2_clusters)

# Level 2 Escalations by Machine ID
st.write("#### Level 2 Escalations by Machine ID")

# Statistical Calculations for Each Machine
machine_means = level_2_by_machine
machine_stds = machine_means.std()  # Standard deviation of Level 2 counts

# Statistical Calculations
machine_mean = machine_means.mean()  # Overall mean
machine_std = machine_means.std()  # Overall standard deviation
confidence_level = 0.95

# Number of machines
n_machines = len(machine_means)

# Calculate overall confidence intervals
stderr = machine_std / np.sqrt(n_machines)  # Standard error
ci_range = stats.t.ppf((1 + confidence_level) / 2, n_machines - 1) * stderr  # CI range for t-distribution

# Compute scalar CI bounds
ci_lower = machine_mean - ci_range
ci_upper = machine_mean + ci_range

# Visualization: Level 2 escalations by machine
fig_level2_machines = px.bar(
    level_2_by_machine,
    x=level_2_by_machine.index,
    y=level_2_by_machine.values,
    labels={'index': 'Machine', 'value': 'Level 2 Count'},
    title="Level 2 Escalations by Machine ID with Level 2 Escalation Confidence Interval",
    color=level_2_by_machine.index,
)

# Add scalar horizontal lines for CI and mean
fig_level2_machines.add_hline(
    y=ci_upper,
    line_dash="dash",
    line_color="red",
    annotation_text="High Level 2 Escalation Threshold"
)
fig_level2_machines.add_hline(
    y=machine_mean,
    line_dash="dash",
    line_color="green",
    annotation_text="Level 2 Escalation Mean (Average)"
)
fig_level2_machines.add_hline(
    y=ci_lower,
    line_dash="dash",
    line_color="blue",
    annotation_text="Low Level 2 Escalation Threshold"
)

# Adjust figure
fig_level2_machines.update_layout(
    margin=dict(t=40, b=40, l=40, r=40),
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=xtick_size),  # Rotate x-tick values and set font size
        title=dict(text='Machine ID', font=dict(size=xlabel_size))  # Set x-axis title and size
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size),  # Set y-tick font size
        title=dict(text='Level 2 Count', font=dict(size=ylabel_size))  # Set y-axis title and size
    ),
    width=1080,
    height=800
)

# Add values as text on the bars
fig_level2_machines.update_traces(text=level_2_by_machine.values)

# Display the plot
st.plotly_chart(fig_level2_machines)

# Display machines with the highest Level 2 proportions
st.write("#### Machines with Level 2 Escalation Proportions")

# Statistical Calculations
level_2_mean = level_2_proportions.mean()
level_2_std = level_2_proportions.std()
level_2_variance = level_2_proportions.var()
confidence_level = 0.95

# Calculate the confidence interval for Level 2 proportions
n = len(level_2_proportions)  # Number of machines
stderr = level_2_std / np.sqrt(n)  # Standard error
ci_range = stats.t.ppf((1 + confidence_level) / 2, n - 1) * stderr
ci_lower = level_2_mean - ci_range
ci_upper = level_2_mean + ci_range

# Plot a horizontal bar chart for Level 2 proportions
fig_level2_high_machines_styled = px.bar(
    level_2_proportions,
    x=level_2_proportions.values,
    y=level_2_proportions.index,
    orientation='h',
    labels={'x': 'Level 2 Proportion', 'y': 'Machine ID'},
    title="Machines with Level 2 Escalation Proportions with Statistics",
    color=level_2_proportions.values,
    color_continuous_scale='Blues'
)

fig_level2_high_machines_styled.add_vline(x=ci_upper, line_dash="dash",
                                          line_color="red",
                                          annotation_text="High Level 2 Escalation Proportion Threshold")
fig_level2_high_machines_styled.add_vline(x=level_2_mean, line_dash="dash",
                                          line_color="green", annotation_text="Proportion Mean (Average)")
fig_level2_high_machines_styled.add_vline(x=ci_lower, line_dash="dash",
                                          line_color="blue", annotation_text="Low Proportion Threshold")

# Enhance layout
fig_level2_high_machines_styled.update_layout(
    width=width,
    height=height,
    yaxis=dict(tickfont=dict(size=xtick_size),
               title=dict(text='Machine ID', font=dict(size=ylabel_size))),
    xaxis=dict(tickfont=dict(size=xtick_size), title=dict(font=dict(size=xlabel_size))),
    annotations=[
        dict(
            xref="paper", yref="paper",
            x=1.05, y=1.15,
            text=f"<b>Statistics:</b><br>"
                 f"Mean: {level_2_mean:.2f}<br>"
                 f"Std Dev: {level_2_std:.2f}<br>"
                 f"Variance: {level_2_variance:.2f}<br>"
                 f"95% CI: [{ci_lower:.2f}, {ci_upper:.2f}]",
            showarrow=False,
            font=dict(size=12),
            align="left"
        )
    ]
)

# Add values as text on the bars
fig_level2_high_machines_styled.update_traces(
    text=level_2_proportions.values,
    textposition='outside'
)

# Display chart
st.plotly_chart(fig_level2_high_machines_styled)

# Get the machine ID with the highest level 2 escalation
top_level_2_scan_machine = level_2_proportions.idxmax()

# Assessing Machines with Disproportionately High Level 2 Escalations
disproportionate_machines = level_2_proportions[level_2_proportions > ci_upper]
disproportionate_machines_count = len(disproportionate_machines)

# Display the analysis
st.markdown(f""" 
### Screening Escalations and Level 2 Analysis Insights
- How many bags reach Level 2 screening, and what proportion does this represent relative to the total throughput?  
###### Total Bags Processed: `{total_bags_processed:,}`  
###### Level 1 Bags Processed: `{level_1_count:,}`  
###### Level 2 Bags Processed: `{level_2_count:,}`  
###### Proportion of bags reaching level 2 is: `{level_2_proportion:.2%}`  
- Are there trends in Level 2 escalations across time? \n
After analyzing the plot "Level 2 Escalations Over Days", the data shows that the number of Level 2 escalations 
fluctuates across the observed period without a clear upward or downward trend. This suggests that the frequency of
 escalations to Level 2 remains relatively stable throughout July.  
The escalation counts vary from day to day, but these variations appear random rather than following a consistent 
pattern. While there are occasional spikes or drops in escalations, these do not occur at regular intervals, nor do
 they align with specific days of the week or times of the month.  
Overall, there are no noticeable trends in Level 2 escalations over time. This lack of a pattern indicates that other 
factors, such as operational issues or specific characteristics of the bags being processed, might be influencing the
 escalations rather than time-based factors. \n
- Are there machines where Level 2 escalations are disproportionately higher? \n
Upon analysis of the data, it was found that the machine `{top_level_2_scan_machine}` had the highest proportion of 
Level 2 escalations compared to other machines. The average proportion of Level 2 escalations across all machines is
 approximately `{level_2_mean:.2%}`, with a confidence interval of +/- `{ci_range:.2%}`. \n
Further analysis reveals that `{disproportionate_machines_count}` machine(s) exhibit disproportionately high Level 2 
escalation rates, exceeding the upper confidence threshold of `{ci_upper:.2%}`. This indicates that these machines 
have a significantly higher rate of escalations compared to the average, which could point to specific operational 
issues or anomalies with those machines that may require further investigation. 
In particular, the machine `{top_level_2_scan_machine}` stands out as an outlier, with a Level 2 escalation rate 
that is significantly higher than the confidence interval's upper bound. This suggests that this machine's behavior
 is unusual and warrants further operational review.
""")

st.markdown(f"""## Chapter - 6""")

# Single vs Multiple screenings
st.write("### Single vs Multiple Screenings")
st.write(" - Are there instances of bags being re-screened unnecessarily after being cleared at Level 1 or Level 2?")
st.write(" - How frequently do recirculation incidents occur, and what are their potential causes?")
st.write("Let's conduct a more detailed analysis of Multiple Screenings cases by examining them for"
         " each machine, each cluster, and breaking them down by day and hour.")

# Data Manipulation for Multiple Screenings Section
multiple_screenings = data.groupby('bag_licence_plate').size()
recirculated_bags = multiple_screenings[multiple_screenings > 1]
cleared_then_reexamined = data[data['bag_licence_plate'].isin(recirculated_bags.index) &
                               (data['scan_machine_result'] == 'Cleared')]

# Visualization: Distribution of Screening Counts per Bag
st.write("#### Distribution of Screening Counts per Bag")

# Plotly Bar chart
screening_counts = multiple_screenings.value_counts().sort_index()
num_unique_values = len(screening_counts)

# Use the Set1 color map, making sure not to exceed its length
color_map = px.colors.qualitative.Set1
color_discrete_map = {str(i): color_map[i % len(color_map)] for i in range(num_unique_values)}

fig_screening_count = px.bar(
    screening_counts,
    x=screening_counts.index,
    y=screening_counts.values,
    labels={'x': 'Number of Screenings', 'y': 'Count of Bags'},
    title="Distribution of Screening Counts per Bag",
    color=screening_counts.index.astype(str),
    color_discrete_map=color_discrete_map
)

fig_screening_count.update_traces(text=screening_counts.values,
                                  textposition='outside',
                                  hovertemplate='Screenings: %{x}<br>Count: %{y}<extra></extra>')

# Adjust figure
fig_screening_count.update_layout(
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=xtick_size),  # Rotate x-tick values and set font size
        title=dict(text='Number of Screenings', font=dict(size=xlabel_size))  # Set x-axis title and size
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size),  # Set y-tick font size
        title=dict(text='Count of Bags', font=dict(size=ylabel_size))  # Set y-axis title and size
    ),
    width=width,
    height=height
)

st.plotly_chart(fig_screening_count)

# Visualizations for Top 10 Screenings
st.write("### Top 10 Screenings Distribution per Bag")

# Calculate the top 10 screenings
top_10_screenings = multiple_screenings.value_counts().sort_index().nlargest(10)

# Create a bar chart
fig_top_10 = px.bar(
    top_10_screenings,
    x=top_10_screenings.index.astype(str),
    y=top_10_screenings.values,
    labels={"x": "Number of Screenings", "y": "Count of Bags"},
    title="Top 10 Screenings Distribution per Bag",
    color=top_10_screenings.index,
    color_discrete_sequence=px.colors.qualitative.Set3
)

# Add hover information and text annotations
fig_top_10.update_traces(
    text=top_10_screenings.values,
    textposition="outside",
    hovertemplate="<b>Screenings:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>"
)

# Update layout for better display
fig_top_10.update_layout(
    xaxis=dict(title="Number of Screenings", tickangle=0),
    yaxis=dict(title="Count of Bags"),
    showlegend=False
)

# Adjust figure
fig_top_10.update_layout(
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=xtick_size),  # Rotate x-tick values and set font size
        title=dict(text='Number of Screenings', font=dict(size=xlabel_size))  # Set x-axis title and size
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size),  # Set y-tick font size
        title=dict(text='Count of Bags', font=dict(size=ylabel_size))  # Set y-axis title and size
    ),
    width=width,
    height=height
)

# Render the Plotly chart
st.plotly_chart(fig_top_10)


# Identify Bags Re-Screened After Clearance
cleared_bags = data[data['scan_machine_result'] == 'Cleared']
recirculated_bags = data.groupby('bag_licence_plate').size()
recirculated_after_clearance = cleared_bags[cleared_bags['bag_licence_plate'].isin(
    recirculated_bags[recirculated_bags > 1].index
)]

# Count and summarize
num_recirculated = len(recirculated_after_clearance)
total_cleared_bags = len(cleared_bags)
percent_recirculated = (num_recirculated / total_cleared_bags) * 100

# Frequency of Recirculation Incidents
recirculation_frequency = recirculated_bags.value_counts().sort_index()

# Investigate reasons for recirculation among recirculated bags
recirculated_data = data[data['bag_licence_plate'].isin(
    recirculated_bags[recirculated_bags > 1].index
)]

recirculated_reasons = recirculated_data['scan_machine_result_reason'].value_counts()

# Check machine and cluster involvement
machine_recirc = recirculated_data['scan_machine_id'].value_counts()
cluster_recirc = recirculated_data['scan_machine_cluster'].value_counts()

# Bags Re-Screened After Clearance
fig_recirculation = px.bar(
    x=['Non-Recirculated', 'Recirculated'],
    y=[total_cleared_bags - num_recirculated, num_recirculated],
    labels={'x': 'Recirculation Status', 'y': 'Count'},
    title='Bags Re-Screened After Clearance',
    color=['Non-Recirculated', 'Recirculated'],
    color_discrete_map={'Non-Recirculated': '#00C853', 'Recirculated': '#D50000'}
)

fig_recirculation.update_traces(
    text=[total_cleared_bags - num_recirculated, num_recirculated],
    textposition='outside',
    marker=dict(line=dict(width=1.5, color='black'))
)

fig_recirculation.update_layout(
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=xtick_size),
        title=dict(text='Recirculation Status', font=dict(size=xlabel_size))
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size),
        title=dict(text='Count', font=dict(size=ylabel_size))
    ),
    width=width,
    height=height
)

st.plotly_chart(fig_recirculation)

# Reasons for Recirculation
fig_reasons = px.bar(
    recirculated_reasons,
    x=recirculated_reasons.index,
    y=recirculated_reasons.values,
    labels={'x': 'Reason', 'y': 'Count'},
    title='Reasons for Recirculation',
    color=recirculated_reasons.index,
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig_reasons.update_traces(
    text=recirculated_reasons.values,
    textposition='outside',
    marker=dict(line=dict(width=1.5, color='black'))
)

fig_reasons.update_layout(
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=xtick_size),
        title=dict(text='Reason', font=dict(size=xlabel_size))
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size),
        title=dict(text='Count', font=dict(size=ylabel_size))
    ),
    width=width,
    height=height
)

st.plotly_chart(fig_reasons)

# Analyze Machine/Cluster Contribution
recirculation_machine_contribution = recirculated_data.groupby('scan_machine_id').size()
recirculation_cluster_contribution = recirculated_data.groupby('scan_machine_cluster').size()

# Time-based trends
recirculation_time_trends = recirculated_data.groupby(recirculated_data['bag_scan_timestamp'].dt.hour).size()

# Analyze relationship between screening levels and recirculation
screening_level_recirculation = recirculated_data['scan_machine_level'].value_counts()

# Machine Contribution to Recirculation
fig_machine_contribution = px.bar(
    recirculation_machine_contribution,
    x=recirculation_machine_contribution.index,
    y=recirculation_machine_contribution.values,
    labels={'x': 'Machine ID', 'y': 'Recirculated Bags'},
    title='Machine Contribution to Recirculation',
    color=recirculation_machine_contribution.index,
    color_discrete_sequence=px.colors.qualitative.Plotly
)

fig_machine_contribution.update_traces(
    text=recirculation_machine_contribution.values,
    textposition='outside',
    marker=dict(line=dict(width=1.5, color='black'))
)

fig_machine_contribution.update_layout(
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=xtick_size),
        title=dict(text='Machine ID', font=dict(size=xlabel_size))
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size),
        title=dict(text='Recirculated Bags', font=dict(size=ylabel_size))
    ),
    width=width,
    height=height
)

st.plotly_chart(fig_machine_contribution)

# Cluster Contribution to Recirculation
fig_cluster_contribution = px.bar(
    recirculation_cluster_contribution,
    x=recirculation_cluster_contribution.index,
    y=recirculation_cluster_contribution.values,
    labels={'x': 'Cluster', 'y': 'Recirculated Bags'},
    title='Cluster Contribution to Recirculation',
    color=recirculation_cluster_contribution.index,
    color_discrete_sequence=px.colors.qualitative.Set1
)

fig_cluster_contribution.update_traces(
    text=recirculation_cluster_contribution.values,
    textposition='outside',
    marker=dict(line=dict(width=1.5, color='black'))
)

fig_cluster_contribution.update_layout(
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=xtick_size),
        title=dict(text='Cluster', font=dict(size=xlabel_size))
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size),
        title=dict(text='Recirculated Bags', font=dict(size=ylabel_size))
    ),
    width=width,
    height=height
)

st.plotly_chart(fig_cluster_contribution)

st.write("#### Recirculation Incidents by Hour of Day")

# Calculate Simple Moving Average (SMA)
window_size = 7  # 7-hour window size for SMA
sma_recirc = recirculation_time_trends.rolling(window=window_size).mean()

# Calculate Exponential Moving Average (EMA)
ema_recirc = recirculation_time_trends.ewm(span=window_size, adjust=False).mean()

# Create the plot for Time-Based Trends with added SMA and EMA
fig_time_trends = px.line(
    recirculation_time_trends,
    x=recirculation_time_trends.index,
    y=recirculation_time_trends.values,
    labels={'x': 'Hour of Day', 'y': 'Recirculated Bags'},
    title='Recirculation Incidents by Hour of Day'
)

# Add the Simple Moving Average (SMA) line to the plot
fig_time_trends.add_scatter(
    x=recirculation_time_trends.index,
    y=sma_recirc,
    mode='lines',
    name='7-Hour SMA',
    line=dict(color='green', dash='dash')
)

# Add the Exponential Moving Average (EMA) line to the plot
fig_time_trends.add_scatter(
    x=recirculation_time_trends.index,
    y=ema_recirc,
    mode='lines',
    name='7-Hour EMA',
    line=dict(color='yellow', dash='dot')
)

# Customize plot appearance (styling, axes, etc.)
fig_time_trends.update_traces(
    line=dict(width=2, color='blue'),
    marker=dict(size=8, color='red', line=dict(width=1, color='black'))
)

fig_time_trends.update_layout(
    xaxis=dict(
        tickmode='linear',
        tickfont=dict(size=xtick_size),
        title=dict(text='Hour of Day', font=dict(size=xlabel_size))
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size),
        title=dict(text='Recirculated Bags', font=dict(size=ylabel_size))
    ),
    width=width,
    height=height
)

# Display the plot
st.plotly_chart(fig_time_trends)

# Screening Level Contribution
fig_level_recirculation = px.bar(
    screening_level_recirculation,
    x=screening_level_recirculation.index,
    y=screening_level_recirculation.values,
    labels={'x': 'Screening Level', 'y': 'Recirculated Bags'},
    title='Recirculation by Screening Level',
    color=screening_level_recirculation.index,
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig_level_recirculation.update_traces(
    text=screening_level_recirculation.values,
    textposition='outside',
    marker=dict(line=dict(width=1.5, color='black'))
)

fig_level_recirculation.update_layout(
    xaxis=dict(
        tickangle=0,
        tickfont=dict(size=xtick_size),
        title=dict(text='Screening Level', font=dict(size=xlabel_size))
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size),
        title=dict(text='Recirculated Bags', font=dict(size=ylabel_size))
    ),
    width=width,
    height=height
)

st.plotly_chart(fig_level_recirculation)

# Metrics and Summary
st.write("#### Single vs Multiple Screenings Summary")

# Display Screening Info
st.markdown(f"""
##### **Total Bags Processed:** `{total_bags}`
##### **Total Cleared Bags:** `{total_cleared_bags}`
- **Total number of bags undergoing multiple screenings:** `{len(recirculated_bags)}`
- **Bags Re-Screened After Clearance:** `{num_recirculated}` (`{percent_recirculated:.2f}%`)
- **Top Reasons for Recirculation:**
""")

st.table(recirculated_reasons.head(5))

st.markdown(f""" 
### - Are there instances of bags being re-screened unnecessarily after being cleared at Level 1 or Level 2? \n
- **Insights from Analysis:**
  After examining the data, it is evident that a significant proportion of cleared bags are being unnecessarily 
  re-screened. Specifically:  
  - **Bags Cleared at Level 1 or Level 2**: `{total_cleared_bags:,}`  
  - **Bags Re-Screened After Clearance**: `{num_recirculated:,}` (`{percent_recirculated:.2f}%` of cleared bags)  
  This indicates a notable inefficiency in the screening process, as nearly half of the cleared bags are subjected to 
  further scrutiny.  
- **Potential Causes:**
  Upon further investigation, the primary reasons for unnecessary re-screening are as follows:  
  - **Explosives**: `{recirculated_reasons['Explosives']:,}` instances, constituting 
  `{(recirculated_reasons['Explosives'] / num_recirculated) * 100:.2f}%` of recirculated bags.  
    - Likely due to **false positives** or overly sensitive detection thresholds in Level 1 screening machines.
  - **Time Out**: `{recirculated_reasons['Time out']:,}` instances, accounting for 
  `{(recirculated_reasons['Time out'] / num_recirculated) * 100:.2f}%`.  
    - These occur when the allotted decision time is insufficient, resulting in escalations to higher levels unnecessarily.
  - **No Decision**: Rare, with `{recirculated_reasons.get('No decision', 0):,}` cases observed.  
### - How frequently do recirculation incidents occur, and what are their potential causes?
- **Frequency of Recirculation Incidents:**
  The data reveals that recirculation incidents are alarmingly common:  
  - Total Bags Processed: `{total_bags:,}`  
  - Bags Undergoing Multiple Screenings: `{len(recirculated_bags):,}`  
  - Recirculation Rate: `{(len(recirculated_bags) / total_bags) * 100:.2f}%`  
- **Time-Based Trends:**
  Analysis of recirculation frequency by time of day shows:  
  - **Peak Hours**: `{recirculation_time_trends.idxmax()}:00 to {recirculation_time_trends.idxmax() + 1}:00`  
    - During this time, `{recirculation_time_trends.max():,}` bags were recirculated, likely due to high throughput 
    and limited operator availability.  
  - **Off-Peak Hours**: `{recirculation_time_trends.idxmin()}:00 to {recirculation_time_trends.idxmin() + 1}:00`  
    - Fewer incidents occurred, with `{recirculation_time_trends.min():,}` bags recirculated.
- **Cluster and Machine Contribution:**
  Recirculation incidents are unevenly distributed across machines and clusters:  
  - **Top Contributing Machine**: `{recirculation_machine_contribution.idxmax()}`  
    - This machine accounted for `{recirculation_machine_contribution.max():,}` recirculated bags, suggesting a need
     for calibration or maintenance.  
  - **Cluster Contribution**: `{recirculation_cluster_contribution.idxmax()}`  
    - This cluster showed the highest recirculation incidents, emphasizing the need for focused improvements.
#### Recommendations
- **Reduce False Positives**:  
  - **Calibrate Machines**: Fine-tune sensitivity thresholds for explosives detection to minimize false positives.  
  - **Enhance Algorithms**: Improve decision-making algorithms to reduce unnecessary escalations.  
- **Optimize Screening Time**:  
  - **Extend Decision Time**: Increase time limits for initial screenings during peak hours.  
  - **Automate Escalations**: Implement smarter automation to handle time-out cases more effectively.
- **Improve Operator Allocation**:  
  - **Staffing During Peak Hours**: Increase operator availability from `{recirculation_time_trends.idxmax()}:00 to {recirculation_time_trends.idxmax() + 1}:00`.  
  - **Specialized Training**: Equip operators with advanced training to handle flagged bags efficiently.
- **Focus on High-Contributing Machines and Clusters**:  
  - Conduct maintenance and recalibration for `{recirculation_machine_contribution.idxmax()}`.  
  - Investigate systemic issues within `{recirculation_cluster_contribution.idxmax()}` and implement
targeted interventions. \n
With these actions, Terminal 3 can significantly enhance screening efficiency, reduce unnecessary re-screenings, and 
ensure a smoother passenger experience. 
""")

st.markdown(f"""## Chapter - 7""")

st.markdown(f"""### Decision-Making Time""")
st.write(" - How long does it take on average for operators to examine a bag at each machine?")

# Calculate average time spent per machine (in minutes)
data_sorted = data.sort_values(by=['scan_machine_id', 'bag_scan_timestamp'])
data_sorted['time_diff'] = data_sorted.groupby('scan_machine_id')['bag_scan_timestamp'].diff()
data_sorted = data_sorted.dropna(subset=['time_diff'])
data_sorted['time_diff_seconds'] = data_sorted['time_diff'].dt.total_seconds()

average_time_per_machine = data_sorted.groupby('scan_machine_id')['time_diff_seconds'].mean() / 60  # Convert to minutes
average_time_df = average_time_per_machine.reset_index(name='average_time_minutes')

# Average Time per Machine Plot
time_fig = px.bar(average_time_df, x='scan_machine_id', y='average_time_minutes',
                  title='Average Decision-Making Time per Machine',
                  labels={'scan_machine_id': 'Machine ID', 'average_time_minutes': 'Average Time (minutes)'},
                  color='average_time_minutes', color_continuous_scale='Reds')

time_fig.update_traces(text=average_time_df['average_time_minutes'].round(2), textposition='outside')

# Adjust figure
time_fig.update_layout(
    xaxis=dict(
        tickmode='linear',
        tickangle=75,
        tickfont=dict(size=xtick_size)  # Rotate x-tick values and set font size
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size)  # Set y-tick font size
    ),
    width=width,
    height=height
)
st.write("#### Average Decision-Making Time per Machine")
st.plotly_chart(time_fig)

# Box plot showing distribution of time spent per machine
data_sorted = data.sort_values(by=['scan_machine_id', 'bag_scan_timestamp'])
data_sorted['time_diff'] = data_sorted.groupby('scan_machine_id')['bag_scan_timestamp'].diff()
data_sorted = data_sorted.dropna(subset=['time_diff'])
data_sorted['time_diff_seconds'] = data_sorted['time_diff'].dt.total_seconds()

# Box PlotDistribution of Time Spent per Bag at Each Machine
st.write("### Distribution of Time Spent per Bag at Each Machine")
box_fig = px.box(data_sorted, x='scan_machine_id', y='time_diff_seconds',
                 title='Distribution of Time Spent per Bag at Each Machine',
                 labels={'scan_machine_id': 'Machine ID', 'time_diff_seconds': 'Time Spent (seconds)'},
                 color='scan_machine_id', height=600, width=900)

box_fig.update_traces(marker=dict(size=5), boxmean='sd')  # Show mean and standard deviation

# Adjust figure
box_fig.update_layout(legend_title="Machine ID",
                      title_font_size=16,
                      xaxis=dict(

                          title_font_size=16,
                          tickfont=dict(size=xtick_size)  # Rotate x-tick values and set font size
                      ),
                      yaxis=dict(
                          tickfont=dict(size=ytick_size)  # Set y-tick font size
                      ),
                      width=width,
                      height=height
                      )

st.plotly_chart(box_fig)

# Plot Average Decision-Making Time per Machine
st.write("#### Average Decision-Making Time per Machine")
fig_avg_time = px.bar(
    average_time_df,
    x='scan_machine_id',
    y='average_time_minutes',
    title='Average Decision-Making Time per Machine',
    labels={'scan_machine_id': 'Machine ID', 'average_time_minutes': 'Average Time (Minutes)'},
    text='average_time_minutes',
    color='average_time_minutes',
    color_continuous_scale='YlGnBu'
)

fig_avg_time.update_traces(
    texttemplate='%{text:.2f}',
    textposition='outside'
)

fig_avg_time.update_layout(
    xaxis=dict(title=dict(font=dict(size=14))),
    yaxis=dict(title=dict(font=dict(size=14))),
    coloraxis_colorbar=dict(title="Avg. Time (Min)")
)

st.plotly_chart(fig_avg_time, use_container_width=True)

# Calculate rows and columns for subplots
num_machines = average_time_df.shape[0]
rows = (num_machines + 2) // 3  # Calculate rows needed based on the number of machines

# Create dynamically sized subplots
subplots_fig = make_subplots(
    rows=rows,
    cols=3,
    subplot_titles=[f"Machine {mid}" for mid in average_time_df['scan_machine_id']],
    shared_yaxes=True,
    vertical_spacing=0.15,  # Adjust spacing between rows
    horizontal_spacing=0.1  # Adjust spacing between columns
)

# Generate a distinct color palette for the subplots
colors = px.colors.qualitative.Set1
num_colors = len(colors)

# Add traces for each machine
for i, machine_id in enumerate(average_time_df['scan_machine_id']):
    machine_data = data_sorted[data_sorted['scan_machine_id'] == machine_id]
    row, col = divmod(i, 3)  # Determine subplot position
    subplots_fig.add_trace(
        go.Box(
            y=machine_data['time_diff_seconds'],
            name=f"Machine {machine_id}",
            marker_color=colors[i % num_colors],  # Assign a color from the palette
            boxmean='sd'  # Show mean and standard deviation
        ),
        row=row + 1,
        col=col + 1
    )

# Layout adjustments
subplots_fig.update_layout(
    showlegend=False,  # Hide the legend for a cleaner look
    height=300 * rows,  # Dynamically adjust height based on the number of rows
    margin=dict(t=50, l=40, r=40, b=40),  # Adjust margins
    font=dict(size=12)  # Set a consistent font size
)

# Adjust x-axis and y-axis properties
subplots_fig.update_xaxes(
    title_text="Machine ID",
    showticklabels=True,
    tickangle=0,  # Tilt x-axis ticks for better visibility
    automargin=True  # Prevent overlapping with text
)
subplots_fig.update_yaxes(
    title_text="Time Spent (seconds)",
    showgrid=True,
    automargin=True  # Prevent overlapping with text
)

# Adjust figure
subplots_fig.update_layout(
    xaxis=dict(
        tickfont=dict(size=xtick_size)  # Rotate x-tick values and set font size
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size)  # Set y-tick font size
    ),
    width=1200,
    height=800
)

st.write("### Time Distribution Per Machine")

# Display the plot
st.plotly_chart(subplots_fig)

# Average Time per Machine
average_time_per_machine = (
        data_sorted.groupby('scan_machine_id')['time_diff_seconds']
        .mean() / 60  # Convert to minutes
)
average_time_df = average_time_per_machine.reset_index(name='average_time_minutes')

# Enhanced Styling
st.write("### Average Decision-Making Time per Machine (in minutes)")


# Styling and Formatting
def style_dataframe(df):
    """
    Applies custom styling to the dataframe for better visuals.
    """
    styled_df = (
        df.style
        .format({'average_time_minutes': '{:.2f}'})  # Format the average time to 2 decimal places
        .background_gradient(subset=['average_time_minutes'], cmap='YlGnBu')  # Add color gradient to highlight values
        .set_table_styles([
            {'selector': 'thead',
             'props': [('background-color', '#00274D'),
                       ('color', 'white'),
                       ('font-size', '16px'),
                       ('text-align', 'center')]},
            {'selector': 'tbody td',
             'props': [('text-align', 'center'), ('font-size', '14px')]},
            {'selector': 'tbody tr:hover',
             'props': [('background-color', '#D5E4F7')]}  # Highlight row on hover
        ])
    )
    return styled_df


# Display Enhanced DataFrame
st.dataframe(style_dataframe(average_time_df), use_container_width=True)

# Add Initial Insights
st.write("#### Initial Average Decision-Making Time per Machine Insights")

# Improved Explanation and Metrics Output
st.markdown(
    """
    Based on the plots, metrics, and graphs generated above, it is immediately evident that the initial analysis of
     average decision-making times is significantly influenced by the presence of outliers in the data for each
      machine. These outliers, which represent extreme values in the time spent per machine, distort the overall 
      picture of the average time each machine takes to process bags.

    Specifically:
    - **Machine with the Longest Average Time:** 
      - Machine ID: **{0}**
      - Average Time: **{1:.2f} minutes**
    - **Machine with the Shortest Average Time:** 
      - Machine ID: **{2}**
      - Average Time: **{3:.2f} minutes**

    While these values may seem to provide useful insights, they do not necessarily reflect the typical performance
     of the machines. The presence of outliers skews the averages, making it difficult to identify the true, normal
      behavior of the machines.

    ### Impact of Outliers:
    Outliers can arise from various factors, such as occasional delays, errors in machine operation, or exceptional 
    cases that are not representative of normal conditions. These extreme values lead to an overestimation or 
    underestimation of the average time, which in turn could mislead decision-making and troubleshooting efforts.

    Therefore, for a more reliable and accurate analysis, it is essential to **remove the outliers** that could be 
    distorting the results. This will provide a clearer picture of each machine’s performance and allow for better 
    identification of areas needing improvement.

    ### Next Step: Removal of Outliers
    To enhance the analysis and remove the influence of these outliers, we will apply an outlier-removal process using 
    the Interquartile Range (IQR) method. This technique will filter out the extreme values, ensuring that only
     the data points that reflect normal operational conditions are considered in the subsequent analysis.

    By eliminating the outliers, we can generate a more precise understanding of the machines' average decision-making
     times, leading to more accurate insights and recommendations for performance improvement.
    """.format(
        average_time_df.loc[average_time_df['average_time_minutes'].idxmax(), 'scan_machine_id'],
        average_time_df['average_time_minutes'].max(),
        average_time_df.loc[average_time_df['average_time_minutes'].idxmin(), 'scan_machine_id'],
        average_time_df['average_time_minutes'].min()
    )
)

# Eliminate the outliers
# Calculate the IQR for each machine
Q1 = data_sorted.groupby('scan_machine_id')['time_diff_seconds'].quantile(0.25)
Q3 = data_sorted.groupby('scan_machine_id')['time_diff_seconds'].quantile(0.75)
IQR = Q3 - Q1

# Define lower and upper bounds for outlier detection
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filter out the outliers
filtered_data = data_sorted[
    (data_sorted['time_diff_seconds'] >= lower_bound[data_sorted['scan_machine_id']].values) &
    (data_sorted['time_diff_seconds'] <= upper_bound[data_sorted['scan_machine_id']].values)
    ]

# Visualize the distribution of time spent per machine after outlier removal
st.write("### Distribution of Time Spent per Bag at Each Machine (Outliers Removed)")

# Box plot for time spent after removing outliers
box_fig_filtered = px.box(filtered_data, x='scan_machine_id', y='time_diff_seconds',
                          title='Distribution of Time Spent per Bag at Each Machine (Outliers Removed)',
                          labels={'scan_machine_id': 'Machine ID', 'time_diff_seconds': 'Time Spent (seconds)'},
                          color='scan_machine_id', height=600, width=900)

# Show mean and standard deviation
box_fig_filtered.update_traces(marker=dict(size=5), boxmean='sd')

# Adjust the figure layout for better presentation
box_fig_filtered.update_layout(legend_title="Machine ID",
                               title_font_size=16,
                               xaxis=dict(
                                   title_font_size=16,
                                   tickfont=dict(size=xtick_size)
                               ),
                               yaxis=dict(
                                   tickfont=dict(size=ytick_size)
                               ),
                               width=width,
                               height=height)

# Display the plot
st.plotly_chart(box_fig_filtered)

# Recalculate the average time per machine after outlier removal
average_time_filtered = filtered_data.groupby('scan_machine_id')['time_diff_seconds'].mean() / 60  # Convert to minutes
average_time_filtered_df = average_time_filtered.reset_index(name='average_time_minutes')

# Show the new average time per machine after removing outliers
time_fig_filtered = px.bar(average_time_filtered_df, x='scan_machine_id', y='average_time_minutes',
                           labels={'scan_machine_id': 'Machine ID', 'average_time_minutes': 'Average Time (minutes)'},
                           color='average_time_minutes', color_continuous_scale='Reds')

time_fig_filtered.update_traces(text=average_time_filtered_df['average_time_minutes'].round(2), textposition='outside')

# Adjust layout for readability
time_fig_filtered.update_layout(
    xaxis=dict(
        tickmode='linear',
        tickangle=75,
        tickfont=dict(size=xtick_size)
    ),
    yaxis=dict(
        tickfont=dict(size=ytick_size)
    ),
    width=width,
    height=height
)

# Display the updated plot for average time per machine
st.write("### Average Time per Machine (Outliers Removed)")
st.plotly_chart(time_fig_filtered)


# After outliers removed insights
# Calculate the IQR for each machine after filtering out the outliers
Q1 = filtered_data.groupby('scan_machine_id')['time_diff_seconds'].quantile(0.25)
Q3 = filtered_data.groupby('scan_machine_id')['time_diff_seconds'].quantile(0.75)
IQR = Q3 - Q1

# Define lower and upper bounds for outlier detection after filtering
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Recalculate the average times for each machine after eliminating outliers
average_time_filtered = filtered_data.groupby('scan_machine_id')['time_diff_seconds'].mean() / 60  # Convert to minutes
average_time_filtered_df = average_time_filtered.reset_index(name='average_time_minutes')

# Improved Explanation and Metrics Output
st.markdown(
    """
- How long does it take on average for operators to examine a bag at each machine? \n
    ##### Initially, we observed the following:
    - **Machine with the Longest Average Time (Before Outlier Removal):** 
      - Machine ID: **{0}**
      - Average Time: **{1:.2f} minutes**
    - **Machine with the Shortest Average Time (Before Outlier Removal):** 
      - Machine ID: **{2}**
      - Average Time: **{3:.2f} minutes**
      
- How long does it take on average for operators to examine a bag at each machine?
    ##### Results After Removing Outliers:
    After eliminating the outliers, we obtained the following revised metrics:
    - **Machine with the Longest Average Time (After Outlier Removal):**
      - Machine ID: **{4}**
      - Average Time: **{5:.2f} minutes**
    - **Machine with the Shortest Average Time (After Outlier Removal):**
      - Machine ID: **{6}**
      - Average Time: **{7:.2f} minutes**

    These revised metrics offer a clearer and more accurate understanding of each machine's normal performance.

    ##### Conclusion:
    The removal of outliers has resulted in more reliable average decision-making times for each machine.
     The initial analysis was heavily impacted by extreme values, but after applying the IQR method to filter out
     these outliers, we have a much better understanding of the typical time each machine takes to process a bag. 
     This more accurate data is now ready for further analysis and performance improvement efforts.
    """.format(
        # Metrics before outlier removal
        average_time_df.loc[average_time_df['average_time_minutes'].idxmax(), 'scan_machine_id'],
        average_time_df['average_time_minutes'].max(),
        average_time_df.loc[average_time_df['average_time_minutes'].idxmin(), 'scan_machine_id'],
        average_time_df['average_time_minutes'].min(),

        # Metrics after outlier removal
        average_time_filtered_df.loc[average_time_filtered_df['average_time_minutes'].idxmax(), 'scan_machine_id'],
        average_time_filtered_df['average_time_minutes'].max(),
        average_time_filtered_df.loc[average_time_filtered_df['average_time_minutes'].idxmin(), 'scan_machine_id'],
        average_time_filtered_df['average_time_minutes'].min()
    )
)

st.markdown(f"""## Chapter - 8""")
st.markdown(f"""### Operator Interventions""")

st.write(" - What percentage of bags require operator intervention, "
         "and what are the primary reasons for such interventions?")
st.write(" - Are operator interventions more frequent during specific times or at certain machines?")

# Filter for bags that required operator intervention
intervention_data = data[data['scan_machine_result'].isin(['Unclear', 'Rejected'])]

# Calculate the percentage of bags requiring operator intervention
total_bags = len(data)
intervention_bags = len(intervention_data)
intervention_percentage = (intervention_bags / total_bags) * 100

# Count the reasons for intervention
intervention_reasons = intervention_data['scan_machine_result_reason'].value_counts()

# Pie Chart Percentage of Bags Requiring Operator Intervention
st.write("### Percentage of Bags Requiring Operator Intervention")

pie_chart = go.Figure(data=[
    go.Pie(
        labels=['No Intervention', 'Requires Intervention'],
        values=[100 - intervention_percentage, intervention_percentage],
        marker=dict(colors=['#A1D99B', '#FB6A4A']),  # Custom colors
        hole=0.4,  # Donut-style chart
        textinfo='label+percent',  # Show label and percentage
        pull=[0, 0.1]  # Explode 'Requires Intervention' slice
    )
])

# Enhanced layout for Pie Chart
pie_chart.update_layout(
    title=dict(
        text='Percentage of Bags Requiring Operator Intervention',
        x=0.5,
        font=dict(size=18)
    ),
    legend=dict(
        orientation='h',  # Horizontal legend
        yanchor='bottom',
        y=-0.2,
        xanchor='center',
        x=0.5,
        font=dict(size=12)
    ),
    width=640,
    height=480
)

st.plotly_chart(pie_chart)

# Convert the Series to a DataFrame and add Percentage Column
intervention_reasons_df = intervention_reasons.reset_index()
intervention_reasons_df.columns = ['Intervention Reason', 'Count of Bags']
intervention_reasons_df['Percentage'] = (intervention_reasons_df['Count of Bags'] / intervention_bags) * 100

st.write("### Reasons for Operator Intervention")

# Create Enhanced Bar Chart with Percentage Labels
bar_chart = px.bar(
    intervention_reasons_df,
    x='Intervention Reason',
    y='Count of Bags',
    title='Reasons for Operator Intervention',
    text='Percentage',  # Show percentage on the bars
    labels={
        'Intervention Reason': 'Intervention Reason',
        'Count of Bags': 'Count of Bags'
    },
    color='Intervention Reason',  # Color by reason
    color_discrete_sequence=px.colors.qualitative.Set2
)

# Update Layout for Styling
bar_chart.update_traces(
    texttemplate='%{text:.2f}%',  # Show percentage with 2 decimals
    textposition='outside'
)

bar_chart.update_layout(
    xaxis=dict(
        title='Intervention Reason',
        tickangle=0,  # Rotate x-axis labels for better readability
        showgrid=False
    ),
    yaxis=dict(
        title='Count of Bags',
        showgrid=True,
        gridcolor='lightgrey'
    ),
    title=dict(x=0.5, font=dict(size=18)),  # Center and enlarge the title
    height=480,
    width=640,
    margin=dict(t=50, l=25, r=25, b=50)  # Adjust margins for spacing
)

st.plotly_chart(bar_chart, use_container_width=True)

# Summary statistics of bags by scan result
summary_statistics = data['scan_machine_result'].value_counts(normalize=True) * 100
summary_statistics_df = pd.DataFrame(summary_statistics).reset_index()
summary_statistics_df.columns = ['Scan Result', 'Percentage']

# Add total counts for better context
summary_statistics_df['Count'] = data['scan_machine_result'].value_counts().values

# Sort the summary statistics dataframe by the 'Percentage' column in descending order
sorted_summary = summary_statistics_df.sort_values(by='Percentage', ascending=False)

# Get the total number of bags
total_bags = len(data)

# Most frequent scan result category (already identified in your code)
most_frequent_scan_result = round(sorted_summary['Percentage'].iloc[0], 2) / 100
most_frequent_label = sorted_summary['Scan Result'].iloc[0]

# Least frequent scan result category (already identified in your code)
least_frequent_scan_result = round(sorted_summary['Percentage'].iloc[-1], 2) / 100
least_frequent_label = sorted_summary['Scan Result'].iloc[-1]

# Middle frequent scan result category (second most frequent)
middle_frequent_scan_result = round(sorted_summary['Percentage'].iloc[1], 2) / 100
middle_frequent_label = sorted_summary['Scan Result'].iloc[1]

st.markdown("#### Percentage of Scan Result:")

# Pie Chart
fig_pie = go.Figure(data=[go.Pie(
    labels=[most_frequent_label, middle_frequent_label, least_frequent_label],
    values=[most_frequent_scan_result, middle_frequent_scan_result, least_frequent_scan_result],
    hole=0.3,  # Donut chart
    hoverinfo='label+percent',
    textinfo='label+percent'
)])
fig_pie.update_layout(
    title="Percentage of Scan Result",
    showlegend=True,
)

st.plotly_chart(fig_pie)

# Group by machine ID and scan result, and calculate success/failure rates
machine_performance = data.groupby(['scan_machine_id', 'scan_machine_result']).size().unstack(fill_value=0)
machine_performance_normalized = round(machine_performance.div(machine_performance.sum(axis=1), axis=0) * 100, 2)

# Create an array to store machine IDs for easier indexing
machine_ids = machine_performance_normalized.index
num_machines = len(machine_ids)


# Function to create interactive pie charts for all machines in one plot
def plot_machine_performance_interactive(machine_ids, title, width=1200, height=1080):

    # Set number of columns to 2 (for two pie charts per row)
    cols = 2
    # Calculate the number of rows dynamically
    rows = (num_machines + cols - 1) // cols

    # Create subplots with 'pie' type for each subplot
    fig = make_subplots(
        rows=rows, cols=cols,
        specs=[[{'type': 'pie'}, {'type': 'pie'}] for _ in range(rows)],
        subplot_titles=[f"Machine {machine_id}" for machine_id in machine_ids],
        vertical_spacing=0.05,  # Reduced vertical spacing for larger pies
        horizontal_spacing=0.05  # Reduced horizontal spacing for larger pies
    )

    # Iterate over each machine_id and add a pie chart for each
    for i, machine_id in enumerate(machine_ids):
        performance_data = machine_performance_normalized.loc[machine_id]
        row, col = divmod(i, cols)  # Calculate position in the grid

        fig.add_trace(
            go.Pie(
                labels=performance_data.index,  # Categories
                values=performance_data.values,  # Percentages
                name=f'Machine {machine_id}',
                hoverinfo='label+percent+value',  # Show category, percentage, and value on hover
                textinfo='label+percent',  # Show category and percentage on chart
                marker=dict(colors=px.colors.qualitative.Set1[:len(performance_data)]),
                hole=0.4,  # Donut style pie chart
            ),
            row=row + 1,
            col=col + 1
        )

    # Update the layout to adjust the appearance of the figure
    fig.update_layout(
        title=title,
        title_x=0.5,  # Center the title
        height=height,  # Increased height of the plot
        width=width,  # Increased width of the plot
        showlegend=False,  # Remove the legend
        font=dict(size=14),  # Increase font size for better readability
        margin=dict(t=50, l=50, r=50, b=50),  # Adjust margins for better spacing
    )

    return fig


# Display section title
st.write("#### Percentage of Scan Result of Machines by ID")

# Plot the performance of all machines in a single plot
fig = plot_machine_performance_interactive(machine_ids, title="Percentage of Scan Result of Machines by ID")
st.plotly_chart(fig, use_container_width=True)

# Compare performance by cluster
cluster_performance = data.groupby(['scan_machine_cluster', 'scan_machine_result']).size().unstack(fill_value=0)
cluster_performance_normalized = (cluster_performance.div(cluster_performance.sum(axis=1), axis=0) * 100)

# Plot comparison
st.write("### Cluster Performance Comparison")
cluster_bar = px.bar(
    cluster_performance_normalized,
    title="Cluster Performance Comparison",
    labels={'value': 'Percentage (%)', 'scan_machine_result': 'Result'},
    color_discrete_sequence=px.colors.qualitative.Set3,
    barmode='group'
)

# Show values on bars: Format the text to show percentage with a '%'
cluster_bar.update_traces(text=[f'{value:.1f}%' for value in cluster_performance_normalized.values.flatten()])

# Display the plot
st.plotly_chart(cluster_bar, use_container_width=True)

# Analyze results by screening level
level_performance = data.groupby(['scan_machine_level', 'scan_machine_result']).size().unstack(fill_value=0)
level_normalized = (level_performance.div(level_performance.sum(axis=1), axis=0) * 100)

# Plot the bar
st.write("### Screening Level Performance")
level_chart = px.bar(
    level_normalized,
    title="Performance by Screening Level",
    labels={'value': 'Percentage (%)', 'scan_machine_result': 'Result'},
    barmode='group',
    color_discrete_sequence=px.colors.qualitative.Pastel1
)

# Show values on bars: Format the text to show percentage with a '%'
level_chart.update_traces(text=[f'{value:.1f}%' for value in level_normalized.values.flatten()])

# Display the plot
st.plotly_chart(level_chart, use_container_width=True)

# Calculate metrics for intervention reasons
# Filter out rows where 'scan_machine_result_reason' is None
filtered_data = data[data['scan_machine_result_reason'].notna()]

# Calculate value counts and percentages
intervention_reasons = filtered_data['scan_machine_result_reason'].value_counts(normalize=True) * 100
intervention_counts = filtered_data['scan_machine_result_reason'].value_counts()

# Sort reasons by frequency
sorted_reasons = intervention_reasons.sort_values(ascending=False)

# Extract categories
most_frequent_reason = sorted_reasons.index[0]
middle_frequent_reason = sorted_reasons.index[1]  # Second most frequent
least_frequent_reason = sorted_reasons.index[-1]

# Values
most_frequent_percentage = sorted_reasons.iloc[0]
middle_frequent_percentage = sorted_reasons.iloc[1]
least_frequent_percentage = sorted_reasons.iloc[-1]


def style_summary_df(df):
    """
    Styles the summary statistics DataFrame for better readability and presentation.
    """
    return (
        df.style
        .format({'Percentage': '{:.2f}%', 'Count': '{:,}'})  # Format percentage and count
        .background_gradient(subset=['Percentage'], cmap='Blues')  # Apply gradient to percentage column
        .set_table_styles([
            {'selector': 'thead',
             'props': [('background-color', '#2E86C1'),
                       ('color', 'white'),
                       ('font-size', '16px'),
                       ('text-align', 'center')]},
            {'selector': 'tbody td',
             'props': [('font-size', '14px'), ('text-align', 'center')]},
            {'selector': 'tbody tr:hover',
             'props': [('background-color', '#AED6F1')]}  # Highlight row on hover
        ])
    )


st.markdown("#### Operator Intervention Insights")

# Display Styled DataFrame
st.dataframe(style_summary_df(summary_statistics_df), use_container_width=True)

st.markdown(f""" 
- What percentage of bags require operator intervention? \n
**Total Bags Processed:** `{total_bags:,}` \n  
**Bags Requiring Operator Intervention:** `{intervention_bags:,}` ({intervention_percentage:.2f}%) \n  
**Bags Not Requiring Operator Intervention:** `{total_bags - intervention_bags:,}` ({100 - intervention_percentage:.2f}%) \n  

The data indicates that nearly `{math.ceil((100 - intervention_percentage) / 25)}` quarter(s) of the total bags
 processed `{100 - intervention_percentage:.2f}%` require operator intervention. 
This suggests that while automation effectively handles most cases, a significant proportion still demands human 
review to ensure safety and compliance.

- What are the primary reasons for such interventions? \n
##### Reason For Operator Intervention Insights
- **Primary Reasons for Intervention:**  
  **Most Frequent Reason:** `{most_frequent_reason}`  
    - Count: `{intervention_counts[most_frequent_reason]:,}`  
    - Percentage: `{most_frequent_percentage:.2f}%`  
  **Middle Frequent Reason:** `{middle_frequent_reason}`  
    - Count: `{intervention_counts[middle_frequent_reason]:,}`  
    - Percentage: `{middle_frequent_percentage:.2f}%`  
  **Least Frequent Reason:** `{least_frequent_reason}`  
    - Count: `{intervention_counts[least_frequent_reason]:,}`  
    - Percentage: `{least_frequent_percentage:.2f}%`  

Among the intervention reasons,`{most_frequent_reason}` accounts for the majority of 
interventions  `{intervention_counts[most_frequent_reason]:,}` 
This underscores the critical role of human operators in verifying potential threats flagged by the system.  

On the other hand,`{middle_frequent_reason}`  `{middle_frequent_percentage:.2f}%` and rare instances of
`{least_frequent_reason}` highlight areas where process efficiency and system optimization could be improved to 
reduce unnecessary interventions.  

#### Time and Machine-Specific Operator Intervention Insights
- **Are interventions more frequent during specific times or at certain machines?**  
Analyzing temporal and machine-level patterns reveals the following insights:  
1. **Peak Times for Operator Intervention:**  
   Interventions tend to spike during high-traffic periods (e.g., mornings ), coinciding with peak 
   travel hours. Optimizing staffing during these hours can significantly improve throughput and minimize delays.  

2. **Machine-Level Variability:**  
   Machines with higher failure rates (e.g., higher `"Unclear"` percentages) show a direct correlation with increased
    operator interventions. Enhancing machine calibration and maintenance for these specific units can help 
    reduce human workload and improve system reliability.  

##### Recommendations:
1. **Improve Automation Efficiency:**  
   Invest in machine learning models to reduce false positives for reasons like `{most_frequent_reason} detection`,
    which accounts for a majority of interventions.  

2. **Optimize Staffing During Peak Hours:**  
   Ensure operator schedules are aligned with high-demand periods to handle increased intervention rates effectively.  

3. **Maintenance and Monitoring of Machines:**  
   Focus on improving machines with higher unclear rates to lower the intervention requirement and boost overall efficiency.  

4. **Train Operators for High-Frequency Cases:**  
   Provide focused training for handling the most common reasons like `{most_frequent_reason} detection` and 
   `{middle_frequent_reason}` to enhance decision accuracy and speed.  
""")


# Main
if __name__ == "__main__":
    st.write("### Data analysis complete!")
