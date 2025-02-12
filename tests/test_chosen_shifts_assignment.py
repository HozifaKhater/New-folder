import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from scripts.chosen_shifts_assignment import ChosenShiftAssignment

@pytest.fixture
def mock_attendance_data():
    return pd.DataFrame({
        'EmployeeId': [1, 2, 3],
        'CheckInTime': ['08:00:00', '09:00:00', '10:00:00'],
        'CheckOutTime': ['16:00:00', '17:00:00', '18:00:00']
    })

@pytest.fixture
def mock_shifts():
    return pd.DataFrame({
        'Shift_Id': ['A', 'B', 'C'],
        'CheckInTime': ['08:00:00', '09:00:00', '10:00:00'],
        'CheckOutTime': ['16:00:00', '17:00:00', '18:00:00']
    })

@pytest.fixture
def chosen_shift_assignment(mock_attendance_data, mock_shifts):
    return ChosenShiftAssignment(mock_attendance_data, mock_shifts, n_clusters=3)

def test_time_to_minutes():
    assert ChosenShiftAssignment.time_to_minutes('08:30:00') == 510
    assert ChosenShiftAssignment.time_to_minutes('23:59:59') == 1439
    assert ChosenShiftAssignment.time_to_minutes(datetime(2024, 12, 1, 8, 30)) == 510

    with pytest.raises(ValueError):
        ChosenShiftAssignment.time_to_minutes('InvalidTimeString')

def test_minutes_to_time():
    assert ChosenShiftAssignment.minutes_to_time(510) == '08:30'
    assert ChosenShiftAssignment.minutes_to_time(1439) == '23:59'

def test_preprocess_data(chosen_shift_assignment):
    chosen_shift_assignment.preprocess_data()
    assert 'CheckInMinutes' in chosen_shift_assignment.attendance_data.columns
    assert 'CheckOutMinutes' in chosen_shift_assignment.attendance_data.columns
    assert 'StartMinutes' in chosen_shift_assignment.shifts.columns
    assert 'EndMinutes' in chosen_shift_assignment.shifts.columns

def test_apply_KNN(chosen_shift_assignment):
    chosen_shift_assignment.preprocess_data()
    assigned_shifts = chosen_shift_assignment.apply_KNN()
    assert 'AssignedShift' in chosen_shift_assignment.attendance_data.columns
    assert len(assigned_shifts) == len(chosen_shift_assignment.attendance_data)
def test_plot_scatter_KNN(chosen_shift_assignment):
    chosen_shift_assignment.preprocess_data()
    chosen_shift_assignment.apply_KNN()
    try:
        chosen_shift_assignment.plot_scatter_KNN()
    except Exception as e:
        pytest.fail(f"plot_scatter_KNN raised an exception: {e}")

def test_plot_assigned_shifts_for_all(chosen_shift_assignment):
    chosen_shift_assignment.preprocess_data()
    chosen_shift_assignment.apply_KNN()
    try:
        chosen_shift_assignment.plot_assigend_shifts_for_all()
    except Exception as e:
        pytest.fail(f"plot_assigend_shifts_for_all raised an exception: {e}")

def test_plot_assigned_shifts_for_all_sorted(chosen_shift_assignment):
    chosen_shift_assignment.preprocess_data()
    chosen_shift_assignment.apply_KNN()
    try:
        chosen_shift_assignment.plot_assigend_shifts_for_all_sorted()
    except Exception as e:
        pytest.fail(f"plot_assigned_shifts_for_all_sorted raised an exception: {e}")
