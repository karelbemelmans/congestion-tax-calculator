from datetime import datetime
from calculator.vehicles import Vehicle
from collections import defaultdict
from functools import reduce


class CongestionTaxCalculator:

    def get_tax(self, vehicle: Vehicle, dates: list):
        """Returns the total toll fee for a vehicle on a list of dates."""

        # We need to sort the dates first to make sure our algorithm works correctly
        dates.sort()

        # We collect the fee per day in a dict
        total_fee = defaultdict(int)

        # Initial values for our loop
        start_date = dates[0]
        previous_date = dates[0]

        for date in dates:

            # We need to keep track of the total fee for each day, not the total
            # fee for all days, since our input can span over multiple days.
            day = date.strftime("%Y-%m-%d")

            # Calculate the fee for the current date
            next_fee = self.get_toll_fee(vehicle, date)
            temp_fee = self.get_toll_fee(vehicle, previous_date)

            minutes = (date.timestamp() - start_date.timestamp()) / 60

            if minutes <= 60:

                # If we already have a fee for this day, we need to subtract the previous fee.
                if total_fee[day] > 0:
                    total_fee[day] -= temp_fee

                # If the next fee is higher than the previous fee, we need to use the next fee instead.
                if next_fee >= temp_fee:
                    temp_fee = next_fee

                # Add the fee to the total fee for this day
                total_fee[day] += temp_fee

            # If there was more than 60 mintes between the previous date and the current date,
            # we simply add this fee to the rest of the fee for this day.
            else:
                total_fee[day] += next_fee
                start_date = date

            # Save the current date as the new previous one and iterate through the loop
            previous_date = date
            total_fee[day] = min(total_fee[day], 60)

        # The total fee for all the dates is the sum of the feeds for every day we encountered
        return reduce(lambda a, b: a+b, total_fee.values())

    def get_toll_fee(self, vehicle: Vehicle, date: datetime, ) -> int:
        """Returns the toll fee for a single date."""

        if self.is_toll_free_date(date):
            return 0

        if vehicle.is_toll_free_vehicle():
            return 0

        hour = date.hour
        minute = date.minute
        print(hour, minute)

        match hour:
            case 6:
                return 8 if 0 <= minute <= 29 else 13
            case 7:
                return 18
            case 8:
                return 13 if 0 <= minute <= 29 else 8
            case 9 | 10 | 11 | 12 | 13 | 14:
                return 8
            case 15:
                return 13 if 0 <= minute <= 29 else 18
            case 16:
                return 18
            case 17:
                return 13
            case 18:
                return 8 if 0 <= minute <= 29 else 0
            case _:
                return 0

    def is_toll_free_date(self, date: datetime):
        """Returns true if the date is a toll-free date, false otherwise."""

        year = date.year
        month = date.month
        day = date.day

        if not year == 2013:
            return False

        # Saturday and Sunday
        if date.weekday() == 5 or date.weekday() == 6:
            return True

        # A manual list of public holidays + the day before a public holiday
        toll_free_days = {
            1: [1],
            3: [28, 29],
            4: [1, 30],
            5: [1, 8, 9],
            6: [5, 6, 21],
            7: list(range(1, 32)),  # All days in July are toll-free
            11: [1],
            12: [24, 25, 26, 31]
        }

        return month in toll_free_days and day in toll_free_days[month]
