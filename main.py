import sys
import csv
import pprint
import datetime
import time
from datetime import date, timedelta

__author__ = 'Dom'

input_csv = 'C:\\Users\\Dom\\Downloads\\gaylord proposed feb 2016 dates.csv'

# example row:
# {'Function Space': 'Maryland Ballroom', 'Date': '2/18/2016', 'Start Time': '1:00 AM', 'End Time': '11:45 PM'}
required_fieldnames = ['Function Space', 'Date', 'Start Time', 'End Time']
hour_tolerance = 1.5   # number of hours away two dates can be to be the "same"

class RoomReservation:
    def __init__(self, start_dt = None, end_dt = None):
        self.start_dt = start_dt
        self.end_dt = end_dt

    # attempts to extend the room reservation using the given times
    # returns true if we could extend, false if we could not
    def extend_if_possible(self, start_date, end_date):

        if self._is_there_no_gap_between(self.end_dt, start_date):
            self.end_dt = end_date
            return True
        elif self._is_there_no_gap_between(end_date, self.start_dt):
            self.start_dt = start_date
            return True

        return False

    # use some fuzzy logic to figure out if a start_date are the "same"
    # i.e. only off by an hour or less, or similar.
    def _is_there_no_gap_between(self, date1, date2):
        seconds_tolerance = hour_tolerance * 60 * 60
        diff = date1 - date2
        return diff.total_seconds() < seconds_tolerance


class MeetingSpaceTimes:
    def __init__(self):
        self.room_reservations = dict()
        self.earliest_seen_time = None
        self.latest_seen_time = None

    def read_from(self, input_csv):
        f = open(input_csv, 'rt')

        reader = csv.DictReader(f)

        for field in required_fieldnames:
            if not field in reader.fieldnames:
                raise 'aborting: CSV doesn\'t contain a required field: ' + field

        for row in reader:
            function_space = row['Function Space']
            date = row['Date']                  # "1/22/16"
            start_time = row['Start Time']      # "5:00 PM"
            end_time = row['End Time']          # "7:00 PM"

            start_date = self.combine_date_time(start_time, date)
            end_date = self.combine_date_time(end_time, date)

            self.append_new_room_times(function_space, start_date, end_date)

    def combine_date_time(self, which_time, date):
        time_format = "%m/%d/%Y %I:%M %p"
        combined_date_time_str = date + " " + which_time
        return datetime.datetime.strptime(combined_date_time_str, time_format)

    def append_new_room_times(self, function_space, start_date, end_date):

        # do hacky bullshit with stupid data
        if function_space == 'Prince George\'s Exhibit Hall ABCD':
            self.do_append_new_room_times('Prince George\'s Exhibit Hall A', start_date, end_date)
            self.do_append_new_room_times('Prince George\'s Exhibit Hall B', start_date, end_date)
            self.do_append_new_room_times('Prince George\'s Exhibit Hall C', start_date, end_date)
            self.do_append_new_room_times('Prince George\'s Exhibit Hall D', start_date, end_date)
            return

        if function_space == 'Prince George\'s Prefunction AB':
            self.do_append_new_room_times('Prince George\'s Prefunction A', start_date, end_date)
            self.do_append_new_room_times('Prince George\'s Prefunction B', start_date, end_date)
            return

        if function_space == 'Prince George\'s Prefunction CD':
            self.do_append_new_room_times('Prince George\'s Prefunction C', start_date, end_date)
            self.do_append_new_room_times('Prince George\'s Prefunction D', start_date, end_date)
            return

        if function_space == 'Prince George\'s Exhibit Hall AB':
            self.do_append_new_room_times('Prince George\'s Exhibit Hall A', start_date, end_date)
            self.do_append_new_room_times('Prince George\'s Exhibit Hall B', start_date, end_date)
            return

        if function_space == 'Prince George\'s Exhibit Hall DE':
            self.do_append_new_room_times('Prince George\'s Exhibit Hall D', start_date, end_date)
            self.do_append_new_room_times('Prince George\'s Exhibit Hall E', start_date, end_date)
            return

        if function_space == 'Prince George\'s A-E Registration Desk':
            self.do_append_new_room_times('Prince George\'s A Registration Desk', start_date, end_date)
            self.do_append_new_room_times('Prince George\'s B Registration Desk', start_date, end_date)
            self.do_append_new_room_times('Prince George\'s C Registration Desk', start_date, end_date)
            self.do_append_new_room_times('Prince George\'s D Registration Desk', start_date, end_date)
            self.do_append_new_room_times('Prince George\'s E Registration Desk', start_date, end_date)
            return

        # no hacky stuff needed, do thsi one.
        self.do_append_new_room_times(function_space, start_date, end_date)

    def do_append_new_room_times(self, function_space, start_date, end_date):
        if self.earliest_seen_time == None or start_date < self.earliest_seen_time:
            self.earliest_seen_time = start_date

        if self.latest_seen_time == None or end_date > self.latest_seen_time:
            self.latest_seen_time = end_date

        if not function_space in self.room_reservations:
            self.room_reservations[function_space] = []

        for existing_reservation in self.room_reservations[function_space]:
            if existing_reservation.extend_if_possible(start_date, end_date):
                return

        new_reservation = RoomReservation(start_date, end_date)
        self.room_reservations[function_space].append(new_reservation)

    def output_csv(self, filename):
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile)

            self.output_csv_date_row(writer)

            for function_space, reservations in sorted(self.room_reservations.items()):
                row = [function_space]
                currently_in_a_block = False
                for day in self.get_full_date_range():
                    cell_text = ' '

                    # BUG: if a reservation starts and ends on the same day it wont output right.
                    for reservation in reservations:
                        if (reservation.start_dt - day).days is 0:
                            cell_text = reservation.start_dt.strftime("%I:%M %p")
                            currently_in_a_block = True
                        elif (reservation.end_dt - day).days is 0:
                            cell_text = reservation.end_dt.strftime("%I:%M %p")
                            currently_in_a_block = False
                        else:
                            if currently_in_a_block:
                                cell_text = '*'
                            else:
                                cell_text = ' '

                    row.append(cell_text)

                writer.writerow(row)




    def get_full_date_range(self):
        days = []
        for x in range((self.latest_seen_time - self.earliest_seen_time).days + 1):
            days.append(self.earliest_seen_time + timedelta(days=x))

        return days

    def output_csv_date_row(self, writer):
        dates = self.get_full_date_range()
        days = []
        for _date in dates:
            days.append(_date.strftime("%m/%d/%y"))

        writer.writerow([''] + days)


meeting_space = MeetingSpaceTimes()

meeting_space.read_from(input_csv)
meeting_space.output_csv("c:/tmp/tmpout.csv")
