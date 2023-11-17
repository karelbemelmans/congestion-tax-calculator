import unittest
from datetime import datetime
from calculator import CongestionTaxCalculator, Car, Motorbike


class TestCongestionTaxCalculator(unittest.TestCase):

    def setUp(self):
        self.CongestionTaxCalculator = CongestionTaxCalculator()

    # Passes with vehicle that should not pay toll
    def test_case_toll_free_vehicle(self):
        self._run_test_case(Motorbike, ["2013-01-14 21:00:00"], 0)

    def test_saturday_is_free(self):
        self._run_test_case(Car, ["2013-04-13 13:30:00"], 0)

    def test_sunday_is_free(self):
        self._run_test_case(Car, ["2013-04-13 13:30:00"], 0)

    def test_christmas_day_is_free(self):
        self._run_test_case(Car, ["2013-12-25 13:30:00"], 0)

    def test_a_day_in_july(self):
        self._run_test_case(Car, ["2013-07-07 13:30:00"], 0)

    def test_two_passages_within_60_minutes(self):
        self._run_test_case(
            Car, [
                "2013-02-08 14:35:00",  # 8sek
                "2013-02-08 15:29:00"   # 13sek
            ], 13)

    def test_three_passages_within_60_minutes(self):
        self._run_test_case(
            Car, [
                "2013-02-08 15:29:00",  # 13sek
                "2013-02-08 15:47:00",  # 18sek
                "2013-02-08 16:01:00"   # 18sek
            ], 18)

    def test_two_passages_further_than_60_minutes(self):
        self._run_test_case(
            Car, [
                "2013-02-08 06:23:00",  # 8sek
                "2013-02-08 15:27:00"   # 13sek
            ], 8 + 13)

    # Passes with a single date, give an easy to calculate score
    def test_case_single_passes(self):
        self._run_test_case(Car, ["2013-01-14 21:00:00"], 0)
        self._run_test_case(Car, ["2013-01-15 21:00:00"], 0)
        self._run_test_case(Car, ["2013-02-07 05:00:00"], 0)
        self._run_test_case(Car, ["2013-02-07 06:01:00"], 8)
        self._run_test_case(Car, ["2013-02-07 06:23:27"], 8)
        self._run_test_case(Car, ["2013-02-07 06:31:00"], 13)
        self._run_test_case(Car, ["2013-02-07 13:15:00"], 8)
        self._run_test_case(Car, ["2013-02-07 15:15:00"], 13)
        self._run_test_case(Car, ["2013-02-07 15:27:00"], 13)
        self._run_test_case(Car, ["2013-02-07 18:01:00"], 8)
        self._run_test_case(Car, ["2013-02-08 06:20:27"], 8)
        self._run_test_case(Car, ["2013-02-08 06:27:00"], 8)
        self._run_test_case(Car, ["2013-02-08 14:25:00"], 8)
        self._run_test_case(Car, ["2013-02-08 14:35:00"], 8)
        self._run_test_case(Car, ["2013-02-08 15:29:00"], 13)
        self._run_test_case(Car, ["2013-02-08 15:47:00"], 18)
        self._run_test_case(Car, ["2013-02-08 16:01:00"], 18)
        self._run_test_case(Car, ["2013-02-08 16:48:00"], 18)
        self._run_test_case(Car, ["2013-02-08 17:49:00"], 13)
        self._run_test_case(Car, ["2013-02-08 18:29:00"], 8)
        self._run_test_case(Car, ["2013-02-08 18:35:00"], 0)
        self._run_test_case(Car, ["2013-03-28 14:07:27"], 0)

    def test_maximum_tax_is_60_per_day(self):
        self._run_test_case(
            Car, [
                "2013-02-08 06:27:00",  # Friday - 8
                "2013-02-08 07:37:00",  # Friday - 18
                "2013-02-08 08:47:00",  # Friday - 8
                "2013-02-08 09:57:00",  # Friday - 8
                "2013-02-08 11:07:00",  # Friday - 8
                "2013-02-08 12:17:00",  # Friday - 8
                "2013-02-08 13:27:00",  # Friday - 8
                "2013-02-08 14:37:00",  # Friday - 8
                "2013-02-08 15:47:00",  # Friday - 18
                "2013-02-08 16:57:00",  # Friday - 18
                "2013-02-08 18:07:00"   # Friday - 8
            ], 60)

    # Ole's example that should not be 0
    def test_cars_arent_free_to_pass(self):
        self._run_test_case(Car, ["2013-02-08 09:01:00",
                                  "2013-02-08 10:02:00",
                                  "2013-02-08 11:03:00",
                                  "2013-02-08 12:04:00",
                                  "2013-02-08 14:05:00"], 40)

    # Internal helper method that converts our string input to datetime objects
    def _run_test_case(self, vehicle, dates, expected):
        result = self.CongestionTaxCalculator.get_tax(
            vehicle,  [datetime.strptime(str, "%Y-%m-%d %H:%M:%S") for str in dates])
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
