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

# Print table structure for debugging
print(df.head())

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

app.layout = html.Div([
    html.H1("FIFA World Cup Winners Visualization", style={'textAlign': 'center'}),
    
    dcc.Graph(id="world_map"),
    
    html.Label("Select a Country:", style={'fontSize': 18}),
    dcc.Dropdown(
        id="country-dropdown",
        options=[{'label': country, 'value': country} for country in winners_count['Country']],
        value='Brazil',  # Default selection
        clearable=False
    ),

    dcc.Graph(id="country_wins"),
    
    html.Label("Select a Year:", style={'fontSize': 18}),
    dcc.Dropdown(
        id="year-dropdown",
        options=[{'label': year, 'value': year} for year in df['Year']],
        value=df['Year'].max(),
        clearable=False
    ),

    html.Div(id="winner-info", style={'fontSize': 20, 'marginTop': 20, 'textAlign': 'center'})
])


# Callback to update the world map
@app.callback(
    Output("world_map", "figure"),
    Input("country-dropdown", "value")
)
def update_map(selected_country):
    fig = px.choropleth(
        winners_count,
        locations="Country",
        locationmode="country names",
        color="Total Wins",
        title="World Cup Wins by Country",
        color_continuous_scale="Blues"
    )
    return fig


# Callback to update country wins bar chart
@app.callback(
    Output("country_wins", "figure"),
    Input("country-dropdown", "value")
)
def update_country_wins(selected_country):
    country_data = winners_count[winners_count['Country'] == selected_country]
    fig = px.bar(
        country_data,
        x="Country",
        y="Total Wins",
        text="Total Wins",
        title=f"{selected_country} World Cup Wins",
        color="Total Wins",
        color_continuous_scale="Blues"
    )
    fig.update_traces(textposition="outside")
    return fig


# Callback to display winner and runner-up based on selected year
@app.callback(
    Output("winner-info", "children"),
    Input("year-dropdown", "value")
)
def update_winner_info(selected_year):
    row = df[df['Year'] == selected_year]
    if not row.empty:
        winner = row.iloc[0]['Winners']
        runner_up = row.iloc[0]['Runners-up']
        return f"In {selected_year}, {winner} won the FIFA World Cup, defeating {runner_up}."
    return "Data unavailable."


# Run app (Updated Fix)
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=10000)
