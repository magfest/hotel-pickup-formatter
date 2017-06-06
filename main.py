import os

from meeting_space_times import *
from preprocessor import preprocess_raw_meeting_times_text

# example row:
# {'Function Space': 'Maryland Ballroom', 'Date': '2/18/2016', 'Start Time': '1:00 AM', 'End Time': '11:45 PM'}

# -----------------------------------------------------------------
# PREPROCESSOR STAGE (crappy PDF ocr'd exports to respectable CSV)
# -----------------------------------------------------------------

input_raw = 'data/gaylord-2020-rawtimes.txt'
output_csv_filename = 'data/gaylord-magfest2020-times-raw-generated.csv'

preprocess_raw_meeting_times_text(input_raw, output_csv_filename)


# -----------------------------------------------------------------
# REAL PIPELINE
# -----------------------------------------------------------------

# if using the preprocessor, uncomment this
input_csv = output_csv_filename

# if not using the preprocessor, uncomment one of these
# input_csv = 'data/gaylord-magfest2018-times.csv'

meeting_space = MeetingSpaceTimes()
# meeting_space.read_meeting_space_names_from("names/markcenter-names.txt")
meeting_space.read_meeting_space_names_from("names/gaylord-names.txt")
meeting_space.read_from(input_csv)

output_csv = "c:/tmp/tmpout.csv"
output_html = "c:/tmp/tmpout.html"
meeting_space.output_csv(output_csv)

os.system('c:\Python34\python.exe csv2html.py ' + output_csv + ' ' + output_html)
os.system("start " + output_html) # dont put any spaces/weird stuff in filename
