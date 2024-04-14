import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from urllib.error import URLError

# Define a function to fetch the data
@st.cache(show_spinner=False, allow_output_mutation=True)
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
    # Create the figure with a specified height and width
    fig = px.bar(data, y=y_axis, x=x_axis, text=x_axis, title=title, orientation='h')
    # Update the layout of the figure to adjust the plot and font sizes
    fig.update_layout(
        height=600,  # or adjust to your preference
        width=800,  # or use `None` to auto-scale with the container width
        title=dict(x=0.5, xanchor='center', font=dict(size=20)),  # Center title and adjust font size
        xaxis=dict(titlefont=dict(size=18), tickfont=dict(size=12)),  # Adjust x-axis title and tick font sizes
        yaxis=dict(titlefont=dict(size=18), tickfont=dict(size=12), categoryorder='total ascending'),  # Adjust y-axis settings
    )
    # Add configuration for responsive sizing
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)
    return fig

# Use the full width of the container for the plot
st.plotly_chart(fig, use_container_width=True)

