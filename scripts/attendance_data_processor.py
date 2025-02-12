import pandas as pd
import logging 
import streamlit as st

# logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AttendanceDataProcessor:
    
    def __init__(self, data):
        self.data = data
        self.cleaned_data = None
        self.final_data = None    
        try:
            # Ensure EmployeeId is a string
            if self.data is not None:
                self.data['EmployeeId'] = self.data['EmployeeId'].astype(str)
                logging.info("EmployeeId column converted to string.")
            else:
                logging.warning("EmployeeId column is missing in the data.")
            # Ensure Type is a string
            if 'Type' in self.data.columns:
                self.data['Type'] = self.data['Type'].astype(str)
                logging.info("Type column converted to string.")
            else:
                logging.warning("Type column is missing in the data.")

        except Exception as e:
            logging.error(f"Error initializing data: {e}")

    def preprocess_data(self):
        try:
            if self.data is not None:
                 # Define the expected format
                 # Convert the TransDateTime column to datetime
                self.data['TransDateTime'] = pd.to_datetime(self.data['TransDateTime'], errors='coerce')
                # Check for rows where parsing failed
                invalid_rows = self.data[self.data['TransDateTime'].isna()]
                if not invalid_rows.empty:
                        st.error(f"Found invalid date-time rows:\n please make sure your date-time row has the format mm:dd:yyyy hh:mm:ss")
                self.data['TransDateTime'] = pd.to_datetime(self.data['TransDateTime'], format='%Y-%m-%d %H:%M:%S.%f')
                logging.info("TransDateTime conversion successful.")
                self.data['Transdate'] = self.data['TransDateTime'].dt.date
                self.data['Transtime'] = self.data['TransDateTime'].dt.time
                Data_to_Keep = ['EmployeeId', 'TransDateTime', 'Transdate', 'Transtime', 'Type']
                self.cleaned_data = self.data[Data_to_Keep].drop_duplicates()
                # remove absence and missing action type records and others
                self.cleaned_data['Type'] = self.cleaned_data['Type'].str.lower()
                self.cleaned_data = self.cleaned_data[self.cleaned_data['Type'].isin(['attend', 'leave'])]
                self.cleaned_data.dropna(inplace=True)
        except Exception as e:
            logging.error(f"Error in preprocessing data: {e}")

    def filter_transactions(self):
        try:
            if self.cleaned_data is not None:
                self.cleaned_data.sort_values(by=['EmployeeId', 'TransDateTime'], inplace=True)
                single_transactions = pd.DataFrame()
                def filter_transactions(group):
                    if len(group) == 1:
                        nonlocal single_transactions
                        single_transactions = pd.concat([single_transactions, group])
                        return None
                    first_attend = group[group['Type'] == 'attend'].head(1)
                    last_leave = group[group['Type'] == 'leave'].tail(1)
                    return pd.concat([first_attend, last_leave])
                self.cleaned_data = self.cleaned_data.groupby(['EmployeeId', self.cleaned_data['TransDateTime'].dt.date]).apply(filter_transactions).reset_index(drop=True)
                self.cleaned_data.dropna(subset=['TransDateTime'], inplace=True)
        except Exception as e:
            logging.error(f"Error in filtering transactions: {e}")
                    
    def aggregate_data(self):
        try:
            if self.cleaned_data is not None:
                self.cleaned_data['CheckInTime'] = self.cleaned_data.apply(lambda x: x['Transtime'] if x['Type'] == 'attend' else None, axis=1)
                self.cleaned_data['CheckOutTime'] = self.cleaned_data.apply(lambda x: x['Transtime'] if x['Type'] == 'leave' else None, axis=1)
                pivoted_data = self.cleaned_data.groupby(['EmployeeId', 'Transdate']).agg({
                    'CheckInTime': 'first',
                    'CheckOutTime': 'last'
                }).reset_index()
                pivoted_data['CheckInDateTime'] = pd.to_datetime(pivoted_data['Transdate'].astype(str) + ' ' + pivoted_data['CheckInTime'].astype(str), errors='coerce')
                pivoted_data['CheckOutDateTime'] = pd.to_datetime(pivoted_data['Transdate'].astype(str) + ' ' + pivoted_data['CheckOutTime'].astype(str), errors='coerce')

                pivoted_data.dropna(subset=['CheckInDateTime', 'CheckOutDateTime'], inplace=True)
                pivoted_data['hours'] = (pivoted_data['CheckOutDateTime'] - pivoted_data['CheckInDateTime']).dt.total_seconds() / 3600
                pivoted_data['DayOfWeek'] = self.cleaned_data['TransDateTime'].dt.dayofweek

                self.final_data = pivoted_data[['EmployeeId', 'Transdate', 'DayOfWeek', 'CheckInTime', 'CheckOutTime', 'hours']]
                self.final_data = self.final_data.copy()
                self.final_data['hours'] = pd.to_numeric(self.final_data['hours'], errors='coerce')
                self.final_data = self.final_data[(self.final_data['hours'] >= 0.5) & (self.final_data['hours'] > 0)].dropna(subset=['hours'])
        except Exception as e:
            logging.error(f"Error in aggregate data: {e}")

