import re
from collections import defaultdict


class DataAnalysis:
    """
    DataAnalysis class that collects data from incident reports csv file
    For linear regression, use the following:
        - linr_x_values and linr_y_values
    For other regression, use the following:
        - logr_x_values and logr_y_values
    """

    def __init__(self, file_name):
        self.file_name = file_name

        # DATA FOR X_INPUT
        self.WEATHER = []
        self.LIGHT = []
        self.ROAD = []

        # DATA FOR LINR
        self.LINR_Y_OUTPUT = []  # severity code [1, 2, 3]

        # DATA FOR LOGR
        self.LOGR_Y_OUTPUT = []  # 0 or 1, based on fatality [0, 1, 1]

        # Dates
        self.DATES = []

        # Incident Counts
        self.cycle_inc_count = 0
        self.total_count = 0

        # Normal array length
        self.NORM_LENGTH = 46

        # REGEX COMPILIERS
        self.CYCLES_REGEX = re.compile(r"(Cycles)")
        self.DATES_REGEX = re.compile(r"([0-9]{4}/[0-9]+/[0-9]+)")

        # SEVERITY CODE INFO
        # Severity Code Indexes
        self.sc_indicator = 11
        self.sc_ind = 12
        self.sc_desc_ind = 13
        # Severity Code Count and Dict
        self.sc_count_dict = defaultdict(lambda: 0)
        self.sc_desc_dict = defaultdict(lambda: "")

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

        self.environment_data = []  # store data

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

                line = line.split(",")
                # Prepare all variables
                severity_code = self.get_severity_code(line)  # 12
                fatality_data = self.get_fatality_data(line)  # 21
                env_data = self.get_environment_data(line)  # [w, r, l]
                self.environment_data.append(env_data)

                # Create logr_x input data -> 1 or 0, based on fatality
                logr_x_input = 1 if fatality_data else 0

                # Add all variables to appropriate collection structure
                self.WEATHER.append(env_data[0])
                self.ROAD.append(env_data[1])
                self.LIGHT.append(env_data[2])

                # For LINR
                self.LINR_Y_OUTPUT.append(severity_code)
                self.DATES.append(incident_date)

                # For LOGR
                self.LOGR_Y_OUTPUT.append(logr_x_input)

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

    def get_fatality_data(self, array):
        """
        Method to obtain injury info
        [Str] -> [Int, Int, Int]
        """
        fatalities = int(array[self.fatalities_ind])

        self.fatalities_count += fatalities  # Increase total fatal count

        return fatalities

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
    def weather_values(self):
        return self.WEATHER

    @property
    def light_values(self):
        return self.LIGHT

    @property
    def road_values(self):
        return self.ROAD

    @property
    def incident_dates(self):
        return self.DATES

    @property
    def linr_y_values(self):
        return self.LINR_Y_OUTPUT

    @property
    def logr_y_values(self):
        return self.LOGR_Y_OUTPUT
