import os
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load data (Ensure this CSV is present in your repository)
df = pd.read_csv("world_cup_data.csv")

# Convert Year to string for visualization
df['Year'] = df['Year'].astype(str)

# Count the number of times each country has won
winners_count = df['Winners'].value_counts().reset_index()
winners_count.columns = ['Country', 'Total Wins']

# Create Dash app
app = dash.Dash(__name__)
server = app.server  # Needed for Render deployment

app.layout = html.Div([
    html.H1("FIFA World Cup Winners Visualization", style={'textAlign': 'center'}),
    
    # World Map Visualization
    dcc.Graph(id="world_map"),

    # Country Selection Dropdown
    html.Label("Select a Country:", style={'fontSize': 18}),
    dcc.Dropdown(
        id="country-dropdown",
        options=[{'label': country, 'value': country} for country in winners_count['Country']],
        value='Brazil',  # Default selection
        clearable=False
    ),

    # Country Wins Bar Chart
    dcc.Graph(id="country_wins"),
    
    # Year Selection Dropdown
    html.Label("Select a Year:", style={'fontSize': 18}),
    dcc.Dropdown(
        id="year-dropdown",
        options=[{'label': year, 'value': year} for year in df['Year']],
        value=df['Year'].max(),  # Default to latest year
        clearable=False
    ),

    # Display Winner Information
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


# Run app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Uses environment variable for deployment
    app.run_server(debug=True, host="0.0.0.0", port=port)
