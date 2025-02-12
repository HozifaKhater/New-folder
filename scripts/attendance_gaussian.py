import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import streamlit as st
import logging

# logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AttendanceGaussian:
    def __init__(self, attendance_df):
        self.attendance_df = attendance_df
        self.expanded_data = None
        self.expanded_checkout_data = None
        self.expanded_checkin_quarter_data = None
        self.expanded_checkout_quarter_data = None
        self.mu = None
        self.std = None
        self.mu_checkout = None
        self.std_checkout = None
        self.mu_quarter = None
        self.std_quarter = None
        self.mu_checkout_quarter = None
        self.std_checkout_quarter = None
        try:
            self.prepare_data()
            logging.info("Data preparation successful.")
        except Exception as e:
            logging.error(f"Error preparing data: {e}")

    def prepare_data(self):     
        df = self.attendance_df.copy()     
        try:
            # Convert CheckInTime and CheckOutTime to datetime
            df['CheckInTime'] = pd.to_datetime(df['CheckInTime'], format='%H:%M:%S', errors='coerce')
            df['CheckOutTime'] = pd.to_datetime(df['CheckOutTime'], format='%H:%M:%S', errors='coerce')
            df['CheckInHour'] = df['CheckInTime'].dt.hour
            df['CheckOutHour'] = df['CheckOutTime'].dt.hour
            df['CheckInQHour'] = (df['CheckInTime'].dt.minute // 15) * 15  
            df['CheckOutQHour'] = (df['CheckOutTime'].dt.minute // 15) * 15   
            df['CheckInTime'] = pd.to_datetime(df['CheckInTime'], format='%H:%M:%S').dt.time
            df['CheckOutTime'] = pd.to_datetime(df['CheckOutTime'], format='%H:%M:%S').dt.time
                  
            def round_to_nearest_quarter_hour(time):
                # Function to round times to the nearest qaurter hour 
                if isinstance(time, pd.Timestamp):
                    time = time.time()  # Convert Timestamp to time
                minutes = (time.minute // 15) * 15
                return time.replace(minute=minutes, second=0, microsecond=0)
            
            def round_to_nearest_hour(time):
                # Function to round times to the nearest hour 
                if isinstance(time, pd.Timestamp):
                    time = time.time()  
                return time.replace(minute=0, second=0, microsecond=0)
            
            # Apply rounding function for CheckInTime / CheckOutTime
            df['RoundedCheckInHours'] = df['CheckInTime'].apply(lambda x: round_to_nearest_hour(pd.Timestamp.combine(pd.Timestamp.today(), x)))
            df['RoundedCheckOutHours'] = df['CheckOutTime'].apply(lambda x: round_to_nearest_hour(pd.Timestamp.combine(pd.Timestamp.today(), x)))
            df['RoundedCheckInQHours'] = df['CheckInTime'].apply(lambda x: round_to_nearest_quarter_hour(pd.Timestamp.combine(pd.Timestamp.today(), x)))
            df['RoundedCheckOutQHours'] = df['CheckOutTime'].apply(lambda x: round_to_nearest_quarter_hour(pd.Timestamp.combine(pd.Timestamp.today(), x)))
            
            attendance_counts_checkin = df['RoundedCheckInHours'].value_counts().sort_index()
            attendance_counts_checkout = df['RoundedCheckOutHours'].value_counts().sort_index()
            attendance_counts_quarter_checkin = df['RoundedCheckInQHours'].value_counts().sort_index()
            attendance_counts_quarter_checkout = df['RoundedCheckOutQHours'].value_counts().sort_index()
            # Convert to DataFrame
            attendance_df_checkin = attendance_counts_checkin.reset_index()
            attendance_df_checkin.columns = ['TimeInterval', 'Count']
            attendance_df_checkout = attendance_counts_checkout.reset_index()
            attendance_df_checkout.columns = ['TimeInterval', 'Count']          
            attendance_df_quarter_checkin = attendance_counts_quarter_checkin.reset_index()
            attendance_df_quarter_checkin.columns = ['TimeQInterval', 'Count']
            # Convert to DataFrame for clustering
            attendance_df_quarter_checkout = attendance_counts_quarter_checkout.reset_index()
            attendance_df_quarter_checkout.columns = ['TimeQInterval', 'Count']
            # Convert TimeInterval to numerical feature (hours since midnight)
            
            def time_to_hours(time_obj):
                return time_obj.hour
            
            def time_to_quarter_hours(time_obj):
                return time_obj.hour + (time_obj.minute // 15) * 0.25  # Convert to quarter hours
            
            attendance_df_checkin['HoursSinceMidnight'] = attendance_df_checkin['TimeInterval'].apply(time_to_hours)
            attendance_df_checkout['HoursSinceMidnight'] = attendance_df_checkout['TimeInterval'].apply(time_to_hours)
            attendance_df_quarter_checkin['QuarterSinceMidnight'] = attendance_df_quarter_checkin['TimeQInterval'].apply(time_to_quarter_hours)
            attendance_df_quarter_checkout['QuarterSinceMidnight'] = attendance_df_quarter_checkout['TimeQInterval'].apply(time_to_quarter_hours)
            # Assign processed data to the class attribute
            self.attendance_df_checkin = attendance_df_checkin
            self.attendance_df_checkout = attendance_df_checkout
            self.attendance_df_quarter_checkin = attendance_df_quarter_checkin
            self.attendance_df_quarter_checkout = attendance_df_quarter_checkout
           # print(attendance_df_quarter_checkin)
            logging.info("Attendance DataFrame prepared.")
        except Exception as e:
            logging.error(f"Error in preparing data: {e}")

    def expand_checkin_quarter_data(self):
        try:
            expanded_checkin_quarter_data = []
            for _, row in self.attendance_df_quarter_checkin.iterrows():
                expanded_checkin_quarter_data.extend([row['QuarterSinceMidnight']] * row['Count'])
            self.expanded_checkin_quarter_data = np.array(expanded_checkin_quarter_data)
            logging.info("expand_checkin_quarter_data")
        except Exception as e:
            logging.error(f"Error expanding quarter hour data: {e}")
    
    def expand_checkout_quarter_data(self):
        try:
            expanded_checkout_quarter_data = []
            for _, row in self.attendance_df_quarter_checkout.iterrows():
                expanded_checkout_quarter_data.extend([row['QuarterSinceMidnight']] * row['Count'])        
            self.expanded_checkout_quarter_data = np.array(expanded_checkout_quarter_data)
            logging.info("expand_checkout_quarter_data")
        except Exception as e:
            logging.error(f"Error expanding quarter hour data: {e}")
    
    def expand_checkin_data(self):
        try:
            expanded_data = []
            for _, row in self.attendance_df_checkin.iterrows():
                expanded_data.extend([row['HoursSinceMidnight']] * row['Count'])
            self.expanded_data = np.array(expanded_data)
            logging.info("expand_checkin_data")
        except Exception as e:
            logging.error(f"Error expanding data: {e}")

    def expand_checkout_data(self):
        try:
            expanded_checkout_data = []
            for _, row in self.attendance_df_checkout.iterrows():
                expanded_checkout_data.extend([row['HoursSinceMidnight']] * row['Count'])        
            self.expanded_checkout_data = np.array(expanded_checkout_data)
            logging.info("expand_checkout_data")
        except Exception as e:
            logging.error(f"Error expanding data: {e}")
    
    def fit_gaussian(self):
        try:
            # Fit Gaussian distribution
            if self.expanded_data.size == 0:
                raise ValueError("Expanded check-in data is empty.")
            self.mu, self.std = norm.fit(self.expanded_data)
            if self.expanded_checkout_data.size == 0:
                raise ValueError("Expanded check-out data is empty.")
            self.mu_checkout, self.std_checkout = norm.fit(self.expanded_checkout_data)
            if self.expanded_checkin_quarter_data.size == 0:
                raise ValueError("Expanded check-in quarter hour data is empty.")
            self.mu_quarter, self.std_quarter = norm.fit(self.expanded_checkin_quarter_data)  
            if self.expanded_checkout_quarter_data.size == 0:
                raise ValueError("Expanded check-out quarter hour data is empty.")
            self.mu_checkout_quarter, self.std_checkout_quarter = norm.fit(self.expanded_checkout_quarter_data)  # Fit for CheckOutQHour
            logging.info("Gaussian fit successful.")
        except Exception as e:
            logging.error(f"Error fitting Gaussian: {e}")
            
    def plot_checkin_histogram(self):
        try:
            # Create a range of values for plotting the Gaussian distribution
            xmin_In, xmax_In = self.expanded_data.min(), self.expanded_data.max()
            x_In = np.linspace(xmin_In, xmax_In, 100)
            p_In = norm.pdf(x_In, self.mu, self.std)
            # Plot Check Inhistogram and Gaussian fit
            plt.figure(figsize=(12, 6))
            plt.hist(self.expanded_data, bins=range(int(xmin_In), int(xmax_In) + 1), density=True, alpha=0.6, color='g', edgecolor='black')
            plt.plot(x_In, p_In, 'k', linewidth=2)
            plt.xlabel('Hours Since Midnight')
            plt.ylabel('Density')
            plt.title('Check In Histogram and Gaussian Fit')
            plt.grid(True)
            st.pyplot(plt)
            plt.close()
            logging.info("Histogram plotted successfully for CheckIn Histogram.")
        except Exception as e:
            logging.error(f"Error fitting Check In Histogram: {e}")   
             
    def plot_checkout_histogram(self):
        try:
            # Create a range of values for plotting the Gaussian distribution
            xmin_Out, xmax_Out = self.expanded_checkout_data.min(), self.expanded_checkout_data.max()
            x_Out = np.linspace(xmin_Out, xmax_Out, 100)
            p_Out = norm.pdf(x_Out, self.mu_checkout, self.std_checkout)
            # Plot Check out histogram and Gaussian fit
            plt.figure(figsize=(12, 6))
            plt.hist(self.expanded_checkout_data, bins=range(int(xmin_Out), int(xmax_Out) + 1), density=True, alpha=0.6, color='b', edgecolor='black')
            plt.plot(x_Out, p_Out, 'k', linewidth=2)
            plt.xlabel('Hours Since Midnight')
            plt.ylabel('Density')
            plt.title('Check Out Histogram and Gaussian Fit')
            plt.grid(True)
            st.pyplot(plt)
            plt.close()
            logging.info("Histogram plotted successfully Check Out.")
        except Exception as e:
            logging.error(f"Error fitting Histogram: {e}")  
              
    def plot_check_in_out_histogram(self):   
        try:
            # Create a range of values for plotting the Gaussian distribution
            xmin_In, xmax_In = self.expanded_data.min(), self.expanded_data.max()
            x_In = np.linspace(xmin_In, xmax_In, 100)
            p_In = norm.pdf(x_In, self.mu, self.std)
            # Create a range of values for plotting the Gaussian distribution
            xmin_Out, xmax_Out = self.expanded_checkout_data.min(), self.expanded_checkout_data.max()
            x_Out = np.linspace(xmin_Out, xmax_Out, 100)
            p_Out = norm.pdf(x_Out, self.mu_checkout, self.std_checkout)
            # Plot Check In-Out histogram and Gaussian fit
            plt.figure(figsize=(12, 6))
            plt.hist(self.expanded_data, bins=range(int(xmin_In), int(xmax_In) + 1), density=True, alpha=0.6, color='g', edgecolor='black', label='CheckIn')
            plt.plot(x_In, p_In, 'k', linewidth=2, label='Gaussian CheckIn')
            plt.hist(self.expanded_checkout_data, bins=range(int(xmin_Out), int(xmax_Out) + 1), density=True, alpha=0.6, color='b', edgecolor='black', label='CheckOut')
            plt.plot(x_Out, p_Out, 'r', linewidth=2, label='Gaussian CheckOut')
            plt.xlabel('Hours Since Midnight')
            plt.ylabel('Density')
            plt.title('Histogram and Gaussian Fit for CheckIn and CheckOut')
            plt.grid(True)
            plt.legend()
            st.pyplot(plt)
            plt.close()
            logging.info("Histogram plotted successfully for CheckIn-CheckOut.")
        except Exception as e:
            logging.error(f"Error fitting CheckIn-CheckOut Histogram: {e}")

    def plot_checkin_quarter_histogram(self):
        try:          
            x_Q = np.arange(0, 24, 0.25)  # From 0 to 23.75 in increments of 0.25
            if len(self.expanded_checkin_quarter_data) == 0:
                raise ValueError("No data available for CheckInQHour.")
            self.mu_quarter, self.std_quarter = norm.fit(self.expanded_checkin_quarter_data)
            p_Q = norm.pdf(x_Q, self.mu_quarter, self.std_quarter)
            plt.figure(figsize=(12, 6))
            plt.hist(self.expanded_checkin_quarter_data, bins=np.arange(0, 24.25, 0.25), density=True, alpha=0.6, color='y', edgecolor='black', label='CheckIn Data')
            plt.plot(x_Q, p_Q, 'k', linewidth=2, label='Gaussian Fit')
            plt.xlabel('Quarter Hours Since Midnight')
            plt.ylabel('Density')
            plt.title('Histogram and Gaussian Fit for CheckIn (Quarter Hour)')
            plt.xticks(np.arange(0, 24, 1))  # Set x-ticks for each hour
            plt.grid(True)
            plt.legend()
            st.pyplot(plt)
            plt.close()
            logging.info("Histogram plotted successfully for Quarter CheckIn.")
        except Exception as e:
            logging.error(f"Error fitting Histogram for CheckInQHour: {e}")

    def plot_checkout_quarter_histogram(self):
        try:          
            x_Q = np.arange(0, 24, 0.25)  # From 0 to 23.75 in increments of 0.25
            if len(self.expanded_checkout_quarter_data) == 0:
                raise ValueError("No data available for CheckInQHour.")
            self.mu_checkout_quarter, self.std_checkout_quarter = norm.fit(self.expanded_checkout_quarter_data)
            p_Q = norm.pdf(x_Q, self.mu_checkout_quarter, self.std_checkout_quarter)
            plt.figure(figsize=(12, 6))
            plt.hist(self.expanded_checkout_quarter_data, bins=np.arange(0, 24.25, 0.25), density=True, alpha=0.6, color='y', edgecolor='black', label='CheckOut Data')
            plt.plot(x_Q, p_Q, 'k', linewidth=2, label='Gaussian Fit')
            plt.xlabel('Quarter Hours Since Midnight')
            plt.ylabel('Density')
            plt.title('Histogram and Gaussian Fit for CheckOut (Quarter Hour)')
            plt.xticks(np.arange(0, 24, 1))  # Set x-ticks for each hour
            plt.grid(True)
            plt.legend()
            st.pyplot(plt)
            plt.close()
            logging.info("Histogram plotted successfully for Quarter CheckOut.")
        except Exception as e:
            logging.error(f"Error fitting Histogram for CheckOutQHour: {e}")
            