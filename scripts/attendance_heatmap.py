import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import streamlit as st

# logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AttendanceHeatmap:
    def __init__(self, df):
        self.df = df
        self.employee_count_by_hour = None
        self.pivot_data = None

    def process_data(self):
        try:
            # Convert 'CheckInTime' and 'CheckOutTime' from HH:MM format to minutes since midnight
            # Convert CheckInTime and CheckOutTime to datetime and extract hour
            if 'CheckInTime' in self.df.columns and 'CheckOutTime' in self.df.columns:
                self.df['CheckInTime'] = pd.to_datetime(self.df['CheckInTime'], format='%H:%M:%S', errors='coerce')
                self.df['CheckOutTime'] = pd.to_datetime(self.df['CheckOutTime'], format='%H:%M:%S', errors='coerce')
                self.df['CheckInHour'] = self.df['CheckInTime'].dt.hour
                self.df['CheckOutHour'] = self.df['CheckOutTime'].dt.hour
            else:
                raise ValueError("DataFrame must contain 'CheckInTime' and 'CheckOutTime' columns.")
            # Group by CheckInHour and CheckOutHour
            self.employee_count_by_hour = self.df.groupby(['CheckInHour', 'CheckOutHour'])['EmployeeId'].nunique().reset_index()
            self.employee_count_by_hour.columns = ['CheckInHour', 'CheckOutHour', 'EmployeeCount']
            self.transaction_count_by_hour = self.df.groupby(['CheckInHour', 'CheckOutHour']).size().reset_index(name='TransactionCount')
            logging.info("Data processed successfully.")
        except Exception as e:
            logging.error(f"Error processing data: {e}")

    def create_pivot(self):
        #Create a pivot table from the grouped data
        try:
            self.pivot_data_employee = self.employee_count_by_hour.pivot(index='CheckInHour', columns='CheckOutHour', values='EmployeeCount')
            logging.info("Pivot table created successfully.")
        except Exception as e:
            logging.error(f"Error creating pivot table: {e}")

    def plot_heatmap(self):
        # Plot the heatmap for CheckInHour vs CheckOutHour.
        try:
            plt.figure(figsize=(16, 12))
            sns.heatmap(self.pivot_data_employee, annot=True, fmt='g', cmap='coolwarm')
            plt.title('CheckInHour - CheckOutHour with Employee Count')
            plt.xlabel('CheckOutHour')
            plt.ylabel('CheckInHour')
            st.pyplot(plt)
            plt.close()
            logging.info("Heatmap plotted successfully.")
        except Exception as e:
            logging.error(f"Error plotting heatmap: {e}")

