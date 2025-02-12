import pandas as pd
import streamlit as st
from scripts.file_uploader import FileUploader

     
class UploadChosenShifts:
    def __init__(self):
        self.uploaded_file = None
        self.data = None
    
    def upload_shifts(self):
        try:
            with st.sidebar:
                file_shift_uploader = FileUploader()
                # Attempt to upload the file
                self.data, file_name = file_shift_uploader.upload_file("Upload the Chosen Shifts", 2)                
                # Check if data was uploaded successfully
                if self.data is not None:
                    if not file_shift_uploader.validate_shifts_columns():
                        st.error("Invalid file structure. Please ensure the uploaded file has the correct columns.")
                        return None
                else:
                    st.warning("No file uploaded. Please upload a file.")
        except FileNotFoundError as e:
            st.error(f"File not found: {e}")
            return None
        except ValueError as e:
            st.error(f"Value error: {e}")
            return None
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            return None
        
        return self.data
