
import unittest
from unittest.mock import patch
import pandas as pd
from scripts.attendance_heatmap import AttendanceHeatmap

class TestAttendanceHeatmap(unittest.TestCase):

    def setUp(self):
        # Sample DataFrame for testing
        self.df = pd.DataFrame({
            "EmployeeId": [1, 2, 3],
            "CheckInTime": ["08:15:00", "09:45:00", "07:30:00"],
            "CheckOutTime": ["17:15:00", "18:00:00", "16:00:00"]
        })
        self.heatmap = AttendanceHeatmap(self.df)

    def test_process_data(self):
        # Test if process_data correctly creates CheckInHour and CheckOutHour columns
        self.heatmap.process_data()
        self.assertIn("CheckInHour", self.heatmap.df.columns)
        self.assertIn("CheckOutHour", self.heatmap.df.columns)
        #self.assertIsNotNone(self.heatmap.employee_count_by_hour)
        self.assertIsNotNone(self.heatmap.transaction_count_by_hour)
        self.assertEqual(self.heatmap.employee_count_by_hour.columns.tolist(), ['CheckInHour', 'CheckOutHour', 'EmployeeCount'])

    def test_create_pivot(self):
        # Test if create_pivot correctly generates the pivot table
        self.heatmap.process_data()
        self.heatmap.create_pivot()
        
        self.assertIsNotNone(self.heatmap.pivot_data_employee)
        self.assertTrue(isinstance(self.heatmap.pivot_data_employee, pd.DataFrame))
       # self.assertIn('EmployeeCount', self.heatmap.pivot_data_employee.columns)

    @patch('streamlit.pyplot')  # Mock Streamlit's pyplot function
    def test_plot_heatmap(self, mock_pyplot):
        # Test if plot_heatmap calls Streamlit's pyplot function
        self.heatmap.process_data()
        self.heatmap.create_pivot()
        
        self.heatmap.plot_heatmap()
        mock_pyplot.assert_called_once()

if __name__ == "__main__":
    unittest.main()
