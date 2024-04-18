import sys
import numpy as np
import statsmodels.api as sm
from dataanalysis import DataAnalysis


class RegressionModel:
    def __init__(self, file_name):
        self.file_name = file_name
        self.x_values = None
        self.y_values = None
        self.df_instance = None  # Reference to the DataAnalysis instance

    def load_data(self):
        if not self.df_instance:  # Load data only if it hasn't been loaded before
            self.df_instance = DataAnalysis(self.file_name)
            self.df_instance.analyze_data()
            self.y_values = np.array(self.df_instance.linr_y_values, dtype=float)
            self.x_values = np.array(
                list(
                    zip(
                        self.df_instance.weather_values,
                        self.df_instance.road_values,
                        self.df_instance.light_values,
                    )
                ),
                dtype=float,
            )

    def perform_regression(self):
        self.load_data()  # Ensure data is loaded
        X = sm.add_constant(self.x_values)
        y = self.y_values
        model = sm.OLS(y, X).fit()
        return model.summary()

    def report_fatalities_and_incidents(self):
        self.load_data()  # Ensure data is loaded
        total_fatalities = self.df_instance.fatalities_count
        total_incidents = self.df_instance.cycle_inc_count
        print(f"The total number of fatalities: {total_fatalities}")
        print(f"Cycling incidents: {total_incidents}")
        proportion = total_fatalities / total_incidents
        print("Proportion:", proportion)

    def report_weather_conditions(self):
        self.load_data()
        total_incidents = self.df_instance.cycle_inc_count
        weather_conditions = [
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
        counts = [0] * len(weather_conditions)

        for weather_index in self.df_instance.weather_values:
            if weather_index < len(counts):
                counts[weather_index] += 1

        print("Counts for each weather condition:")
        for index, count in enumerate(counts):
            print(f"{weather_conditions[index]}: {count}")

        for index, count in enumerate(counts):
            proportion = count / total_incidents
            print(f"{weather_conditions[index]}: {count} ({proportion:.4f})")

    def report_road_conditions(self):
        self.load_data()
        total_incidents = self.df_instance.cycle_inc_count
        road_conditions = [
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
        counts = [0] * len(road_conditions)

        for road_index in self.df_instance.road_values:
            if road_index < len(counts):
                counts[road_index] += 1

        print("Counts for each road condition:")
        for index, count in enumerate(counts):
            print(f"{road_conditions[index]}: {count}")

        for index, count in enumerate(counts):
            proportion = count / total_incidents
            print(f"{road_conditions[index]}: {count} ({proportion:.4f})")

    def report_light_conditions(self):
        self.load_data()
        total_incidents = self.df_instance.cycle_inc_count
        light_conditions = [
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
        counts = [0] * len(light_conditions)

        for light_index in self.df_instance.light_values:
            if light_index < len(counts):
                counts[light_index] += 1

        print("Counts for each lighting condition:")
        for index, count in enumerate(counts):
            proportion = count / total_incidents
            print(f"{light_conditions[index]}: {count} ({proportion:.4f})")


file_name = sys.argv[1]
regression_model = RegressionModel(file_name)
regression_model.report_fatalities_and_incidents()
print(regression_model.perform_regression())
regression_model.report_weather_conditions()  # Call the method to print environment data
regression_model.report_road_conditions()
regression_model.report_light_conditions()
