import re
from collections import defaultdict


class DataAnalysis():
    """
    DataAnalysis class that collects data from incident reports csv file
    For linear regression, use the following:
        - lr_x_values and lr_y_values
    For other regression, use the following:
        - or_x_values and or_y_values
    """
    def __init__(self, file_name):
        self.file_name = file_name
        self.X_INPUT = []
        self.Y_OUTPUT = []
        self.DATES = []

        # Incident Counts
        self.cycle_inc_count = 0
        self.total_count = 0

        # Normal array length
        self.NORM_LENGTH = 46

        # REGEX COMPILIERS
        self.CYCLES_REGEX = re.compile(r'(Cycles)')
        self.DATES_REGEX = re.compile(r'([0-9]{4}/[0-9]+/[0-9]+)')

        # SEVERITY CODE INFO
        # Severity Code Indexes
        self.sc_indicator = 11
        self.sc_ind = 12
        self.sc_desc_ind = 13
        # Severity Code Count and Dict
        self.sc_count_dict = defaultdict(lambda: 0)
        self.sc_desc_dict = defaultdict(lambda: '')

        # INJURY INFO
        # Injury indexes
        self.inj_ind = 19
        self.ser_inj_ind = 20
        self.fatalities_ind = 21
        # Injury Counts
        self.inj_count = 0
        self.ser_inj_count = 0
        self.fatalities_count = 0

        # ENVIRONMENT INFO
        # Environment indexes
        self.weather_ind = 29
        self.road_ind = 30
        self.light_ind = 31
        # Environment dictionaries and conversions
        self.weather_conv_counter = 0
        self.weather_dict = defaultdict()

        self.road_conv_counter = 0
        self.road_dict = defaultdict()

        self.light_conv_counter = 0
        self.light_dict = defaultdict()

        # [[19, 20, 21, 29, 30, 31]] -> x input
        # [12] -> y output

    def analyze_data(self):
        try:
            f = open(self.file_name, "r", encoding="utf-8")
        except OSError as e:
            print("Something went wrong")
            print(f"Error: {e}")

        for line in f:
            line = line.strip()
            self.total_count += 1
            if self.is_cycle_incident(line):
                self.cycle_inc_count += 1
                incident_date = self.get_incident_date(line)

                line = line.split(',')
                # Prepare all variables
                severity_code = self.get_severity_code(line)  # 12
                inj_data = self.get_inj_data(line)  # [19, 20, 21]
                env_data = self.get_environment_data(line)  # [29, 30, 31]

                # Create x input data
                x_input_array = inj_data + env_data

                # Add all variables to appropriate collection structure
                self.X_INPUT.append(x_input_array)
                self.Y_OUTPUT.append(severity_code)
                self.DATES.append(incident_date)

    def is_cycle_incident(self, line):
        """
        Method to determine whether an incident is a cycling incident
        Str -> Bool
        """
        return True if re.search(self.CYCLES_REGEX, line) else False

    def get_incident_date(self, line):
        """
        Method to get incident date
        Str -> Str
        """
        return re.findall(self.DATES_REGEX, line)[0]

    def get_severity_code(self, array):
        """
        Method to obtain severity code and collect severity data
        [Str] -> Str
        """
        sc = array[self.sc_ind]
        if array[self.sc_indicator]:  # Something here = the data was shifted 1
            sc = array[self.sc_ind + 1]
        if sc == "2b":  # Need a numerical value
            sc = 4
        if not self.sc_desc_dict[sc]:  # If we haven't encountered this sc yet
            self.sc_desc_dict[sc] = array[self.sc_desc_ind]  # Add the desc
        self.sc_count_dict[sc] += 1  # Increase this sc count
        return sc

    def get_inj_data(self, array):
        """
        Method to obtain injury info
        [Str] -> [Int, Int, Int]
        """
        injuries = int(array[self.inj_ind])
        serious_injuries = int(array[self.ser_inj_ind])
        fatalities = int(array[self.fatalities_ind])

        self.inj_count += injuries  # Increase total minor inj count
        self.ser_inj_count += serious_injuries  # Increase total ser inj count
        self.fatalities_count += fatalities  # Increase total fatal count

        return [injuries, serious_injuries, fatalities]

    def get_environment_data(self, array):
        """
        Method to obtain weather data
        [Str] -> [Int, Int, Int]
        """
        array_len = len(array)
        diff = array_len - self.NORM_LENGTH

        weather = array[self.weather_ind + diff]  # Get weather string
        if weather in self.weather_dict:
            weather = self.weather_dict[weather]  # Replace weather with code
        else:
            # Establish this weather with a code
            self.weather_dict[weather] = self.weather_conv_counter
            self.weather_conv_counter += 1  # Increase by 1 for uniqueness
            weather = self.weather_dict[weather]  # Replace weather with code

        # Same logic as weather for road and light conditions
        road_cond = array[self.road_ind + diff]
        if road_cond in self.road_dict:
            road_cond = self.road_dict[road_cond]
        else:
            self.road_dict[road_cond] = self.road_conv_counter
            self.road_conv_counter += 1
            road_cond = self.road_dict[road_cond]

        light_cond = array[self.light_ind + diff]
        if light_cond in self.light_dict:
            light_cond = self.light_dict[light_cond]
        else:
            self.light_dict[light_cond] = self.light_conv_counter
            self.light_conv_counter += 1
            light_cond = self.light_dict[light_cond]

        return [weather, road_cond, light_cond]

    @property
    def x_values(self):
        return self.X_INPUT

    @property
    def y_values(self):
        return self.Y_OUTPUT

    @property
    def incident_dates(self):
        return self.DATES
