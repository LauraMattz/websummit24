entosimport streamlit as st
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

st.title('Eventos Web Summit 2024✨')

try:
    json_data = get_data(url, headers)
    df = prepare_data(json_data)
except URLError as e:
    st.error(f"Error fetching data: {e}")
    st.stop()

st.sidebar.header('Filtrar por Categoria')
categories = df['Category'].unique()
selected_categories = st.sidebar.multiselect('Categories', categories, default=categories)
filtered_data = df[df['Category'].isin(selected_categories)]

# Plotting using Plotly
# Plotting using Plotly
def create_bar_chart(data, title, category):
    fig = px.bar(data, x=category, title=title)
    fig.update_layout(xaxis={'categoryorder':'total descending'}, yaxis=dict(title='Number of Events'))
    fig.update_traces(marker_color='lightskyblue', marker_line_color='black', marker_line_width=1.5)
    fig.update_xaxes(tickangle=45)
    return fig

# Main Streamlit app
st.title('Event Distribution Analysis')

try:
    # Fetch and prepare data
    json_data = get_data(url, headers)
    df = prepare_data(json_data)
    
    # Sidebar filters for Category, Topic, and Curated Track
    st.sidebar.header('Filter by Category')
    all_categories = df['Category'].unique()
    selected_category = st.sidebar.selectbox('Category', all_categories)

    st.sidebar.header('Filter by Topic')
    all_topics = df['Topic'].unique()
    selected_topic = st.sidebar.selectbox('Topic', all_topics)
    
    st.sidebar.header('Filter by Curated Track')
    all_curated_tracks = df['Curated Track'].unique()
    selected_curated_track = st.sidebar.selectbox('Curated Track', all_curated_tracks)
    
    # Filtering data
    filtered_data_by_category = df[df['Category'] == selected_category]
    filtered_data_by_topic = df[df['Topic'] == selected_topic]
    filtered_data_by_curated_track = df[df['Curated Track'] == selected_curated_track]
    
    # Creating plots
    fig_category = create_bar_chart(filtered_data_by_category, f'Events by {selected_category}', 'Category')
    st.plotly_chart(fig_category, use_container_width=True)
    
    fig_topic = create_bar_chart(filtered_data_by_topic, f'Events by {selected_topic}', 'Topic')
    st.plotly_chart(fig_topic, use_container_width=True)
    
    fig_curated_track = create_bar_chart(filtered_data_by_curated_track, f'Events by {selected_curated_track}', 'Curated Track')
    st.plotly_chart(fig_curated_track, use_container_width=True)

except URLError as e:
    st.error(f"Error fetching data: {e}")

