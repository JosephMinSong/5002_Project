import sys
import numpy as np
from dataanalysis import DataAnalysis
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import seaborn as sns


file_name = sys.argv[1]
df_instance = DataAnalysis(file_name)
df_instance.analyze_data()
light = df_instance.light_values
weather = df_instance.weather_values
road = df_instance.road_values
x_values = np.array([[light[i], weather[i], road[i]] for i in range(len(light))])

y_values = np.array(df_instance.logr_y_values)
x_train, x_test, y_train, y_test = train_test_split(x_values, y_values, test_size=0.4, random_state=42)

model = LogisticRegression()
model.fit(x_train, y_train)

# Predictions
predictions = model.predict(x_test)

# Evaluation
print(confusion_matrix(y_test, predictions))
TN, FP, FN, TP = confusion_matrix(y_test, predictions).ravel()

print('True Positive(TP)  = ', TP)
print('False Positive(FP) = ', FP)
print('True Negative(TN)  = ', TN)
print('False Negative(FN) = ', FN)

accuracy = (TP + TN) / (TP + FP + TN + FN)
print('Accuracy of the binary classifier = {:0.3f}'.format(accuracy))
print(classification_report(y_test, predictions))


# Plot
cm = confusion_matrix(y_test, predictions)
# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d")
plt.title('Confusion Matrix')
plt.ylabel('Actual Label')
plt.xlabel('Predicted Label')
plt.show()
