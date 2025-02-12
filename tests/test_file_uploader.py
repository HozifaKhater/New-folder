import pytest
import pandas as pd
from io import StringIO
from scripts.file_uploader import FileUploader

@pytest.fixture
def mock_attendance_csv():
    return StringIO(
        """EmployeeId,TransDateTime,Type
        101,2024-01-01 08:00:00,CheckIn
        102,2024-01-01 09:00:00,CheckIn
        103,2024-01-01 10:00:00,CheckIn
        """
    )

@pytest.fixture
def mock_shifts_csv():
    return StringIO(
        """Shift_Id,CheckInTime,CheckOutTime
        A,08:00,16:00
        B,09:00,17:00
        C,10:00,18:00
        """
    )

@pytest.fixture
def mock_assigned_shifts_csv():
    return StringIO(
        """EmployeeId,AssignedShift,TotalTransaction,Percentage
        101,A,5,50.0
        102,B,3,30.0
        103,C,2,20.0
        """
    )

@pytest.fixture
def file_uploader():
    return FileUploader()

def test_validate_attendance_columns(file_uploader, mock_attendance_csv):
    file_uploader.uploaded_file = mock_attendance_csv
    file_uploader.data = pd.read_csv(mock_attendance_csv)
    assert file_uploader.validate_attendance_columns() is True

def test_validate_shifts_columns(file_uploader, mock_shifts_csv):
    file_uploader.uploaded_file = mock_shifts_csv
    file_uploader.data = pd.read_csv(mock_shifts_csv)
    assert file_uploader.validate_shifts_columns() is True

def test_validate_assigned_shifts_columns(file_uploader, mock_assigned_shifts_csv):
    file_uploader.uploaded_file = mock_assigned_shifts_csv
    file_uploader.data = pd.read_csv(mock_assigned_shifts_csv)
    assert file_uploader.validate_assigned_shifts_columns() is True

def test_missing_columns(file_uploader, mock_shifts_csv):
    incomplete_csv = StringIO(
        """Shift_Id,CheckInTime
        A,08:00
        B,09:00
        """
    )
    file_uploader.uploaded_file = incomplete_csv
    file_uploader.data = pd.read_csv(incomplete_csv)
    assert file_uploader.validate_shifts_columns() is False
