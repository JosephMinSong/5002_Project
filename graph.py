import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import re

# Setup instructions and package requirements
# Install virtualenv if not already installed:
# pip install virtualenv
# Navigate to the project directory:
# cd path_to_project
# Create a virtual environment:
# virtualenv venv
# Activate the virtual environment:
# source venv/bin/activate (Linux/Mac)
# Install necessary packages:
# pip install dash pandas plotly
# Run this script:
# python graph.py
# To exit the virtual environment:
# deactivate

# Initialize a regular expression to identify cycling-related incidents
CYCLES_REGEX = re.compile(r"Cycles", re.IGNORECASE)


def is_cycle_incident(collision_type):
    """Check if the collision type indicates a cycling-related incident."""
    return bool(re.search(CYCLES_REGEX, str(collision_type)))


# Load the dataset and filter for cycling incidents
df = pd.read_csv("Collisions.csv", low_memory=False)
df = df[df["COLLISIONTYPE"].apply(is_cycle_incident)]


def classify_accident(row):
    """Classify each accident based on the severity of injuries."""
    if row["FATALITIES"] > 0:
        return "Fatalities"
    elif row["SERIOUSINJURIES"] > 0:
        return "Serious Injuries"
    else:
        return "Injuries"


df["Accident_Type"] = df.apply(classify_accident, axis=1)

# Dropdown menu options for weather, road, and lighting conditions
weather_values = [
    "Clear",
    "Overcast",
    "Unknown",
    "Raining",
    "Other",
    "Snow",
    "Sleet",
    "Blank",
    "Fog",
    "Sand",
    "Partly Cloudy",
]
road_values = [
    "Dry",
    "Ice",
    "Unknown",
    "Wet",
    "Standing Water",
    "Snow",
    "Other",
    "Sand",
    "Empty String",
]
light_values = [
    "Daylight",
    "Dark - Street Lights On",
    "Dusk",
    "Unknown",
    "Dawn",
    "Dark - Street Lights Off",
    "Dark - No Street Lights",
    "Other",
    "Empty String",
    "Dark - Unknown Lighting",
]

# Initialize the Dash application
app = dash.Dash(__name__)

# Layout of the web application
app.layout = html.Div(
    [
        html.H1("Traffic Accident Analysis Dashboard"),
        html.Div(
            [
                html.Label("Select Weather Condition:"),
                dcc.Dropdown(
                    id="weather-dropdown",
                    options=[{"label": i, "value": i} for i in weather_values],
                    value=weather_values[0],
                ),
                html.Label("Select Road Condition:"),
                dcc.Dropdown(
                    id="road-dropdown",
                    options=[{"label": i, "value": i} for i in road_values],
                    value=road_values[0],
                ),
                html.Label("Select Lighting Condition:"),
                dcc.Dropdown(
                    id="lighting-dropdown",
                    options=[{"label": i, "value": i} for i in light_values],
                    value=light_values[0],
                ),
            ],
            style={"margin": "20px"},
        ),
        dcc.Graph(id="accident-graph"),
    ],
    style={"width": "80%", "margin": "auto"},
)


# Callback to update the graph based on user inputs
@app.callback(
    Output("accident-graph", "figure"),
    [
        Input("weather-dropdown", "value"),
        Input("road-dropdown", "value"),
        Input("lighting-dropdown", "value"),
    ],
)
def update_graph(selected_weather, selected_road, selected_lighting):
    filtered_df = df[
        (df["WEATHER"] == selected_weather)
        & (df["ROADCOND"] == selected_road)
        & (df["LIGHTCOND"] == selected_lighting)
    ]
    if filtered_df.empty:
        # Return an empty plot with a message indicating no data available
        fig = go.Figure()
        fig.update_layout(
            title="No data available for selected conditions",
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        )
        return fig
    else:
        fig = px.histogram(
            filtered_df,
            x="Accident_Type",
            title="Accident Severity under Selected Conditions",
            text_auto=True,
        )
        fig.update_layout(
            xaxis_title="Accident Type", yaxis_title="Number of Accidents", bargap=0.2
        )
        return fig


app.run_server(debug=True)
