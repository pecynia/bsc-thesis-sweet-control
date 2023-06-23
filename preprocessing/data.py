import pandas as pd
import math
import csv

# Tools
import enums


# Class for keeping track of the time and date on the x-axis
class TemporalData:
    def __init__(self, xls):
        self.x_axis = []  # Array with all time and date values
        self.cgm_raw = xls['glucose_15']
        self.bolus_raw = xls['new_bolus']
        self.basal_raw = xls['new_basal']
        self.heart_rate_raw = xls['heart_rate']
        self.xdrip_raw = xls['xdrip']

        self.earliest = None
        self.latest = None

    # Get the latest earlies time and date for all raw data
    def process_temporal(self):
        # Get the earliest time and date and the latest, and create an array with one minute intervals
        # between the earliest and latest time and date
        earlierst_bolus = self.bolus_raw['Timestamp'][len(self.bolus_raw['Timestamp']) - 1]
        latest_bolus = self.bolus_raw['Timestamp'][0]

        earlierst_basal = self.basal_raw['Timestamp'][len(self.basal_raw['Timestamp']) - 1]
        latest_basal = self.basal_raw['Timestamp'][0]

        # For the CGM data, the time and date is descending instead of ascending
        earlierst_cgm = self.cgm_raw['Tijdstempel apparaat'][0]
        latest_cgm = self.cgm_raw['Tijdstempel apparaat'][len(self.cgm_raw['Tijdstempel apparaat']) - 1]

        # Similiary for the xdrip data
        earlierst_xdrip = self.xdrip_raw['Tijdstempel apparaat'][0]
        latest_xdrip = self.xdrip_raw['Tijdstempel apparaat'][len(self.xdrip_raw['Tijdstempel apparaat']) - 1]

        # Similiary for the heart rate data
        earliest_heart_rate = self.heart_rate_raw['Timestamp'][0]
        latest_heart_rate = self.heart_rate_raw['Timestamp'][len(self.heart_rate_raw['Timestamp']) - 1]

        # Get the latest earliest time and date, this represents the time and date for which we have all data points
        earliest = min(earlierst_bolus, earlierst_basal, earlierst_cgm, earlierst_xdrip, earliest_heart_rate)
        latest = max(latest_bolus, latest_basal, latest_cgm, latest_xdrip, latest_heart_rate)

        self.earliest = earliest
        self.latest = latest

        # Create array with one minute intervals between the earliest and latest time and date
        self.x_axis = pd.date_range(earliest, latest, freq='1min')


