import unittest
from unittest.mock import patch
import pandas as pd
from scripts.file_saver import FileSaver
from io import StringIO

class TestFileSaver(unittest.TestCase):
    def setUp(self):
        # Create a sample DataFrame for testing
        data = {'Column1': [1, 2, 3], 'Column2': ['A', 'B', 'C']}
        self.df = pd.DataFrame(data)
        self.file_saver = FileSaver(self.df)

    @patch('streamlit.download_button')
    def test_download_button(self, mock_download_button):
        # Mocking streamlit.download_button
        mock_download_button.return_value = True  # Simulate button click

        # Call the method
        self.file_saver.download_button(button_label="Download CSV", filename="test_data.csv", key="test-key")

        # Check if the download_button was called with the correct arguments
        csv_output = self.file_saver.to_csv()
        mock_download_button.assert_called_once_with(
            "Download CSV",   # Button label
            csv_output,       # CSV content
            "test_data.csv",  # Filename
            "Shifts Data",    # MIME type
            key="test-key"    # Key
        )

if __name__ == '__main__':
    unittest.main()
