import pandas as pd
import numpy as np
from pmdarima.arima import auto_arima
from dataframe import DataAnalysis as df

# Assuming you have a DataFrame 'df' with columns 'date' and 'target_variable'
# where 'date' is the datetime variable and 'target_variable' is what you want to predict.

# Step 2: Prepare data
df['date'] = pd.to_datetime(df.incident_dates)

# Step 3: Fit the regression model
x = df.x_values
y = df.y_values

model = auto_arima(df.y_values, exogenous = df.x_values, seasonal=False) # Ordinary Least Squares regression
results = model.fit()

# Step 4: Evaluate the model
print(results.summary())
