"""
add preprocessor to take text that looks like this from Gaylord PDFs:

12/29/18 Sat 1:00AM 11:45 PM Set Up Prince George's Exhibit Hall D

and transform it to text that looks like this ready for our CSV input:

Date,Day,Start Time,End Time,Status,Function Space
12/29/18,Sat,1:00 AM,11:45 PM,Set Up,Prince George's Exhibit Hall D

Then, we'll pass the CSV data on to the next stage of the pipeline
"""

import csv

_allowed_room_statuses = ['setup', 'set up', '24hour hold', '24 hour hold', '24 hourhold', '24 hour-hold']
_allowed_days = ['sat', 'sun', 'mon', 'tues', 'tue', 'wed', 'thu', 'thurs', 'fri']
_allowed_time_postfixes = ['AM', 'PM']


# gaylord data has this, mark center doesn't
has_start_day = False
has_room_status = False


def preprocess_raw_meeting_times_text(input_filename, outfile_name):
    # cheap hack
    assert '.csv' in outfile_name
    assert '.txt' in input_filename

    out_data = []

    f = open(input_filename, 'rt')
    for line in f.readlines():
        line_data_out = process_line(line)
        if line_data_out:
            out_data.append(line_data_out)

    with open(outfile_name, 'w') as csvfile:
        out_csv = csv.writer(csvfile)

        if has_start_day:
            out_csv.writerow(['Date','Day','Start Time','End Time','Status','Function Space'])
        else:
            out_csv.writerow(['Date', 'Start Time', 'End Time', 'Status', 'Function Space'])

        for row in out_data:
            out_csv.writerow(row)


def process_line(line):
    if not line or not len(line) or line[0] is '\n':
        return None

    remainder = line

    # ----
    date = remainder.split(' ', 1)[0]

    remainder = remainder.split(' ', 1)[1]

    # ----
    if has_start_day:
        start_day = remainder.split(' ', 1)[0]
        assert start_day.lower() in _allowed_days

        remainder = remainder.split(' ', 1)[1]

    # ----
    tmp = process_time_with_postfix(remainder)
    start_time, remainder = tmp[0], tmp[1]

    # ----
    tmp = process_time_with_postfix(remainder)
    end_time, remainder = tmp[0], tmp[1]

    # ----
    if not has_room_status:
        room_status = None
    else:
        tmp = match_room_status(remainder)
        assert tmp and "Couldn't match valid room status"
        room_status, remainder = tmp[0], tmp[1]

    # ----
    room_name = remainder.strip().replace('\n', '')

    # there's a more elegant way to do this but HAXXX
    if has_start_day:
        return [date, start_day, start_time, end_time, room_status, room_name]
    else:
        return [date,            start_time, end_time, room_status, room_name]


def match_room_status(remainder):
    for status in _allowed_room_statuses:
        if remainder.lower().startswith(status):
            remainder = remainder[len(status):]
            return [status, remainder]

    return None


def process_time_with_postfix(remainder):
    # third is time, which is either like "11:00 AM" or no space like "11:00AM"
    # normalize this to always have a space, so end result is like "11:00 AM"
    time = remainder.split(' ', 1)[0]
    remainder = remainder.split(' ', 1)[1]

    found_postfix = False
    for postfix in _allowed_time_postfixes:
        if postfix in time:
            found_postfix = True
            break

    if not found_postfix:
        postfix = remainder.split(' ', 1)[0]
        assert postfix in _allowed_time_postfixes

        time += " " + postfix

        remainder = remainder.split(' ', 1)[1]
    else:
        # add a space back to make "11:00AM" be "11:00 AM"
        beginning_time = time[:-2]
        end_postfix = time[-2:]
        assert end_postfix in _allowed_time_postfixes

        time = beginning_time + " " + postfix

    return [time, remainder]





