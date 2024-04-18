import sys
from dataanalysis import DataAnalysis


def main(file_name):
    d_a = DataAnalysis(file_name)
    d_a.analyze_data()
    # print(d_a.logr_x_values)
    print(d_a.logr_y_values)


main(sys.argv[1])
