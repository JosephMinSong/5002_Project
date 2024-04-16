import sys
import numpy as np
import statsmodels.api as sm
from dataframe import DataAnalysis


class RegressionModel:
    def __init__(self, x_values, y_values):
        self.x_values = x_values
        self.y_values = y_values
    
    def perform_regression(self):
        X = sm.add_constant(self.x_values)
        y = self.y_values
        model = sm.OLS(y, X).fit()
        return model.summary()


file_name = sys.argv[1]
df_instance = DataAnalysis(file_name)
df_instance.analyze_data()

x_values = np.array(df_instance.x_values, dtype=float)
y_values = np.array(df_instance.y_values, dtype=float)

regression_model = RegressionModel(x_values, y_values)
result = regression_model.perform_regression()
print(result)
