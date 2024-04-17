import pandas as pd
import numpy as np
from pmdarima.arima import auto_arima
from dataanalysis import DataAnalysis
import sys


def main(file_name):
    # Step 1: Need to create instance of DataAnalysis
    df_instance = DataAnalysis(file_name)
    df_instance.analyze_data()
    # Step 2: Prepare data
    # df_instance['date'] = pd.to_datetime(df_instance.incident_dates)

    # Step 3: Fit the regression model
    x = df_instance.x_values
    y = df_instance.y_values

    # Ordinary Least Squares regression
    model = auto_arima(y, exogenous=x, seasonal=False)
    results = model.fit()  # needs y value

    # Step 4: Evaluate the model
    print(results.summary())


main(sys.argv[1])