# Class for insulin data
class InsulinData:
    def __init__(self, xls):
        self.insulin = {}  # Dictionary with all insulin per time
        self.bolus_insulin = {}  # Dictionary with all bolus insulin per time
        self.basal_insulin = {}  # Dictionary with all basal insulin per time
        self.units_raw = {}  # Dictionary with all units per time
        self.temporal = TemporalData(xls)

        # Get the raw data from the excel file
        self.cgm_raw = xls['glucose_15']
        self.bolus_raw = xls['new_bolus']
        self.basal_raw = xls['new_basal']
        self.heart_rate_raw = xls['heart_rate']
        self.xdrip_raw = xls['xdrip']

    # Process the basal data
    def process_bolus(self):
        """
        Add the activity of the bolus to the insulin dictionary by looping through the bolus data, starting at the end
        """
        # Loop through the bolus data, starting at the end, and add the activity of the bolus to the insulin dictionary
        for i in range(len(self.bolus_raw['Timestamp']) - 1, -1, -1):
            # Get the time and units of the bolus
            base_time = self.bolus_raw['Timestamp'][i]
            units = self.bolus_raw['Insulin Delivered (U)'][i]

            # Add the activity of the bolus to the insulin dictionary
            self.process_raw_bolus(base_time, units)
            self.set_bolus_activity(base_time, units, True)

    def process_raw_bolus(self, base_time, units):
        """
        Add the activity of the bolus to the insulin dictionary by looping through the bolus data, starting at the end
        """
        # Get the time and units of the bolus
        # Add the activity of the bolus to the insulin dictionary
        if base_time not in self.units_raw:
            self.units_raw[base_time] = units

        else:
            self.units_raw[base_time] += units


    # Add the activity of the bolus to the insulin dictionary
    def set_bolus_activity(self, basetime, units, bolus):
        """
        Add the activity of the bolus to the insulin dictionary by looping through the time array and adding the activity to the insulin dictionary
        params: basetime: datetime object, the time of the bolus; units: float, the amount of insulin in the bolus
        """
        insulin_activity_raw = enums.INSULIN_ACTIVITY_FUNCTION(
            units)  # returns a 1D numpy array with 500 values representing the activity per minute for 8.33 hours

        # Get the time for the activity by making an array of 500 values with 1 minute intervals, with the first value being the base time + 13 minutes for the insulin delay
        base_time = basetime + pd.Timedelta(minutes=enums.INSULIN_ACTIVITY_DELAY)
        time_array = pd.date_range(base_time, periods=len(insulin_activity_raw),
                                   freq='1min')  # array of 500 values with 1 minute intervals after the base time and after the insulin delay

        # Loop through the time array and add the activity to the insulin dictionary
        for i in range(0, len(time_array)):
            time = time_array[i]
            activity = insulin_activity_raw[i]

            # If the time is not in the dictionary, add it
            if time not in self.insulin:
                self.insulin[time] = activity

            # If the time is in the dictionary, add the activity to the existing activity
            else:
                self.insulin[time] += activity

            if bolus and time not in self.bolus_insulin:
                self.bolus_insulin[time] = activity

            elif bolus and time in self.bolus_insulin:
                self.bolus_insulin[time] += activity

            elif not bolus and time not in self.basal_insulin:
                self.basal_insulin[time] = activity

            elif not bolus and time in self.basal_insulin:
                self.basal_insulin[time] += activity

                # Process the basal data

    def process_basal(self):
        """
        Add the activity of the basal to the insulin dictionary by looping through the basal data, starting at the end
        """
        # Loop through the basal data, starting at the end, and add the activity of the basal to the insulin dictionary
        for i in range(len(self.basal_raw['Timestamp']) - 1, -1, -1):
            # Get the time and units of the basal
            base_time = self.basal_raw['Timestamp'][i]
            rate = self.basal_raw['Rate'][i]
            minutes = self.basal_raw['Duration (minutes)'][i]

            # Add the activity of the basal to the insulin dictionary
            self.set_basel_activity(base_time, minutes, rate)

    # Calculation for basal rate of omnipod dash insulin pump
    def set_basel_activity(self, base_time, minutes, rate):
        """
        Calculate the timestamps for the basal rate of the omnipod dash insulin pump based on the basal rate, the time and the duration
        params: base_time: datetime object, the time of the basal rate; minutes: int, the duration of the basal rate in minutes; rate: float, the basal rate in U/h
        returns: time: normal list, the timestamps for the basal rate of 0.05 units
        """
        shots_per_hour = round(rate / enums.INSULIN_STEP_SIZE)
        shots = math.floor(shots_per_hour * (minutes / 60))
        interval_per_hour = 60 / shots_per_hour if shots_per_hour != 0 else 0

        # Create an array with the time of the shots in minutes below the hour
        time = [int((i % shots_per_hour) * interval_per_hour + interval_per_hour - 1) for i in range(0, int(shots))]

        # Add hours to the minutes
        time = [int(((i + 1) * interval_per_hour - 1)) for i in range(0, len(time))]

        # Remove the minutes from the basetime, round it down to the nearest hour and add the minutes back
        base_time_ref = base_time
        base_time_ref = base_time_ref.replace(minute=0, second=0, microsecond=0)

        # Add the base time to the time array
        time = [base_time_ref + pd.Timedelta(minutes=i) for i in time]

        # Filter the array to only include the times that are higher than the base time
        time = [i for i in time if i > base_time]

        # Loop through the time array and set the activity to 0.05
        for i in range(0, len(time)):
            self.set_bolus_activity(time[i], enums.INSULIN_STEP_SIZE, False)

    # Process the insulin data
    def process_insulin(self):
        """
        Process the insulin data by adding the activity of the bolus and basal to the insulin dictionary
        """
        self.process_bolus()
        self.process_basal()



# Class for CGM data
class CGMData:
    def __init__(self, temporal_data, cgm_raw):
        self.cgm = {}
        self.temporal_data = temporal_data
        self.cgm_raw = cgm_raw

    def process_cgm(self):
        """
        Add the activity of the bolus to the insulin dictionary by looping through the bolus data, starting at the end
        """
        # Loop through the cgm data, starting at the earliest in temporal data, to the latest time in temporal data and add the activity of the bolus to the cgm dictionary
        earliest = self.temporal_data.earliest
        latest = self.temporal_data.latest
        for i in range(0, len(self.cgm_raw['Tijdstempel apparaat'])):
            # Get the time and units of the bolus
            base_time = self.cgm_raw['Tijdstempel apparaat'][i]
            value = self.cgm_raw['Historische glucose mmol/l'][i]

            if earliest <= base_time <= latest:
                # If the time is not in the dictionary, add it
                if base_time not in self.cgm:
                    self.cgm[base_time] = value

                # If the time is in the dictionary, overwrite the value
                else:
                    self.cgm[base_time] = value


