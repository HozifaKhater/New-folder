import pytest
import pandas as pd
from io import StringIO
from unittest.mock import patch, MagicMock
from scripts.upload_chosen_shifts import UploadChosenShifts
from scripts.file_uploader import FileUploader

@pytest.fixture
def mock_valid_shifts_csv():
    return StringIO(
        """Shift_Id,CheckInTime,CheckOutTime
        A,08:00,16:00
        B,09:00,17:00
        C,10:00,18:00
        """
    )

@pytest.fixture
def mock_invalid_shifts_csv():
    return StringIO(
        """Shift_Id,StartTime,EndTime
        A,08:00,16:00
        B,09:00,17:00
        """
    )

@pytest.fixture
def upload_chosen_shifts():
    return UploadChosenShifts()

@patch("scripts.file_uploader.FileUploader.upload_file")
@patch("scripts.file_uploader.FileUploader.validate_shifts_columns")
def test_upload_shifts_valid(mock_validate_shifts_columns, mock_upload_file, upload_chosen_shifts, mock_valid_shifts_csv):
    mock_upload_file.return_value = (pd.read_csv(mock_valid_shifts_csv), "mock_valid_shifts.csv")
    mock_validate_shifts_columns.return_value = True

    with patch("streamlit.sidebar"):
        data = upload_chosen_shifts.upload_shifts()

    assert data is not None
    assert "Shift_Id" in data.columns
    assert "CheckInTime" in data.columns
    assert "CheckOutTime" in data.columns

@patch("scripts.file_uploader.FileUploader.upload_file")
@patch("scripts.file_uploader.FileUploader.validate_shifts_columns")
def test_upload_shifts_invalid(mock_validate_shifts_columns, mock_upload_file, upload_chosen_shifts, mock_invalid_shifts_csv):
    mock_upload_file.return_value = (pd.read_csv(mock_invalid_shifts_csv), "mock_invalid_shifts.csv")
    mock_validate_shifts_columns.return_value = False

    with patch("streamlit.sidebar") as mock_sidebar:
        mock_sidebar.return_value = None
        data = upload_chosen_shifts.upload_shifts()

    assert data is None

@patch("scripts.file_uploader.FileUploader.upload_file")
def test_no_file_uploaded(mock_upload_file, upload_chosen_shifts):
    mock_upload_file.return_value = (None, None)

    with patch("streamlit.sidebar") as mock_sidebar:
        mock_sidebar.return_value = None
        data = upload_chosen_shifts.upload_shifts()

    assert data is None
