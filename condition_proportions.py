import sys
import numpy as np
from dataanalysis import DataAnalysis


class Proportions:
    def __init__(self, filename):
        self.filename = filename
        self.data_analyzer = None  # This will be set in load_data()

    def load_data(self):
        """Loads and processes the data from the file."""
        if self.data_analyzer is None:
            self.data_analyzer = DataAnalysis(self.filename)
            self.data_analyzer.analyze_data()

    def fatalities_proportion(self):
        """Reports the number of fatalities and incidents along with the proportion."""
        self.load_data()
        total_fatalities = self.data_analyzer.fatalities_count
        total_incidents = self.data_analyzer.cycle_inc_count
        proportion = total_fatalities / total_incidents
        print(f"The total number of fatalities: {total_fatalities}")
        print(f"Cycling incidents: {total_incidents}")
        print("Proportion:", proportion)

    def conditions_proportions(self, condition_values, condition_names, condition_type):
        """Method to report conditions such as weather, road, and lighting."""
        self.load_data()
        total_incidents = self.data_analyzer.cycle_inc_count
        counts = np.zeros(len(condition_names), dtype=int)

        for index in condition_values:
            if index < len(counts):
                counts[index] += 1

        print(f"\nCounts and Proportions for {condition_type} Conditions:")
        for name, count in zip(condition_names, counts):
            proportion = count / total_incidents if total_incidents else 0
            print(f"{name}: {count} ({proportion:.4f})")


filename = sys.argv[1]
proportions = Proportions(filename)
proportions.load_data()

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
    "Dark-Street Lights On",
    "Dusk",
    "Unknown",
    "Dawn",
    "Dark - Street Lights Off",
    "Dark - No Street Lights",
    "Other",
    "Empty String",
    "Dark - Unknown Lighting",
]

proportions.conditions_proportions(
    proportions.data_analyzer.weather_values, weather_values, "Weather"
)
proportions.conditions_proportions(
    proportions.data_analyzer.road_values, road_values, "Road"
)
proportions.conditions_proportions(
    proportions.data_analyzer.light_values, light_values, "Light"
)
