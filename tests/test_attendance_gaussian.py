import unittest
from unittest.mock import patch
import pandas as pd
import numpy as np
from scripts.attendance_gaussian import AttendanceGaussian

class TestAttendanceGaussian(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.data = pd.DataFrame({
            "EmployeeId": [1, 1, 2, 2],
            "CheckInTime": ["08:15:00", "09:30:00", "07:45:00", "08:00:00"],
            "CheckOutTime": ["17:15:00", "18:00:00", "16:30:00", "16:45:00"]
        })
        self.gaussian = AttendanceGaussian(self.data)

    def test_prepare_data(self):
        # Test if data preparation is successful
        self.gaussian.prepare_data()
 
    def test_expand_checkin_data(self):
        # Test if check-in data is expanded correctly
        self.gaussian.prepare_data()
        self.gaussian.expand_checkin_data()
        self.assertTrue(isinstance(self.gaussian.expanded_data, np.ndarray))
        self.assertGreater(len(self.gaussian.expanded_data), 0)

    def test_expand_checkout_data(self):
        # Test if check-out data is expanded correctly
        self.gaussian.prepare_data()
        self.gaussian.expand_checkout_data()
        self.assertTrue(isinstance(self.gaussian.expanded_checkout_data, np.ndarray))
        self.assertGreater(len(self.gaussian.expanded_checkout_data), 0)

    def test_expand_checkin_quarter_data(self):
        # Test if check-in quarter data is expanded correctly
        self.gaussian.prepare_data()
        self.gaussian.expand_checkin_quarter_data()
        self.assertTrue(isinstance(self.gaussian.expanded_checkin_quarter_data, np.ndarray))
        self.assertGreater(len(self.gaussian.expanded_checkin_quarter_data), 0)

    def test_expand_checkout_quarter_data(self):
        # Test if check-out quarter data is expanded correctly
        self.gaussian.prepare_data()
        self.gaussian.expand_checkout_quarter_data()
        self.assertTrue(isinstance(self.gaussian.expanded_checkout_quarter_data, np.ndarray))
        self.assertGreater(len(self.gaussian.expanded_checkout_quarter_data), 0)

    def test_fit_gaussian(self):
        # Test if Gaussian fitting works for expanded data
        self.gaussian.prepare_data()
        self.gaussian.expand_checkin_data()
        self.gaussian.expand_checkout_data()
        self.gaussian.fit_gaussian()
        self.assertIsNotNone(self.gaussian.mu)
        self.assertIsNotNone(self.gaussian.std)
        self.assertIsNotNone(self.gaussian.mu_checkout)
        self.assertIsNotNone(self.gaussian.std_checkout)

    @patch('streamlit.pyplot')
    def test_plot_checkin_histogram(self, mock_pyplot):
        # Test if plotting check-in histogram calls Streamlit's pyplot
        self.gaussian.prepare_data()
        self.gaussian.expand_checkin_data()
        self.gaussian.fit_gaussian()
        self.gaussian.plot_checkin_histogram()
        mock_pyplot.assert_called_once()

    @patch('streamlit.pyplot')
    def test_plot_check_in_out_histogram(self, mock_pyplot):
        # Test if plotting combined check-in and check-out histogram calls Streamlit's pyplot
        self.gaussian.prepare_data()
        self.gaussian.expand_checkin_data()
        self.gaussian.expand_checkout_data()
        self.gaussian.fit_gaussian()
        self.gaussian.plot_check_in_out_histogram()
        mock_pyplot.assert_called_once()

    @patch('streamlit.pyplot')
    def test_plot_checkin_quarter_histogram(self, mock_pyplot):
        # Test if plotting check-in quarter histogram calls Streamlit's pyplot
        self.gaussian.prepare_data()
        self.gaussian.expand_checkin_quarter_data()
        self.gaussian.fit_gaussian()
        self.gaussian.plot_checkin_quarter_histogram()
        mock_pyplot.assert_called_once()

    @patch('streamlit.pyplot')
    def test_plot_checkout_quarter_histogram(self, mock_pyplot):
        # Test if plotting check-out quarter histogram calls Streamlit's pyplot
        self.gaussian.prepare_data()
        self.gaussian.expand_checkout_quarter_data()
        self.gaussian.fit_gaussian()
        self.gaussian.plot_checkout_quarter_histogram()
        mock_pyplot.assert_called_once()

if __name__ == "__main__":
    unittest.main()

