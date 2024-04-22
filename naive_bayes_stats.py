import re
from collections import defaultdict


class DataAnalysis():
    """
    DataAnalysis class that collects data from incident reports csv file
    """
    def __init__(self, file_name):
        self.file_name = file_name
        self.UNKNOWN_STRING = "Unknown"

        # COUNTS
        self.total = 0
        self.total_viable = 0
        self.cycle_inc_count = 0
        self.no_accident_count = 0

        # total environment set collection
        self.env_count_dict = defaultdict(lambda: 0)

        # total individual count dicts
        self.weather_count_dict = defaultdict(lambda: 0)
        self.road_count_dict = defaultdict(lambda: 0)
        self.light_count_dict = defaultdict(lambda: 0)

        # cycling count dicts
        self.cycle_env_c_d = defaultdict(lambda: 0)
        self.cycle_weather_c_d = defaultdict(lambda: 0)
        self.cycle_road_c_d = defaultdict(lambda: 0)
        self.cycle_light_c_d = defaultdict(lambda: 0)

        # non-cycling accident count dicts
        self.non_cycle_env_c_d = defaultdict(lambda: 0)
        self.non_cycle_weather_c_d = defaultdict(lambda: 0)
        self.non_cycle_road_c_d = defaultdict(lambda: 0)
        self.non_cycle_light_c_d = defaultdict(lambda: 0)

        # REGEX COMPILIERS
        self.CYCLES_REGEX = re.compile(r'(Cycles)')

        # ENVIRONMENT INFO
        # Environment indexes
        self.weather_ind = -3
        self.road_ind = -2
        self.light_ind = -1
        # Environment dictionaries and conversions
        self.env_set_converter = defaultdict(lambda: 0)
        self.weather_conv_counter = 0
        self.weather_dict = defaultdict()
        self.weather_dict_conv = defaultdict()
        self.weather_indicators_2 = {
            "Dark - No Street Lights",
            "Dark - Street Lights Off",
            "Dark - Street Lights On",
            "Dusk",
            "Daylight"
        }
        self.weather_indicators_1 = {
            "Wet",
            "Dry"
        }

        self.road_conv_counter = 0
        self.road_dict = defaultdict()
        self.road_dict_conv = defaultdict()
        self.road_indicators_1 = {
            "Dark - Street Lights On",
            "Dark - No Street Lights",
            "Dusk"
        }

        self.light_conv_counter = 0
        self.light_dict = defaultdict()
        self.light_dict_conv = defaultdict()
        self.analyze_data()

    def analyze_data(self):
        try:
            f = open(self.file_name, "r", encoding="utf-8")
        except OSError as e:
            print("Something went wrong")
            print(f"Error: {e}")

        f.readline()

        for line in f:
            line = line.strip()
            split_line = line.split(',')[:-14]
            cycling_accident = self.is_cycle_incident(line)
            env_data = self.get_environment_data(split_line)  # [w, r, l]
            self.total += 1

            if env_data:
                self.total_viable += 1
                env_tuple = tuple(env_data)
                weather_cond, road_cond, light_cond = env_data
                if cycling_accident:
                    self.cycle_inc_count += 1
                    # env set in cycles
                    self.cycle_env_c_d[env_tuple] += 1
                    # increase individual info in cycles
                    self.cycle_weather_c_d[weather_cond] += 1
                    self.cycle_road_c_d[road_cond] += 1
                    self.cycle_light_c_d[light_cond] += 1
                else:
                    self.no_accident_count += 1
                    # env set in non_cycles
                    self.non_cycle_env_c_d[env_tuple] += 1
                    # increase individual info in cycles
                    self.non_cycle_weather_c_d[weather_cond] += 1
                    self.non_cycle_road_c_d[road_cond] += 1
                    self.non_cycle_light_c_d[light_cond] += 1

                # regardless, increase the totals of each
                self.env_count_dict[env_tuple] += 1
                self.weather_count_dict[weather_cond] += 1
                self.road_count_dict[road_cond] += 1
                self.light_count_dict[light_cond] += 1

    def is_cycle_incident(self, line):
        """
        Method to determine whether an incident is a cycling incident
        Str -> Bool
        """
        return True if re.search(self.CYCLES_REGEX, line) else False

    def get_environment_data(self, array):
        """
        Method to obtain weather data
        [Str] -> [Int, Int, Int]
        """
        weather_index = self.weather_ind
        road_index = self.road_ind
        light_index = self.light_ind

        weather = array[weather_index]
        if weather in self.weather_indicators_2:  # data shifted by 2
            weather_index -= 2
            road_index -= 2
            light_index -= 2
        elif weather in self.weather_indicators_1:  # data shifted by 1
            weather_index -= 1
            road_index -= 1
            light_index -= 1

        env_set_convert = []
        weather = array[weather_index]
        if not weather or weather == self.UNKNOWN_STRING:
            return None
        env_set_convert.append(weather)  # add to convert before
        if weather in self.weather_dict:
            weather = self.weather_dict[weather]  # Replace weather with code
        else:
            # Establish this weather with a code
            self.weather_dict[weather] = self.weather_conv_counter
            # Establish converter dictionary as well
            self.weather_dict_conv[self.weather_conv_counter] = weather
            self.weather_conv_counter += 1  # Increase by 1 for uniqueness
            weather = self.weather_dict[weather]  # Replace weather with code

        # Same logic as weather for road and light conditions
        road_cond = array[road_index]
        if not road_cond or road_cond == self.UNKNOWN_STRING:
            return None
        env_set_convert.append(road_cond)  # add to convert before
        if road_cond in self.road_dict:
            road_cond = self.road_dict[road_cond]
        else:
            self.road_dict[road_cond] = self.road_conv_counter
            self.road_dict_conv[self.road_conv_counter] = road_cond
            self.road_conv_counter += 1
            road_cond = self.road_dict[road_cond]

        light_cond = array[light_index]
        if not light_cond or light_cond == self.UNKNOWN_STRING:
            return None
        env_set_convert.append(light_cond)  # add to convert before
        if light_cond in self.light_dict:
            light_cond = self.light_dict[light_cond]
        else:
            self.light_dict[light_cond] = self.light_conv_counter
            self.light_dict_conv[self.light_conv_counter] = light_cond
            self.light_conv_counter += 1
            light_cond = self.light_dict[light_cond]

        env = (weather, road_cond, light_cond)
        self.env_set_converter[env] = tuple(env_set_convert)
        return [weather, road_cond, light_cond]

    @property
    def total_env_counts(self):
        return self.env_count_dict

    @property
    def total_weather_counts(self):
        return self.weather_count_dict

    @property
    def total_road_counts(self):
        return self.road_count_dict

    @property
    def total_light_counts(self):
        return self.light_count_dict

    @property
    def cycle_env_counts(self):
        return self.cycle_env_c_d

    @property
    def cycle_weather_counts(self):
        return self.cycle_weather_c_d

    @property
    def cycle_road_counts(self):
        return self.cycle_road_c_d

    @property
    def cycle_light_counts(self):
        return self.cycle_light_c_d

    @property
    def non_cycle_env_counts(self):
        return self.non_cycle_env_c_d

    @property
    def non_cycle_weather_counts(self):
        return self.non_cycle_weather_c_d

    @property
    def non_cycle_road_counts(self):
        return self.non_cycle_road_c_d

    @property
    def non_cycle_light_counts(self):
        return self.non_cycle_light_c_d

    @property
    def env_converter(self):
        return self.env_set_converter

    @property
    def weather_cond_converter(self):
        return self.weather_dict_conv

    @property
    def road_cond_converter(self):
        return self.road_dict_conv

    @property
    def light_cond_converter(self):
        return self.light_dict_conv
