import streamlit as st
st.cache(suppress_st_warning=True)  # Clear cache with suppression
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
from urllib.error import URLError

# Define a function to fetch the data
#@st.cache(ttl=60*60*24)  # Cache for 1 day
def get_data(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        raise URLError(err)

# Function to extract and preprocess data from JSON for plotting
def prepare_data(json_data):
    # Assuming json_data is the JSON dictionary containing the schedule data
    # Adjust the field accesses according to the actual structure of your JSON data
    items = json_data['data']['listItems']
    df = pd.json_normalize(items)
    # Extracting the necessary fields, modify these lines to match your JSON structure
    df = df[['title', 'location.name', 'schedule_track.name']]
    df.columns = ['Event Title', 'Location', 'Category']
    return df

# Define the URL, headers
url = 'https://rio.websummit.com/api/list/?slug=schedule&typename=DefaultTemplate_Custompage_FlexibleContent_ScheduleList&page=1'
headers = {
  'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
  'Referer': 'https://rio.websummit.com/schedule/',
  'sec-ch-ua-mobile': '?0',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
  'sec-ch-ua-platform': '"Windows"'
}

# Streamlit application layout
st.title('Web Summit Event Visualization')

# Fetch and prepare data
try:
    json_data = get_data(url, headers)
    df = prepare_data(json_data)
except URLError as e:
    st.error(
        f"Error fetching data: {e}"
    )
    st.stop()

# Sidebar filters for Category
st.sidebar.header('Filter by Category')
categories = df['Category'].unique()
selected_categories = st.sidebar.multiselect('Categories', categories, default=categories)

# Apply filters to data
filtered_data = df[df['Category'].isin(selected_categories)]

# Function to create and plot a seaborn barplot
def create_plot(data, title, x_label, y_label):
    plt.figure(figsize=(10, 8))
    ax = sns.countplot(y=data[y_label], order=data[y_label].value_counts().index, palette='viridis')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    for p in ax.patches:
        ax.annotate(f'{p.get_width()}', (p.get_x() + p.get_width(), p.get_y() + 0.55*p.get_height()))
    return ax

# Plot and display Category distribution
st.header('Event Distribution by Category')
category_plot = create_plot(filtered_data, 'Number of Events by Category', 'Number of Events', 'Category')
st.pyplot(plt)

# Similarly, create plots for other fields like 'Location' if desired...
