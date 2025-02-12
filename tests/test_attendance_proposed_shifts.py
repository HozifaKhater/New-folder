import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from scripts.attendance_proposed_shifts import AttendanceProposedShifts

class TestAttendanceProposedShifts(unittest.TestCase):

    def setUp(self):
        # Sample DataFrame for testing
        self.df = pd.DataFrame({
            "EmployeeId": [1, 2, 3],
            "CheckInTime": ["08:15:00", "09:45:00", "07:30:00"],
            "CheckOutTime": ["17:15:00", "18:00:00", "16:00:00"]
        })
        self.shifts = AttendanceProposedShifts(self.df)

    def test_process_data(self):
        # Test if process_data correctly creates CheckInHour and CheckOutHour columns
        self.shifts.process_data()
        self.assertIn("CheckInHour", self.shifts.df.columns)
        self.assertIn("CheckOutHour", self.shifts.df.columns)
        self.assertIn("CheckInQHour", self.shifts.df.columns)
        self.assertIn("CheckOutQHour", self.shifts.df.columns)

    def test_create_pivot(self):
        # Test if create_pivot correctly creates pivot tables
        self.shifts.process_data()
        self.shifts.create_pivot()
        
        self.assertIsNotNone(self.shifts.pivot_data)
        self.assertIsNotNone(self.shifts.pivot_data_quarter)
        self.assertTrue(isinstance(self.shifts.pivot_data, pd.DataFrame))
        self.assertTrue(isinstance(self.shifts.pivot_data_quarter, pd.DataFrame))

    def test_define_shifts(self):
        # Test if define_shifts creates the shifts DataFrame
        self.shifts.process_data()
        self.shifts.create_pivot()
        self.shifts.define_shifts()
        
        self.assertTrue(hasattr(self.shifts, 'shifts'))
        self.assertTrue(hasattr(self.shifts, 'shifts_quarter'))
        self.assertTrue(isinstance(self.shifts.shifts, pd.DataFrame))
        self.assertTrue(isinstance(self.shifts.shifts_quarter, pd.DataFrame))

    @patch('streamlit.pyplot')
    def test_plot_shifts(self, mock_pyplot):
        # Test if plot_shifts calls Streamlit's pyplot function
        self.shifts.process_data()
        self.shifts.create_pivot()
        self.shifts.define_shifts()
        
        self.shifts.plot_shifts()
        mock_pyplot.assert_called_once()

    @patch('streamlit.pyplot')
    def test_plot_shifts_quarter(self, mock_pyplot):
        # Test if plot_shifts_quarter calls Streamlit's pyplot function
        self.shifts.process_data()
        self.shifts.create_pivot()
        self.shifts.define_shifts()
        
        self.shifts.plot_shifts_quarter()
        mock_pyplot.assert_called_once()

    @patch('streamlit.pyplot')
    def test_plot_heatmap(self, mock_pyplot):
        # Test if plot_heatmap calls Streamlit's pyplot function
        self.shifts.process_data()
        self.shifts.create_pivot()
        
        self.shifts.plot_heatmap()
        mock_pyplot.assert_called_once()

    @patch('streamlit.pyplot')
    def test_plot_quarter_heatmap(self, mock_pyplot):
        # Test if plot_quarter_heatmap calls Streamlit's pyplot function
        self.shifts.process_data()
        self.shifts.create_pivot()
        
        self.shifts.plot_quarter_heatmap()
        mock_pyplot.assert_called_once()

    @patch('streamlit.pyplot')
    def test_plot_heatmap_shifts_quarter(self, mock_pyplot):
        # Test if plot_heatmap_shifts_quarter calls Streamlit's pyplot function
        self.shifts.process_data()
        self.shifts.create_pivot()
        self.shifts.define_shifts()
        
        self.shifts.plot_heatmap_shifts_quarter()
        mock_pyplot.assert_called_once()

if __name__ == "__main__":
    unittest.main()
