import os

from meeting_space_times import *
from preprocessor import preprocess_raw_meeting_times_text, has_start_day

# example row:
# {'Function Space': 'Maryland Ballroom', 'Date': '2/18/2016', 'Start Time': '1:00 AM', 'End Time': '11:45 PM'}

# -----------------------------------------------------------------
# PREPROCESSOR STAGE (crappy PDF ocr'd exports to respectable CSV)
# -----------------------------------------------------------------

mode = "MarkCenter"

if mode == "MarkCenter":
    has_start_day = False
elif mode == "Gaylord":
    has_start_day = True

# input_raw = 'data/gaylord-2020-rawtimes.txt'
input_raw = 'data/markcenter-labs2.txt'
output_csv_filename = 'data/mark_center_labs2-generatedtimes.csv'

preprocess_raw_meeting_times_text(input_raw, output_csv_filename)

# if using the preprocessor, uncomment this
input_csv = output_csv_filename

# -----------------------------------------------------------------
# REAL PIPELINE
# -----------------------------------------------------------------

# if not using the preprocessor, uncomment one of these
# input_csv = 'data/markcenter-labs2.csv'

meeting_space = MeetingSpaceTimes()
meeting_space.read_meeting_space_names_from("names/markcenter-names.txt")
# meeting_space.read_meeting_space_names_from("names/gaylord-names.txt")
meeting_space.read_from(input_csv)

output_csv = "c:/tmp/tmpout.csv"
output_html = "c:/tmp/tmpout.html"
meeting_space.output_csv(output_csv)

os.system('c:\Python34\python.exe csv2html.py ' + output_csv + ' ' + output_html)
os.system("start " + output_html) # dont put any spaces/weird stuff in filename
