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
        clear = 0
        overcast = 0
        unknown = 0
        raining = 0
        other = 0
        snow = 0
        sleet = 0
        fog = 0
        sand = 0
        partly_cloudy = 0
        total_incidents = self.df_instance.cycle_inc_count

        for i in self.df_instance.weather_values:
            if i == 0:
                clear += 1
            if i == 1:
                overcast += 1
            if i == 2:
                unknown += 1
            if i == 3:
                raining += 1
            if i == 4:
                other += 1
            if i == 5:
                snow += 1
            if i == 6:
                sleet += 1
            if i == 8:
                fog += 1
            if i == 9:
                sand += 1
            if i == 10:
                partly_cloudy += 1

        # print(raining)
        # proportion = raining / total_incidents
        # print(proportion)

    def report_road_conditions(self):
        dry = 0
        ice = 0
        unknown = 0
        wet = 0
        standing_water = 0
        snow = 0
        other = 0
        sand = 0

        print(self.df_instance.road_dict)

        for i in self.df_instance.road_dict:
            if i == 0:
                dry += 1
            if i == 1:
                ice += 1
            if i == 2:
                unknown += 1
            if i == 3:
                wet += 1
            if i == 4:
                standing_water += 1
            if i == 5:
                snow += 1
            if i == 6:
                other += 1
            if i == 7:
                sand += 1
        print(dry)

    def report_light_conditions(self):
        daylight = 0
        street_light = 0
        dusk = 0
        unknown = 0
        dawn = 0
        dark_sl_off = 0
        dark_no_sl = 0
        other = 0
        dark_unknown = 0
        for i in self.df_instance.light_dict:
            if i == 0:
                daylight += 1
            if i == 1:
                street_light += 1
            if i == 2:
                dusk += 1
            if i == 3:
                unknown += 1
            if i == 4:
                dawn += 1
            if i == 5:
                dark_sl_off += 1
            if i == 6:
                dark_no_sl += 1
            if i == 7:
                other += 1
            if i == 8:
                dark_unknown += 1
        print(self.df_instance.light_dict)


file_name = sys.argv[1]
regression_model = RegressionModel(file_name)
regression_model.report_fatalities_and_incidents()
print(regression_model.perform_regression())
regression_model.report_weather_conditions()  # Call the method to print environment data
regression_model.report_road_conditions()
regression_model.report_light_conditions()
