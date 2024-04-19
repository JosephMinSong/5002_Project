import sys
from data_analysis_nb import DataAnalysis


def main(file_name):
    d_a = DataAnalysis(file_name)
    total = d_a.total
    total_viable = d_a.total_viable
    c_indicents = d_a.cycle_inc_count
    per_cycle_after = (d_a.cycle_inc_count/(d_a.total/4))*100
    weathers = list(d_a.weather_dict)
    roads = list(d_a.road_dict)
    lights = list(d_a.light_dict)
    print(f"Total incident count: {total}")
    print(f"Total viable incidents: {total_viable}")
    print(f"Difference: {total - total_viable}")
    print(f"Total cycling accidents: {c_indicents}")
    print(f"Percentage cycling accidents: {(c_indicents/total)*100}")
    print(f"Total incidents after data balancing: {total/4}")
    print(f"Percentage cycling accidents after balancing: {per_cycle_after}")
    print(f"\nAll weather condition values: {weathers}")
    print(f"\nAll road conditon values: {roads}")
    print(f"\nAll light condition values: {lights}")


main(sys.argv[1])
