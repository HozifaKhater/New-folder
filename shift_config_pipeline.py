import streamlit as st
from scripts.app_onfig import AppConfig
from scripts.file_manager import FileManager
from scripts.visualization import Visualization
from scripts.tabs_manager import TabsManager

def main():
    try:
        AppConfig.configure_app()
        data, uploaded_file_name = FileManager.handle_file_upload()
        if data is not None:
            if "Employees_Shifts_Percentage.csv" in uploaded_file_name:
                Visualization.render_employees_shifts_percentage(data)
            else:
                TabsManager.process_data_in_tabs(data)
    except Exception as e:
        st.error(f"An unexpected error occurred in the app: {e}")

if __name__ == "__main__":
    main()