import re
from collections import defaultdict


class DataAnalysis():
    def __init__(self, file_name):
        self.file_name = file_name

        # REGEX COMPILIERS
        self.CYCLES_REGEX = re.compile(r'(Cycles)')
        self.DATES_REGEX = re.compile(r'([0-9]{4}/[0-9]+/[0-9]+)')

        # SEVERITY CODE INFO
        self.severity_code_count_dict = defaultdict(lambda: 0)
        self.severity_code_description = defaultdict(lambda: '')

        # INJURY INFO
        # - Injury should probably have some corelation to 29, 30, 31

        # Could possibly group pieces of important data into a tuple and store

        # INDEX FOR EACH PIECE OF DATA
        # 12 = SEVERITY CODE
        # 13 = SEVERITY DESCRIPTION

        # 19 = INJURIES
        # 20 = SERIOUS INJURIES
        # 21 = FATALITIES

        # 29 = WEATHER

        # 30 = ROAD CONDITION

        # 31 = LIGHT CONDITION

    def analyze_data(self):
        try:
            f = open(self.file_name, "r", encoding="utf-8")
        except OSError as e:
            print("Something went wrong")
            print(f"Error: {e}")

        for line in f:
            line = line.strip()
            if self.is_cycle_incident(line):
                pass

    def is_cycle_incident(self, line):
        """
        Method to determine whether an incident is a cycling incident
        """
        return re.search(self.CYCLES_REGEX, line)

    def get_incident_date(self, line):
        """
        Method to get incident date
        """
        return re.findall(self.DATES_REGEX, line)[0]
