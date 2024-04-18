import sys
import numpy as np
import statsmodels.api as sm
from dataanalysis import DataAnalysis


class RegressionModel:
    """
    A model for running regressions and reporting conditions based on traffic data
    """

    def __init__(self, file_name):
        self.file_name = file_name
        self.x_values = None
        self.y_values = None
        self.df_instance = None  # Reference to the DataAnalysis instance

    def load_data(self):
        """
        Loads and processes the data from the file
        """
        if not self.df_instance:
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
        """
        Performs linear regression analysis on the loaded data.
        Returns a summary of the regression model fit
        """
        self.load_data()
        X = sm.add_constant(self.x_values)
        y = self.y_values
        model = sm.OLS(y, X).fit()
        return model.summary()

    def report_fatalities_and_incidents(self):
        """
        Reports the number of fatalities and incidents
        Along with the proportion of fatalities to incidents
        """
        self.load_data()
        total_fatalities = self.df_instance.fatalities_count
        total_incidents = self.df_instance.cycle_inc_count
        proportion = total_fatalities / total_incidents
        print(f"The total number of fatalities: {total_fatalities}")
        print(f"Cycling incidents: {total_incidents}")
        print("Proportion:", proportion)

    def report_conditions(self, condition_values, condition_names, condition_type):
        """
        Method to report conditions such as weather, road, and lighting
        """
        self.load_data()
        total_incidents = self.df_instance.cycle_inc_count
        counts = np.zeros(len(condition_names), dtype=int) # initializes count array

        for index in condition_values: # count occurences of each condition
            if index < len(counts):
                counts[index] += 1

        print(f"\nCounts and Proportions for {condition_type} Conditions:")
        for name, count in zip(condition_names, counts):
            proportion = count / total_incidents if total_incidents else 0
            print(f"{name}: {count} ({proportion:.4f})")


file_name = sys.argv[1]
regression_model = RegressionModel(file_name)
print(regression_model.perform_regression())
print(regression_model.report_fatalities_and_incidents())
regression_model.report_conditions(
    regression_model.df_instance.weather_values,
    [
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
    ],
    "Weather",
)
regression_model.report_conditions(
    regression_model.df_instance.road_values,
    [
        "Dry",
        "Ice",
        "Unknown",
        "Wet",
        "Standing Water",
        "Snow",
        "Other",
        "Sand",
        "Empty String",
    ],
    "Road",
)
regression_model.report_conditions(
    regression_model.df_instance.light_values,
    [
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
    ],
    "Light",
)
