import sys
import os

from reservation import *
from meeting_space_times import *

# example row:
# {'Function Space': 'Maryland Ballroom', 'Date': '2/18/2016', 'Start Time': '1:00 AM', 'End Time': '11:45 PM'}


meeting_space = MeetingSpaceTimes()

input_csv = 'markcenter-times.csv'
# input_csv = "c:/tmp/test-input.csv"
meeting_space.read_meeting_space_names_from("markcenter-names.txt")
meeting_space.read_from(input_csv)
output_csv = "c:/tmp/tmpout.csv"
output_html = "c:/tmp/tmpout.html"
meeting_space.output_csv(output_csv)

os.system('c:\Python34\python.exe csv2html.py ' + output_csv + ' ' + output_html)
os.system("start " + output_html) # dont put any spaces/weird stuff in filename