import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load data from Wikipedia
url = "https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals"

# Read tables from Wikipedia
tables = pd.read_html(url)

# Identify the correct table by checking the number of columns
df = None
for table in tables:
    if len(table.columns) >= 5:  # Ensure at least Year, Winner, Runner-up, etc.
        df = table
        break

# If no valid table is found, raise an error
if df is None:
    raise ValueError("Could not find a suitable table on Wikipedia.")

# Rename columns dynamically based on actual table structure
df.columns = ['Year', 'Winners', 'Score', 'Runners-up', 'Venue', 'Location', 'Attendance', 'Ref']

# Select relevant columns
df = df[['Year', 'Winners', 'Runners-up']]

# Drop rows with missing values
df = df.dropna()

# Convert Year to string for visualization
df['Year'] = df['Year'].astype(str)

# Count the number of times each country has won
winners_count = df['Winners'].value_counts().reset_index()
winners_count.columns = ['Country', 'Total Wins']

# Create Dash app
app = dash.Dash(__name__)

# Simplified layout for testing
app.layout = html.Div([
    html.H1("FIFA World Cup Visualization Test", style={'textAlign': 'center'}),
    html.Div("This is a test message.")  # A simple message to verify the app is working
])

# Run app (Test version)
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=10000)

