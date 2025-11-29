import unittest
from user_input import check_date_validity

class TestCheckDateValidity(unittest.TestCase):

    def test_valid_date(self):
        self.assertTrue(check_date_validity("2025-11-29"))

    def test_invalid_format(self):
        self.assertFalse(check_date_validity("2025/11/29"))
        self.assertFalse(check_date_validity("2025-1-1"))
        self.assertFalse(check_date_validity("not-a-date"))

    def test_invalid_day(self):
        self.assertFalse(check_date_validity("2025-11-31"))

    def test_invalid_month(self):
        self.assertFalse(check_date_validity("2025-13-01"))

    def test_leap_year_valid(self):
        self.assertTrue(check_date_validity("2024-02-29"))

    def test_leap_year_invalid(self):
        self.assertFalse(check_date_validity("2023-02-29"))

if __name__ == "__main__":
    unittest.main()