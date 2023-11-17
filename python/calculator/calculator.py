from datetime import datetime
from enum import Enum
from calculator.vehicles import Vehicle


class CongestionTaxCalculator:

    # Calculate the total tax for a single vehicle in a list of dates
    # We expect the dates to be sorted before passing into this function
    def get_tax(self, vehicle: Vehicle, dates: list):

        interval_start = dates[0]
        total_fee = 0

        for date in dates:
            print("date checked:", date)
            next_fee = self.get_toll_fee(vehicle, date)
            temp_fee = self.get_toll_fee(vehicle, interval_start)

            diff_in_seconds = date.timestamp() - interval_start.timestamp()
            minutes = diff_in_seconds / 60

            if minutes <= 60:
                if total_fee > 0:
                    total_fee = total_fee - temp_fee
                if next_fee >= temp_fee:
                    temp_fee = next_fee
                total_fee = total_fee + temp_fee
            else:
                total_fee = total_fee + next_fee

        # We can never pay more than 60kr per day
        print("FEE:", total_fee)
        return total_fee

    # Comment
    def is_toll_free_vehicle(self, vehicle: Vehicle) -> bool:
        if vehicle == None:
            return False

        vehicle_type = vehicle.get_vehicle_type(vehicle)
        return vehicle_type in [toll_free_vehicle.name.capitalize() for toll_free_vehicle in TollFreeVehicles]

    # Comment
    def get_toll_fee(self, vehicle: Vehicle, date: datetime, ) -> int:
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
        year = date.year
        month = date.month
        day = date.day

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

        if year == 2013:
            if month in toll_free_days and day in toll_free_days[month]:
                return True
        return False
