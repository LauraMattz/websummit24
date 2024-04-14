import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

# Function to fetch data
def fetch_data():
    base_url = 'https://rio.websummit.com/api/list/?slug=schedule&typename=DefaultTemplate_Custompage_FlexibleContent_ScheduleList'
    headers = {
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'Referer': 'https://rio.websummit.com/schedule/',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"'
    }
    all_items = []
    page = 1
    while True:
        response = requests.get(f"{base_url}&page={page}", headers=headers)
        if response.status_code != 200:
            st.error(f"Failed to fetch data: {response.status_code}")
            return None
        data = response.json()
        items = data['data']['listItems']
        if not items:
            break
        all_items.extend(items)
        page += 1
    return all_items

# Function to plot data
def plot_data(df):
    category_counts = df['Category'].value_counts().reset_index()
    category_counts.columns = ['Category', 'Number of Events']
    
    # Plotting with Seaborn
    plt.figure(figsize=(12, 8))
    ax = sns.barplot(x="Number of Events", y="Category", data=category_counts,
                     palette=sns.color_palette("husl", len(category_counts)))
    ax.set(xlabel="Number of Events", ylabel="Category", title="Number of Events per Category")
    for p in ax.patches:
        ax.annotate(f'{int(p.get_width())}', (p.get_x() + p.get_width(), p.get_y() + 0.5), va='center')
    st.pyplot(plt.gcf())
    plt.clf()

# Streamlit interface
st.title('Web Summit Event Analysis')
if st.button('Fetch Data'):
    items = fetch_data()
    if items is not None:
        df = pd.DataFrame(items)
        df = df[['date', 'title', 'location.name', 'schedule_track.name', 'description']]
        df.columns = ['Date', 'Event Title', 'Location', 'Category', 'Description']
        df['Location'] = df['Location'].apply(lambda x: x['name'] if isinstance(x, dict) else 'N/A')
        df['Category'] = df['Category'].apply(lambda x: x['name'] if isinstance(x, dict) else 'N/A')
        plot_data(df)

        # Display the data as a table
        st.write("Preview of Data:", df.head())
        st.table(df.head())  # You can also use st.dataframe(df) for a large dataset with a scrollbar
