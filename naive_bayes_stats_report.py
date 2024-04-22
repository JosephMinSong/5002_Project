import sys
from naive_bayes_stats import DataAnalysis
from collections import defaultdict


def sort_dictionary(dictionary):
    return sorted(dictionary.items(),
                  key=lambda x: x[1],
                  reverse=True)


def bayes_calculation(p_a1_b1, p_a1_b2, b1, b2):
    numerator = p_a1_b1 * b1
    denominator = (p_a1_b1 * b1) + (p_a1_b2 * b2)
    return numerator/denominator


def naive_bayes_calculation(p_a1_b1, b1, a1):
    numerator = p_a1_b1 * b1
    denominator = a1
    return numerator/denominator


def main(file_name):
    d_a = DataAnalysis(file_name)

    # RESULTS AND REPORT
    env_set_probs = defaultdict(lambda: 0)
    weather_probs = defaultdict(lambda: 0)
    road_probs = defaultdict(lambda: 0)
    light_probs = defaultdict(lambda: 0)
    probs = [
        env_set_probs,
        weather_probs,
        road_probs,
        light_probs
    ]

    order = [
        "Conditional Environment Probabilities",
        "Conditional Weather Probabilities",
        "Conditional Road Condition Probabilities",
        "Conditional Light Condition Probabilities"
    ]

    # CONVERTERS
    env_set_converter = d_a.env_converter
    weather_converter = d_a.weather_cond_converter
    road_converter = d_a.road_cond_converter
    light_converter = d_a.light_cond_converter
    converters = [
        env_set_converter,
        weather_converter,
        road_converter,
        light_converter
    ]

    # CONSTANTS
    total_incidents_overall = d_a.total
    total_incidents = d_a.total_viable
    total_cycling_incidents = d_a.cycle_inc_count
    total_no_cycle_incidents = d_a.no_accident_count
    B1 = total_cycling_incidents/total_incidents
    B2 = total_no_cycle_incidents/total_incidents

    # TOTAL ENVIRONMENT COUNTS DICTIONARY
    total_env_counts = d_a.total_env_counts
    total_weather_counts = d_a.total_weather_counts
    total_road_counts = d_a.total_road_counts
    total_light_counts = d_a.total_light_counts
    total_env_list = [
        total_env_counts,
        total_weather_counts,
        total_road_counts,
        total_light_counts
    ]

    # CYCLING ENVIRONMENT COUNTS DICTIONARY
    cycling_env_counts = d_a.cycle_env_counts
    cycling_weather_counts = d_a.cycle_weather_counts
    cycling_road_counts = d_a.cycle_road_counts
    cycling_light_counts = d_a.cycle_light_counts
    cycle_env_list = [
        cycling_env_counts,
        cycling_weather_counts,
        cycling_road_counts,
        cycling_light_counts
    ]

    # NON-CYCLING ENVIRONMENT COUNTS DICTIONARY
    n_cycling_env_counts = d_a.non_cycle_env_counts
    n_cycling_weather_counts = d_a.non_cycle_weather_counts
    n_cycling_road_counts = d_a.non_cycle_road_counts
    n_cycling_light_counts = d_a.non_cycle_light_counts
    n_cycle_env_list = [
        n_cycling_env_counts,
        n_cycling_weather_counts,
        n_cycling_road_counts,
        n_cycling_light_counts
    ]

    for i in range(len(total_env_list)):
        for key in total_env_list[i]:
            p_a1_b1 = cycle_env_list[i][key]/total_cycling_incidents
            p_a1_b2 = n_cycle_env_list[i][key]/total_no_cycle_incidents
            prob = bayes_calculation(p_a1_b1, p_a1_b2, B1, B2)
            if prob:
                probs[i][key] = prob

    for i in range(len(probs)):
        sorted_probs = sort_dictionary(probs[i])
        print(order[i])
        for entry in sorted_probs:
            condition = converters[i][entry[0]]
            probability = entry[1] * 100
            print(f"{condition}: {probability}")


main(sys.argv[1])
