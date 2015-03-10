from unittest import TestCase

from meeting_space_times import *

__author__ = 'Dom'


class TestMeetingSpaceTimes(TestCase):
    def test_append_new_room_times(self):

        t = MeetingSpaceTimes()


        function_space = "bigass ballroom"
        start_date1 = t.combine_date_time("1:00 PM", "2/1/2016")
        end_date1 = t.combine_date_time("4:00 PM", "2/2/2016")

        t.append_new_room_times(function_space, start_date1, end_date1)

        self.assertEqual(1, len(t.room_reservations))
        self.assertEqual(1, len(t.room_reservations["bigass ballroom"]))


        start_date2 = t.combine_date_time("5:00 PM", "2/2/2016")
        end_date2 = t.combine_date_time("4:00 PM", "2/3/2016")

        t.append_new_room_times(function_space, start_date2, end_date2)

        self.assertEqual(1, len(t.room_reservations))
        self.assertEqual(1, len(t.room_reservations["bigass ballroom"]))

        self.assertEqual(t.room_reservations["bigass ballroom"][0].start_dt, start_date1)
        self.assertEqual(t.room_reservations["bigass ballroom"][0].end_dt, end_date2)


        start_date3 = t.combine_date_time("5:00 PM", "1/31/2016")
        end_date3 = t.combine_date_time("12:00 PM", "2/1/2016")

        t.append_new_room_times(function_space, start_date3, end_date3)

        self.assertEqual(1, len(t.room_reservations))
        self.assertEqual(1, len(t.room_reservations["bigass ballroom"]))

        self.assertEqual(t.room_reservations["bigass ballroom"][0].start_dt, start_date3)
        self.assertEqual(t.room_reservations["bigass ballroom"][0].end_dt, end_date2)


    def test_hacky_name_recognition_junk(self):
        t = MeetingSpaceTimes()

        function_space1 = "Prince George\'s Exhibit Hall ABCD"
        start_date1 = t.combine_date_time("1:00 AM", "2/2/2016")
        end_date1 = t.combine_date_time("11:45 PM", "2/2/2016")

        t.append_new_room_times(function_space1, start_date1, end_date1)

        required_function_spaces = ["Prince George\'s Exhibit Hall A",
                                    "Prince George\'s Exhibit Hall B",
                                    "Prince George\'s Exhibit Hall C",
                                    "Prince George\'s Exhibit Hall D"]

        self.assertEqual(4, len(t.room_reservations))

        for required_function_space in required_function_spaces:
            self.assertIn(required_function_space, t.room_reservations)
            self.assertEqual(1, len(t.room_reservations[required_function_space]))
            self.assertEqual(t.room_reservations[required_function_space][0].start_dt, start_date1)
            self.assertEqual(t.room_reservations[required_function_space][0].end_dt, end_date1)

        function_space2 = "Prince George\'s Exhibit Hall C"
        start_date2 = t.combine_date_time("1:00 AM", "2/3/2016")
        end_date2 = t.combine_date_time("4:00 PM", "2/3/2016")

        t.append_new_room_times(function_space2, start_date2, end_date2)

        self.assertEqual(4, len(t.room_reservations))
        self.assertEqual(1, len(t.room_reservations[function_space2]))

        self.assertEqual(t.room_reservations[function_space2][0].start_dt, start_date1, "start date is wrong")
        self.assertEqual(t.room_reservations[function_space2][0].end_dt, end_date2, "end date is wrong")