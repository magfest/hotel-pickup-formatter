from reservation import *
import csv
import datetime
from datetime import timedelta

required_fieldnames = ['Function Space', 'Date', 'Start Time', 'End Time']


class MeetingSpaceTimes:
    def __init__(self):
        self.room_reservations = dict()
        self.earliest_seen_time = None
        self.latest_seen_time = None

    def read_meeting_space_names_from(self, input_file):
        f = open(input_file, 'rt')
        for function_space in f.readlines():
            self.add_function_space_if_not_exists(function_space.strip())

    def read_from(self, input_csv):
        f = open(input_csv, 'rt')

        reader = csv.DictReader(f)

        for field in required_fieldnames:
            if field not in reader.fieldnames:
                raise 'aborting: CSV doesn\'t contain a required field: ' + field

        for row in reader:
            function_space = row['Function Space']
            day = row['Date']                  # "1/22/16"
            start_time = row['Start Time']      # "5:00 PM"
            end_time = row['End Time']          # "7:00 PM"

            start_date = MeetingSpaceTimes.combine_date_time(start_time, day)
            end_date = MeetingSpaceTimes.combine_date_time(end_time, day)

            self.append_new_room_times(function_space, start_date, end_date)

    @staticmethod
    def combine_date_time(which_time, day):
        time_format = "%m/%d/%Y %I:%M %p"
        combined_date_time_str = day + " " + which_time
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

        if function_space == 'Prince George\'s Exhibit Hall BC':
            self.do_append_new_room_times('Prince George\'s Exhibit Hall B', start_date, end_date)
            self.do_append_new_room_times('Prince George\'s Exhibit Hall C', start_date, end_date)
            return

        if function_space == 'Prince George\'s Exhibit Hall CD':
            self.do_append_new_room_times('Prince George\'s Exhibit Hall C', start_date, end_date)
            self.do_append_new_room_times('Prince George\'s Exhibit Hall D', start_date, end_date)
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

        # no hacky stuff needed, do this one.
        self.do_append_new_room_times(function_space, start_date, end_date)

    def update_start_end_times(self, reservation):
        if self.earliest_seen_time is None or reservation.start_dt < self.earliest_seen_time:
            self.earliest_seen_time = reservation.start_dt

        if self.latest_seen_time is None or reservation.end_dt > self.latest_seen_time:
            self.latest_seen_time = reservation.end_dt

    def add_function_space_if_not_exists(self, function_space):
        if function_space not in self.room_reservations:
            self.room_reservations[function_space] = []

    def do_append_new_room_times(self, function_space, start_date, end_date):
        self.add_function_space_if_not_exists(function_space)

        new_reservation = RoomReservation(start_date, end_date)

        self.update_start_end_times(new_reservation)

        # attempt to combine our new reservation with any existing ones
        for existing_reservation in self.room_reservations[function_space]:
            if existing_reservation.extend_if_possible(new_reservation):
                return  # it worked, so bail out

        # couldn't combine with any existing registrations, so add this one in
        self.room_reservations[function_space].append(new_reservation)

    @staticmethod
    def is_day_month_year_same(day1, day2):
        return day1.day == day2.day and day1.month == day2.month and day1.year == day2.year

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
                        if self.is_day_month_year_same(reservation.start_dt, day):
                            cell_text = reservation.start_dt.strftime("%I:%M %p")
                            currently_in_a_block = True
                        elif self.is_day_month_year_same(reservation.end_dt, day):
                            cell_text = reservation.end_dt.strftime("%I:%M %p")
                            currently_in_a_block = False
                        else:
                            if currently_in_a_block:
                                cell_text = '*'
                            else:
                                cell_text = ' '

                    row.append(cell_text)

                writer.writerow(row)

    def output_csv_date_row(self, writer):
        dates = self.get_full_date_range()
        days = []
        for _date in dates:
            days.append(_date.strftime("%m/%d/%y"))

        writer.writerow([''] + days)

    # return a list of all the days between our earliest time seen and latest seen
    def get_full_date_range(self):
        days = []
        for x in range((self.latest_seen_time - self.earliest_seen_time).days + 1):
            days.append(self.earliest_seen_time + timedelta(days=x))

        return days