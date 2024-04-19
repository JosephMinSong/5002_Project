import re
from collections import defaultdict


class DataAnalysis():
    """
    DataAnalysis class that collects data from incident reports csv file
    """
    def __init__(self, file_name):
        self.file_name = file_name
        self.UNKNOWN_STRING = "Unknown"
        self.EVERY_NTH = 0
        self.NTH = 25

        self.NB_ENV = []
        self.NB_Y = []

        # ENV DATA
        self.NB_WEATHER = []
        self.NB_LIGHT = []
        self.NB_ROAD = []

        # Incident Counts
        self.cycle_inc_count = 0
        self.total_count = 0
        self.total_viable = 0
        self.total = 0

        # REGEX COMPILIERS
        self.CYCLES_REGEX = re.compile(r'(Cycles)')

        # ENVIRONMENT INFO
        # Environment indexes
        self.weather_ind = -3
        self.road_ind = -2
        self.light_ind = -1
        # Environment dictionaries and conversions
        self.weather_conv_counter = 0
        self.weather_dict = defaultdict()
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
        self.road_indicators_1 = {
            "Dark - Street Lights On",
            "Dark - No Street Lights",
            "Dusk"
        }

        self.light_conv_counter = 0
        self.light_dict = defaultdict()
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
                # if it's a cycling accident or not
                if cycling_accident:
                    self.cycle_inc_count += 1
                    self.NB_Y.append(1)
                    # if we have appropriate env data, add it to the x values
                    self.NB_ENV.append(env_data)
                else:
                    if self.EVERY_NTH % self.NTH == 0:
                        self.NB_Y.append(0)
                        self.NB_ENV.append(env_data)
                    self.EVERY_NTH += 1

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

        weather = array[weather_index]
        if not weather or weather == self.UNKNOWN_STRING:  #
            return None
        if weather in self.weather_dict:
            weather = self.weather_dict[weather]  # Replace weather with code
        else:
            # Establish this weather with a code
            self.weather_dict[weather] = self.weather_conv_counter
            self.weather_conv_counter += 1  # Increase by 1 for uniqueness
            weather = self.weather_dict[weather]  # Replace weather with code

        # Same logic as weather for road and light conditions
        road_cond = array[road_index]
        if not road_cond or road_cond == self.UNKNOWN_STRING:
            return None
        if road_cond in self.road_dict:
            road_cond = self.road_dict[road_cond]
        else:
            self.road_dict[road_cond] = self.road_conv_counter
            self.road_conv_counter += 1
            road_cond = self.road_dict[road_cond]

        light_cond = array[light_index]
        if not light_cond or light_cond == self.UNKNOWN_STRING:
            return None
        if light_cond in self.light_dict:
            light_cond = self.light_dict[light_cond]
        else:
            self.light_dict[light_cond] = self.light_conv_counter
            self.light_conv_counter += 1
            light_cond = self.light_dict[light_cond]

        return [weather, road_cond, light_cond]

    @property
    def NB_X(self):
        return self.NB_ENV

    @property
    def NB_Y_INPUT(self):
        return self.NB_Y

    @property
    def NB_X_WEATHER(self):
        return self.NB_WEATHER

    @property
    def NB_X_ROAD(self):
        return self.NB_ROAD

    @property
    def NB_X_LIGHT(self):
        return self.NB_LIGHT
