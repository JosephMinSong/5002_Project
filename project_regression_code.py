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

    def report_environment(self):
        self.load_data()
        for data in self.df_instance.environment_data:
            print("Weather:", data[0], "Road:", data[1], "Light:", data[2])


file_name = sys.argv[1]
regression_model = RegressionModel(file_name)
regression_model.report_fatalities_and_incidents()
print(regression_model.perform_regression())
regression_model.report_environment()  # Call the method to print environment data
