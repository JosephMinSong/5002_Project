import pandas as pd
import numpy as np
from pmdarima.arima import auto_arima
from dataframe import DataAnalysis

# Step 1: Need to create instance of DataAnalysis
df_instance = DataAnalysis(file_name)
df_instance.analyze_data()
# Step 2: Prepare data
df_instance['date'] = pd.to_datetime(df_instance.incident_dates)

# Step 3: Fit the regression model
x = df_instance.x_values
y = df_instance.y_values

model = auto_arima(y, exogenous=x, seasonal=False) # Ordinary Least Squares regression
results = model.fit()

# Step 4: Evaluate the model
print(results.summary())
