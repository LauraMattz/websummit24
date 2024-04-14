import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from urllib.error import URLError

# Define a function to fetch the data
def get_data(url, headers):
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Will raise HTTPError for bad responses
    return response.json()

# Function to extract and preprocess data from JSON for plotting
def prepare_data(json_data):
    items = json_data['data']['listItems']
    df = pd.json_normalize(items)
    df = df[['title', 'location.name', 'schedule_track.name']]
    df.columns = ['Event Title', 'Location', 'Category']
    return df

# Define the URL and headers
url = 'https://rio.websummit.com/api/list/?slug=schedule&typename=DefaultTemplate_Custompage_FlexibleContent_ScheduleList&page=1'
headers = {
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'Referer': 'https://rio.websummit.com/schedule/',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"'
}

st.title('Web Summit Event Visualization')

try:
    json_data = get_data(url, headers)
    df = prepare_data(json_data)
except URLError as e:
    st.error(f"Error fetching data: {e}")
    st.stop()

st.sidebar.header('Filter by Category')
categories = df['Category'].unique()
selected_categories = st.sidebar.multiselect('Categories', categories, default=categories)
filtered_data = df[df['Category'].isin(selected_categories)]

# Plotting using Plotly
# Plotting using Plotly
def create_plotly_bar_chart(data, title, x_axis, y_axis):
    # Ensure the data is sorted based on the y-axis values for better visualization
    data = data.sort_values(by=y_axis, ascending=True)
    
    # Create the bar chart using Plotly Express
    fig = px.bar(
        data_frame=data,
        x=x_axis,
        y=y_axis,
        text=x_axis,
        title=title,
        orientation='h',  # 'h' for horizontal, 'v' for vertical
        height=600,  # Customizable height
        width=800,  # Customizable width
    )
    
    # Update layout for a cleaner look
    fig.update_layout(
        xaxis_title=x_axis,  # Set x-axis title
        yaxis_title=y_axis,  # Set y-axis title
        yaxis={'categoryorder':'total ascending'},
        title={'x':0.5, 'xanchor': 'center'},  # Center the plot title
        margin=dict(l=20, r=20, t=40, b=20),  # Adjust the margins (left, right, top, bottom)
    )
    
    # Update text font and size for readability
    fig.update_traces(
        texttemplate='%{text}',  # Use the x-axis values as text labels
        textposition='inside',  # Position the text labels inside the bars
        textfont_size=14,  # Customize the size of the text
    )
    
    # Return the Plotly figure object
    return fig

# Call the function and store the returned figure in a variable
fig = create_plotly_bar_chart(filtered_data, 'Number of Events by Category', 'Category', 'Event Title')

# Display the plot in the Streamlit app
st.plotly_chart(fig, use_container_width=True)

