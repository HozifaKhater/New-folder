import unittest
import pandas as pd
from scripts.attendance_data_processor import AttendanceDataProcessor

class TestAttendanceDataProcessor(unittest.TestCase):

    def setUp(self):
        # Sample DataFrame for testing
        self.data = pd.DataFrame({
            'EmployeeId': [1, 1, 1, 2, 2],
            'TransDateTime': [
                '2023-10-01 08:00:00.000',
                '2023-10-01 17:00:00.000',
                '2023-10-02 09:00:00.000',
                '2023-10-01 08:30:00.000',
                '2023-10-01 16:30:00.000'
            ],
            'Type': ['attend', 'leave', 'attend', 'attend', 'leave']
        })
        self.processor = AttendanceDataProcessor(self.data)

    def test_preprocess_data(self):
        # Test if preprocess_data correctly converts data and filters on 'attend' and 'leave'
        self.processor.preprocess_data()
        self.assertIn("Transdate", self.processor.cleaned_data.columns)
        self.assertIn("Transtime", self.processor.cleaned_data.columns)
        self.assertTrue(all(self.processor.cleaned_data['Type'].isin(['attend', 'leave'])))

    def test_filter_transactions(self):
        # Test if filter_transactions correctly removes single transactions
        self.processor.preprocess_data()
        self.processor.filter_transactions()

        # Check that transactions are filtered correctly
        unique_counts = self.processor.cleaned_data.groupby(['EmployeeId', self.processor.cleaned_data['TransDateTime'].dt.date]).size()
        for count in unique_counts:
            self.assertGreaterEqual(count, 2)  # Ensures that only paired transactions remain

    def test_aggregate_data(self):
        # Test if aggregate_data correctly calculates CheckInTime, CheckOutTime, and hours worked
        self.processor.preprocess_data()
        self.processor.filter_transactions()
        self.processor.aggregate_data()

        self.assertIsNotNone(self.processor.final_data)
        self.assertIn("CheckInTime", self.processor.final_data.columns)
        self.assertIn("CheckOutTime", self.processor.final_data.columns)
        self.assertIn("hours", self.processor.final_data.columns)
        self.assertTrue(all(self.processor.final_data['hours'] >= 0.5))

if __name__ == "__main__":
    unittest.main()
