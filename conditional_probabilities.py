import pandas as pd
from collections import defaultdict
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB, ComplementNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import warnings
from sklearn.exceptions import UndefinedMetricWarning

warnings.filterwarnings("ignore", category=UndefinedMetricWarning)


def calculate_conditional_probabilities(weather_data, road_data, light_data):
    """
    Calculates the frequency of bicycle-related incidents under different weather, road, and light conditions.
    Arguments:
    - weather_data: List of weather conditions for each cycling incident.
    - road_data: List of road conditions for each cycling incident.
    - light_data: List of light conditions for each cycling incident.
    """

    def print_probabilities(data, condition_type):
        count_dict = defaultdict(int)
        for condition in data:
            count_dict[condition] += 1
        total_incidents = len(data)
        print(f"Frequency of Bicycle Incidents by {condition_type} Conditions:")
        for condition, count in count_dict.items():
            if count > 0:
                frequency = count / total_incidents
                print(
                    f"Incident Frequency when {condition_type} is {condition} = {frequency:.4f}"
                )

    print_probabilities(weather_data, "Weather")
    print_probabilities(road_data, "Road")
    print_probabilities(light_data, "Light")


def load_and_prepare_data(filename):
    """
    Loads data from a CSV file, filters it for bicycle collisions, and prepares it for analysis.
    Outputs:
    - weather_data: List of weather conditions for filtered incidents.
    - road_data: List of road conditions for filtered incidents.
    - light_data: List of light conditions for filtered incidents.
    """
    df = pd.read_csv(filename)

    # Keep only data rows where collisions involve bicycles
    df = df[df["COLLISIONTYPE"].str.contains("Cycle", na=False)]

    weather_data = df["WEATHER"].tolist()
    road_data = df["ROADCOND"].tolist()
    light_data = df["LIGHTCOND"].tolist()

    return weather_data, road_data, light_data


def naive_bayes_classification(df):

    models = {
        "Multinomial": MultinomialNB(),
        "Gaussian": GaussianNB(),
        "Bernoulli": BernoulliNB(),
        "Complement": ComplementNB(),
    }

    # one-hot encode categorical variables
    weather_encoded = pd.get_dummies(df["WEATHER"])
    road_encoded = pd.get_dummies(df["ROADCOND"])
    light_encoded = pd.get_dummies(df["LIGHTCOND"])

    # Combine all feature data into a single DataFrame
    X = pd.concat([weather_encoded, road_encoded, light_encoded], axis=1)

    # encode the target label column "SEVERITYCODE"
    le = LabelEncoder()
    Y = le.fit_transform(df["SEVERITYCODE"])

    # Split data into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, random_state=42
    )

    # Initialize and train the Naive Bayes classifier
    model = MultinomialNB()
    model.fit(X_train, Y_train)

    # Make predictions on the test set
    Y_predictions = model.predict(X_test)

    # Evaluate the classifier
    accuracy = accuracy_score(Y_test, Y_predictions)
    conf_matrix = confusion_matrix(Y_test, Y_predictions)

    # print classification report with zero_division set to 0 to handle undefined metrics
    class_report = classification_report(Y_test, Y_predictions, zero_division=0)

    for model_name, model in models.items():
        model.fit(X_train, Y_train)
        Y_predictions = model.predict(X_test)
        accuracy = accuracy_score(Y_test, Y_predictions)
        conf_matrix = confusion_matrix(Y_test, Y_predictions)
        class_report = classification_report(Y_test, Y_predictions)

        print(f"{model_name} Naive Bayes Classifier Results:")
        print("Accuracy", accuracy)
        print("Confusion Matrix:")
        print(conf_matrix)
        print("Classification Report:")
        print(class_report)
        print("\n")


def main():
    filename = "collisions.csv"  # Path to the CSV file containing collision data
    df = pd.read_csv(filename)
    weather_data, road_data, light_data = load_and_prepare_data(filename)
    calculate_conditional_probabilities(weather_data, road_data, light_data)
    bicycle_df = df[df["COLLISIONTYPE"].str.contains("Cycle", na=False)]
    naive_bayes_classification(bicycle_df)


main()
