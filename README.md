# Web Summit Rio API Access and Data Visualization

This script facilitates fetching and visualizing the schedule data from the Web Summit Rio's API. It is designed to retrieve event data and display the distribution of events across various categories using a bar chart.

## Getting Started

Follow these instructions to get the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have Python installed on your machine. This project depends on the following Python libraries:
- `requests` for making API calls
- `seaborn` and `matplotlib` for data visualization

You can install all necessary libraries with the following command:

```bash
pip install requests seaborn matplotlib

## Script Overview
### API Request
- URL and Headers Setup: The script sets up the necessary URL and headers to interact with the Web Summit Rio's API.
- GET Request: Executes a GET request to the API and handles the response.
- Data Handling: Parses the JSON response and processes the data for visualization.

### Data Visualization
- Data Preparation: Assumes the presence of a DataFrame df containing a 'Category' column. Processes this data to count the number of events per category.
- Plotting: Uses seaborn and matplotlib to plot a bar chart with distinct colors for each category, enhancing the visual representation of the data.
