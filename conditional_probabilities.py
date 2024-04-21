import pandas as pd
from collections import defaultdict


def calculate_conditional_probabilities(weather_data, road_data, light_data):
    """
    Calculates the frequency of bicycle-related incidents under different weather, road, and light conditions.
    Arguments:
    - weather_data: List of weather conditions for each cycling incident.
    - road_data: List of road conditions for each cycling incident.
    - light_data: List of light conditions for each cycling incident.
    """

    def print_probabilities(data, condition_type):
        count_dict = defaultdict(int)
        for condition in data:
            count_dict[condition] += 1
        total_incidents = len(data)
        print(f"Frequency of Bicycle Incidents by {condition_type} Conditions:")
        for condition, count in count_dict.items():
            if count > 0:
                frequency = count / total_incidents
                print(
                    f"Incident Frequency when {condition_type} is {condition} = {frequency:.4f}"
                )

    print_probabilities(weather_data, "Weather")
    print_probabilities(road_data, "Road")
    print_probabilities(light_data, "Light")


def load_and_prepare_data(filename):
    """
    Loads data from a CSV file, filters it for bicycle collisions, and prepares it for analysis.
    Outputs:
    - weather_data: List of weather conditions for filtered incidents.
    - road_data: List of road conditions for filtered incidents.
    - light_data: List of light conditions for filtered incidents.
    """
    df = pd.read_csv(filename)

    # Keep only data rows where collisions involve bicycles
    df = df[df["COLLISIONTYPE"].str.contains("Cycle", na=False)]

    weather_data = df["WEATHER"].tolist()
    road_data = df["ROADCOND"].tolist()
    light_data = df["LIGHTCOND"].tolist()

    return weather_data, road_data, light_data


def main():
    filename = "collisions.csv"  # Path to the CSV file containing collision data
    weather_data, road_data, light_data = load_and_prepare_data(filename)
    calculate_conditional_probabilities(weather_data, road_data, light_data)


main()
