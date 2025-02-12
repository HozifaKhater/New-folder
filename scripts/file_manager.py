import streamlit as st
from scripts.file_uploader import FileUploader
from scripts.file_saver import FileSaver


class FileManager:
    @staticmethod
    def handle_file_upload():
        #Handle file upload and return uploaded data and file name.
        try:
            with st.sidebar:
                file_uploader = FileUploader()
                data, file_name = file_uploader.upload_file("Upload CSV", 1)
                if data is None:
                    st.warning("No file uploaded. Please upload a valid file.")
                return data, file_name
        except Exception as e:
            st.error(f"An error occurred while uploading the file: {e}")
            return None, None

def toggle_button_state(): #Toggle the session state for the button
    st.session_state['button'] = not st.session_state.get('button', False)
