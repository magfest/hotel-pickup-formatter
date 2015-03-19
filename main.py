import sys

from reservation import *
from meeting_space_times import *

# example row:
# {'Function Space': 'Maryland Ballroom', 'Date': '2/18/2016', 'Start Time': '1:00 AM', 'End Time': '11:45 PM'}


meeting_space = MeetingSpaceTimes()

input_csv = 'C:\\Users\\Dom\\Downloads\\gaylord proposed feb 2016 dates.csv'
# input_csv = "c:/tmp/test-input.csv"
meeting_space.read_meeting_space_names_from("gaylord-names.txt")
meeting_space.read_from(input_csv)
meeting_space.output_csv("c:/tmp/tmpout.csv")