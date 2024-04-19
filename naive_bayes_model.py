from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB, ComplementNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix
from data_analysis_nb import DataAnalysis
import numpy as np
import sys


def main(file_name):
    da = DataAnalysis(file_name)
    NB_X_INPUT = da.NB_X
    NB_Y = da.NB_Y_INPUT

    x_train, x_test, y_train, y_test = train_test_split(
                                                        NB_X_INPUT,
                                                        NB_Y,
                                                        test_size=0.2,
                                                        random_state=42
                                                        )

    # MULTINOMIAL NB
    multinomial_model = MultinomialNB()
    multinomial_model.fit(x_train, y_train)
    multinomial_y_predictions = multinomial_model.predict(x_test)
    multinomial_accuracy = accuracy_score(y_test, multinomial_y_predictions)
    print("MULTINOMIAL NAIVE-BAYES MODEL")
    print("Overall Accuracy: ", multinomial_accuracy)
    print("Overall classification report:")
    print(classification_report(
        y_test, multinomial_y_predictions, zero_division=0))
    print("Confusion Matrix: ")
    print(confusion_matrix(y_test, multinomial_y_predictions))

    # GAUSSIAN NB
    gaussian_model = GaussianNB()
    gaussian_model.fit(x_train, y_train)
    gaussian_y_predictions = gaussian_model.predict(x_test)
    gaussian_accuracy = accuracy_score(y_test, gaussian_y_predictions)
    print("\n\nGAUSSIAN NAIVE-BAYES MODEL")
    print("Overall Accuracy: ", gaussian_accuracy)
    print("Overall classification report:")
    print(classification_report(
        y_test, gaussian_y_predictions, zero_division=0))
    print("Confusion Matrix: ")
    print(confusion_matrix(y_test, gaussian_y_predictions))

    # GAUSSIAN NB
    bernoulli_model = BernoulliNB()
    bernoulli_model.fit(x_train, y_train)
    bernoulli_y_predictions = bernoulli_model.predict(x_test)
    bernoulli_accuracy = accuracy_score(y_test, bernoulli_y_predictions)
    print("\n\nBERNOULLI NAIVE-BAYES MODEL")
    print("Overall Accuracy: ", bernoulli_accuracy)
    print("Overall classification report:")
    print(classification_report(
        y_test, bernoulli_y_predictions, zero_division=0))
    print("Confusion Matrix: ")
    print(confusion_matrix(y_test, bernoulli_y_predictions))

    # COMPLEMENT NB
    complement_model = ComplementNB()
    complement_model.fit(x_train, y_train)
    complement_y_predictions = complement_model.predict(x_test)
    complement_accuracy = accuracy_score(y_test, complement_y_predictions)
    print("\n\nCOMPLEMENT NAIVE-BAYES MODEL")
    print("Overall Accuracy: ", complement_accuracy)
    print("Overall classification report:")
    print(classification_report(
        y_test, complement_y_predictions, zero_division=0))
    print("Confusion Matrix: ")
    print(confusion_matrix(y_test, complement_y_predictions))

    print("\n\nX_train shape:", np.array(x_train).shape)
    print("X_test shape:", np.array(x_test).shape)

    print("y_train shape:", np.array(y_train).shape)
    print("y_test shape:", np.array(y_test).shape)


main(sys.argv[1])
