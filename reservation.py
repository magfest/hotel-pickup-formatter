hour_tolerance = 1.5   # number of hours away two dates can be to be the "same"


class RoomReservation:
    def __init__(self, start_dt=None, end_dt=None):
        self.start_dt = start_dt
        self.end_dt = end_dt

    # attempts to extend the room reservation using the given times
    # returns true if we could extend, false if we could not
    def extend_if_possible(self, reservation):
        if self._is_there_no_gap_between(self.end_dt, reservation.start_dt):
            self.end_dt = reservation.end_dt
            return True
        elif self._is_there_no_gap_between(reservation.end_dt, self.start_dt):
            self.start_dt = reservation.start_dt
            return True

        return False

    # use some fuzzy logic to figure out if a start_date and end_date are the "same"
    # i.e. only off by two hours or less, or similar.
    @staticmethod
    def _is_there_no_gap_between(date1, date2):
        seconds_tolerance = hour_tolerance * 60 * 60
        diff = date1 - date2
        return diff.total_seconds() < seconds_tolerance