# Class for heart rate data
class HeartRateData:
    def __init__(self, temporal_data, heart_rate_raw):
        self.heart_rate = {}
        self.temporal_data = temporal_data
        self.heart_rate_raw = heart_rate_raw

    def process_heart_rate(self):
        """
        Add the activity of the bolus to the insulin dictionary by looping through the bolus data, starting at the end
        """
        # Loop through the heart rate data, starting at the earliest in temporal data, to the latest time in temporal data and add the activity of the bolus to the heart rate dictionary
        earliest = self.temporal_data.earliest
        latest = self.temporal_data.latest
        for i in range(0, len(self.heart_rate_raw['Timestamp'])):
            # Get the time and units of the bolus
            base_time = self.heart_rate_raw['Timestamp'][i]
            value = self.heart_rate_raw['heart rate'][i]

            if earliest <= base_time <= latest:
                # If the time is not in the dictionary, add it
                if base_time not in self.heart_rate:
                    self.heart_rate[base_time] = value

                # If the time is in the dictionary, overwrite the value
                else:
                    self.heart_rate[base_time] = value


# Class for xdrip data
class XdripData:
    def __init__(self, temporal_data, xdrip_raw):
        self.xdrip = {}
        self.temporal_data = temporal_data
        self.xdrip_raw = xdrip_raw

    def process_xdrip(self):
        """
        Add the activity of the bolus to the insulin dictionary by looping through the bolus data, starting at the end
        """
        # Loop through the xdrip data, starting at the earliest in temporal data, to the latest time in temporal data and add the activity of the bolus to the xdrip dictionary
        earliest = self.temporal_data.earliest
        latest = self.temporal_data.latest
        for i in range(0, len(self.xdrip_raw['Tijdstempel apparaat'])):
            # Get the time and units of the bolus
            base_time = self.xdrip_raw['Tijdstempel apparaat'][i]
            value = self.xdrip_raw['Historische glucose mmol/l'][i]

            if earliest <= base_time <= latest:
                # If the time is not in the dictionary, add it
                if base_time not in self.xdrip:
                    self.xdrip[base_time] = value

                # If the time is in the dictionary, overwrite the value
                else:
                    self.xdrip[base_time] = value



# to convert str to pandas._libs.tslibs.timestamps.Timestamp, use pd.to_datetime function for the columns heart rate and xdrip data column Timestamp

def process_data():
    # Read in the excel file
    xls = pd.read_excel(enums.DATA_PATH, sheet_name=['glucose_15', 'new_bolus', 'new_basal', 'heart_rate', 'xdrip'], engine='openpyxl')

    # Convert heart_rate: "Timestamp" column to pandas._libs.tslibs.timestamps.Timestamp and xdrip: "Tijdstempel apparaat"
    xls['heart_rate']['Timestamp'] = pd.to_datetime(xls['heart_rate']['Timestamp'])
    xls['xdrip']['Tijdstempel apparaat'] = pd.to_datetime(xls['xdrip']['Tijdstempel apparaat'])

    # Process the insulin data
    insulin_data = InsulinData(xls)
    insulin_data.temporal.process_temporal()
    insulin_data.process_insulin()

    # Process the cgm data, keeping only the data that is in in line with temporal data
    cgm_data = CGMData(insulin_data.temporal, xls['glucose_15'])
    cgm_data.process_cgm()

    # Process the heart reate data
    heart_rate_data = HeartRateData(insulin_data.temporal, xls['heart_rate'])
    heart_rate_data.process_heart_rate()

    # Process the xdrip data
    xdrip_data = XdripData(insulin_data.temporal, xls['xdrip'])
    xdrip_data.process_xdrip()

    # Write all data to a csv file to not have to run the code every time
    with open(enums.NEW_DATA_PATH, 'w',
              newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['time', 'insulin', 'bolus', 'basal', 'cgm', 'heart_rate', 'xdrip', 'units_raw'])

        # Loop through the times in temporal data and write the data to the csv file
        for time in insulin_data.temporal.x_axis:
            # If the time is in the insulin dictionary, write the insulin data to the csv file

            writer.writerow([time, insulin_data.insulin.get(time, ''),
                            insulin_data.bolus_insulin.get(time, ''),
                            insulin_data.basal_insulin.get(time, ''),
                            cgm_data.cgm.get(time, ''),
                            heart_rate_data.heart_rate.get(time, ''),
                            xdrip_data.xdrip.get(time, ''),
                            insulin_data.units_raw.get(time, '')
                            ])

process_data()
