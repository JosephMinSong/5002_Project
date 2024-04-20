import sys
import numpy as np
from dataanalysis import DataAnalysis
import matplotlib.pyplot as plt

# Create a virtual environment
# python -m venv env
# Activate the virtual environment
# On macOS and Linux, use:
# source env/bin/activate
# Install packages
# pip install numpy matplotlib
# Run script
# python your_script.py
# To stop using the virtual environment, deactivate it
# deactivate OR ctrl + c


class Proportions:
    def __init__(self, filename):
        # Constructor to initialize the class with a filename and setup data structures
        self.filename = filename
        self.data_analyzer = None
        # Lists of conditions to track in the data
        self.weather_values = [
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
        self.road_values = [
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
        self.light_values = [
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
        # Initialize dictionaries to keep track of counts for each condition
        self.weather_counts = {w: 0 for w in self.weather_values}
        self.road_counts = {r: 0 for r in self.road_values}
        self.light_counts = {l: 0 for l in self.light_values}

    def load_data(self):
        # Method to load and process data using a custom data analysis module
        if self.data_analyzer is None:
            self.data_analyzer = DataAnalysis(self.filename)
            self.data_analyzer.analyze_data()

    def conditions_proportions(self, condition_values, condition_names, condition_type):
        # Method to calculate and display the proportions of different accident conditions
        self.load_data()
        total_incidents = self.data_analyzer.cycle_inc_count
        counts = {name: 0 for name in condition_names}

        for value in condition_values:
            if value < len(condition_names):
                counts[condition_names[value]] += 1

        setattr(self, f"{condition_type.lower()}_counts", counts)

        print(f"\nCounts and Proportions for {condition_type} Conditions:")
        for name, count in counts.items():
            proportion = count / total_incidents if total_incidents else 0
            print(f"{name}: {count} ({proportion:.4f})")

    def visualize_data(self, accident_type):
        # Method to generate bar graphs for the specified type of accident
        self.load_data()
        if accident_type == "all":
            filtered_indices = range(len(self.data_analyzer.weather_values))
        elif accident_type == "fatal":
            filtered_indices = [
                i for i, x in enumerate(self.data_analyzer.logr_y_values) if x == 1
            ]
        elif accident_type == "non_fatal":
            filtered_indices = [
                i for i, x in enumerate(self.data_analyzer.logr_y_values) if x == 0
            ]
        else:
            raise ValueError(
                "Invalid accident type specified. Choose from 'all', 'fatal', 'non_fatal'."
            )

        # Plotting
        fig, axs = plt.subplots(3, 1, figsize=(10, 15))
        fig.suptitle(f"Accident Conditions for {accident_type.capitalize()} Accidents")

        for ax, (condition_dict, title) in zip(
            axs,
            [
                (self.weather_counts, "Weather Conditions"),
                (self.road_counts, "Road Conditions"),
                (self.light_counts, "Lighting Conditions"),
            ],
        ):
            ax.bar(condition_dict.keys(), condition_dict.values(), color="tab:blue")
            ax.set_title(title)
            ax.set_ylabel("Count")
            ax.set_xlabel("Condition Type")
        plt.tight_layout()
        plt.show()


filename = "Collisions.csv"
proportions = Proportions(filename)
proportions.load_data()
proportions.conditions_proportions(
    proportions.data_analyzer.weather_values, proportions.weather_values, "Weather"
)
proportions.conditions_proportions(
    proportions.data_analyzer.road_values, proportions.road_values, "Road"
)
proportions.conditions_proportions(
    proportions.data_analyzer.light_values, proportions.light_values, "Light"
)
proportions.visualize_data("fatal")
proportions.visualize_data("non_fatal")
proportions.visualize_data("all")
