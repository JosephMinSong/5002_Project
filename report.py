import sys
from data_analysis import DataAnalysis


def main(file_name):
    d_a = DataAnalysis(file_name)
    d_a.analyze_data()


main(sys.argv[1])
