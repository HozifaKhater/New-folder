import pandas as pd
import streamlit as st

class FileUploader:
    def __init__(self):
        self.uploaded_file = None
        self.data = None
        self.file_name = None

    def upload_file(self,get_title,get_key):
        self.uploaded_file = st.file_uploader(get_title, type=["csv"], key=get_key)
        if self.uploaded_file is not None:
            self.data = pd.read_csv(self.uploaded_file, encoding='utf-8')
            self.file_name = self.uploaded_file.name
            return self.data, self.file_name
        return None, None

    def validate_attendance_columns(self):
        if self.data is not None:
            required_columns = ['EmployeeId', 'TransDateTime', 'Type']
            missing_columns = [col for col in required_columns if col not in self.data.columns]
            if missing_columns:
                st.error(f"Error: The following required columns are missing: {', '.join(missing_columns)}")
                return False
            return True
        return False
    def validate_shifts_columns(self):
        if self.data is not None:
            required_columns = ['Shift_Id', 'CheckInTime', 'CheckOutTime']
            missing_columns = [col for col in required_columns if col not in self.data.columns]
            if missing_columns:
                st.error(f"Error: The following required columns are missing: {', '.join(missing_columns)}")
                return False
            return True
        return False
    
    def validate_assigned_shifts_columns(self):
        if self.data is not None:
            required_columns = ['EmployeeId', 'AssignedShift', 'TotalTransaction','Percentage']
            missing_columns = [col for col in required_columns if col not in self.data.columns]
            if missing_columns:
                st.error(f"Error: The following required columns are missing: {', '.join(missing_columns)}")
                return False
            return True
        return False