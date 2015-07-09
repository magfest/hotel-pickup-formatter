hour_tolerance = 0.45   # number of hours away two dates can be to be the "same"


# a date comparison class that
class FuzzyDate:
    def __init__(self, _date):
        self.date = _date

    @staticmethod
    def _is_there_only_a_small_gap_between(date1, date2):
        seconds_tolerance = hour_tolerance * 60 * 60
        diff = date1 - date2
        num_seconds_diff = abs(diff.total_seconds())
        return num_seconds_diff  < seconds_tolerance

    def __lt__(self, other):
        return self.date < other.date or FuzzyDate._is_there_only_a_small_gap_between(self.date, other.date)

    def __le__(self, other):
        return self.date <= other.date or FuzzyDate._is_there_only_a_small_gap_between(self.date, other.date)

    def __eq__(self, other):
        return self.date == other.date or FuzzyDate._is_there_only_a_small_gap_between(self.date, other.date)

    def __ne__(self, other):
        return self.date != other.date and not FuzzyDate._is_there_only_a_small_gap_between(self.date, other.date)

    def __gt__(self, other):
        return self.date > other.date or FuzzyDate._is_there_only_a_small_gap_between(self.date, other.date)

    def __ge__(self, other):
        return self.date >= other.date or FuzzyDate._is_there_only_a_small_gap_between(self.date, other.date)


class RoomReservation:
    def __init__(self, start_dt=None, end_dt=None):
        self.start_dt = start_dt
        self.end_dt = end_dt

    # attempts to extend the room reservation using the given times
    # returns true if we could extend, false if we could not
    def extend_if_possible(self, reservation):        
        start_A = FuzzyDate(reservation.start_dt)
        end_A = FuzzyDate(reservation.end_dt)
        
        start_B = FuzzyDate(self.start_dt)
        end_B = FuzzyDate(self.end_dt)
        
        if start_B <= start_A and end_B >= start_A:
            self.end_dt = max(self.end_dt, reservation.end_dt)
            return True
        elif start_B >= start_A and start_B <= end_A:
            self.end_dt = max(self.end_dt, reservation.end_dt)
            self.start_dt = reservation.start_dt
            return True
     
        return False

    # use some fuzzy logic to figure out if a start_date and end_date are the "same"
    # i.e. only off by two hours or less, or similar.
    """@staticmethod
    def _is_there_no_gap_between(date1, date2):
        seconds_tolerance = hour_tolerance * 60 * 60
        diff = date1 - date2
        return diff.total_seconds() < seconds_tolerance

    def _fuzzy_equals(date1, date2, seconds_tolerance = hour_tolerance * 60 * 60):
        diff = date1 - date2
        return diff.total_seconds() < seconds_tolerance
            """