import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
from datetime import datetime, time
from sklearn.neighbors import NearestNeighbors
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ChosenShiftAssignment:
    def __init__(self, attendance_data, shifts, n_clusters):
        self.attendance_data = attendance_data
        self.shifts = shifts
        self.n_clusters = n_clusters
        self.centroids = None
        self.kmeans = None
        self.detailed_assigend_shifts_employees = None
    @staticmethod
    def time_to_minutes(time_input):
        #Convert time strings to minutes since midnight
        if isinstance(time_input, pd.Timestamp):
            return time_input.hour * 60 + time_input.minute
        elif isinstance(time_input, datetime):
            return time_input.hour * 60 + time_input.minute
        elif isinstance(time_input, time):
            return time_input.hour * 60 + time_input.minute
        elif isinstance(time_input, str):
            #different string formats
            for fmt in ['%H:%M:%S', '%H:%M', '%I:%M %p', '%I:%M:%S %p']:
                try:
                    time_obj = datetime.strptime(time_input, fmt)
                    return time_obj.hour * 60 + time_obj.minute
                except ValueError:
                    continue
            # Raise error if no formats matched
            raise ValueError(f"Unsupported time string format: {time_input}")
        else:
            # Handle unsupported input types
            raise ValueError(f"Unsupported time format or type: {type(time_input)}")
        
    @staticmethod
    def minutes_to_time(minutes):
        #Convert minutes since midnight to time
        hours = minutes // 60
        mins = minutes % 60
        return f"{int(hours):02d}:{int(mins):02d}"

    def preprocess_data(self):
      # Ensure self.shifts is a DataFrame
        if not isinstance(self.shifts, pd.DataFrame):
            try:
                self.shifts = pd.DataFrame(self.shifts, columns=['Shift_Id', 'CheckInTime', 'CheckOutTime'])
                self.shifts['Shift_Id'] = self.shifts['Shift_Id'].astype(str)
            except ValueError as e:
                print("Error converting shifts to DataFrame:", e)
                print("self.shifts content:", self.shifts)
                return  
        self.attendance_data['CheckInMinutes'] = self.attendance_data['CheckInTime'].apply(self.time_to_minutes)
        self.attendance_data['CheckOutMinutes'] = self.attendance_data['CheckOutTime'].apply(self.time_to_minutes)
        self.shifts['StartMinutes'] = self.shifts['CheckInTime'].apply(self.time_to_minutes)
        self.shifts['EndMinutes'] = self.shifts['CheckOutTime'].apply(self.time_to_minutes)

    def apply_KNN(self):
        try:
            # Prepare data for Nearest Neighbors
            shift_features = self.shifts[['StartMinutes', 'EndMinutes']].to_numpy()
            attendance_features = self.attendance_data[['CheckInMinutes', 'CheckOutMinutes']].to_numpy()
            # Fit the nearest neighbors model
            nn = NearestNeighbors(n_neighbors=1)
            nn.fit(shift_features)
            # Find the nearest shift for each attendance record
            distances, indices = nn.kneighbors(attendance_features)
            # Map the nearest shift
            self.attendance_data['AssignedShift'] = [self.shifts.iloc[idx]['Shift_Id'] for idx in indices.flatten()]
            assigned_shift = self.attendance_data['AssignedShift']
            return assigned_shift
        except Exception as e:
            logging.error(f"Error applying KNN clustering: {e}")
            return
        
    def plot_scatter_KNN(self):
        try:
            plt.figure(figsize=(10, 6))
            scatter = plt.scatter(
                self.attendance_data['CheckInMinutes'],
                self.attendance_data['CheckOutMinutes'],
                c=self.attendance_data['AssignedShift'],  # Use AssignedShift for color coding
                cmap='viridis',
                label="Attendance Data",
                alpha=0.8,
                s=100
            )
            # Add cluster (shift) centroids
            plt.scatter(
                self.shifts['StartMinutes'],
                self.shifts['EndMinutes'],
                c='red',
                marker='X',
                s=200,
                label="Shift Clusters (Centroids)"
            )
            plt.colorbar(scatter, label="Assigned Shift")
            plt.title("Attendance Data and Shift Clusters")
            plt.xlabel("Check-In Time (Minutes since Midnight)")
            plt.ylabel("Check-Out Time (Minutes since Midnight)")
            plt.legend()
            plt.grid(alpha=0.5, linestyle='--')
            plt.tight_layout()
            st.pyplot(plt)
            plt.close()
        except Exception as e:
            logging.error(f"Error plot attendance clustring: {e}")
            return    
        
    def calculate_shift_percentages(self):
        try:
            self.attendance_data.drop(columns=['CheckInTime','CheckOutTime','CheckInQHour','CheckOutQHour'], inplace=True)        
            detailed_shift_counts = self.attendance_data.groupby(['EmployeeId', 'AssignedShift']).size().reset_index(name='TotalTransaction')
            total_shifts = self.attendance_data.groupby('EmployeeId')['AssignedShift'].count().reset_index(name='TotalShifts')
            detailed_shift_counts = detailed_shift_counts.merge(total_shifts, on='EmployeeId')
            detailed_shift_counts['Percentage'] = (detailed_shift_counts['TotalTransaction'] / detailed_shift_counts['TotalShifts']) * 100
            detailed_shift_counts['Percentage'] = detailed_shift_counts['Percentage'].round(2)
            detailed_shift_counts = detailed_shift_counts.drop(columns=['TotalShifts','StartMinutes','EndMinutes'], errors='ignore')
            detailed_assigend_shifts_employees = detailed_shift_counts.merge(
                self.shifts,
                left_on='AssignedShift',  
                right_on='Shift_Id',      
                how='left')
            detailed_assigend_shifts_employees['ShiftTime'] = detailed_assigend_shifts_employees.apply(
                lambda row: f"{row['CheckInTime']} - {row['CheckOutTime']}", axis=1)
            detailed_assigend_shifts_employees = detailed_assigend_shifts_employees.drop(columns=['TotalShifts','Shift_Id','CheckInTime','CheckOutTime','CheckInMinutes','CheckOutMinutes'], errors='ignore')
            self.detailed_assigend_shifts_employees = detailed_assigend_shifts_employees
        except Exception as e:
            logging.error(f"Error get the shifts details: {e}")
            return
        
    def plot_assigend_shifts_for_all(self):
        try:
            plt.figure(figsize=(10, 6))    
            # Calculate total transactions for each shift (using ShiftLabel)
            shifts_plot = self.shifts.copy()
            # Rename the columns
            shifts_plot.rename(columns={'CheckInTime': 'CheckIn', 'CheckOutTime': 'CheckOut'}, inplace=True)     
            attendance_with_shifts = self.attendance_data.merge(
                shifts_plot, 
                left_on='AssignedShift', 
                right_on='Shift_Id', 
                how='left')
            shift_totals = attendance_with_shifts.groupby('ShiftLabel').size()
            # Generate a color palette with as many colors as unique CheckInHour and CheckOutHour combinations
            unique_combinations = attendance_with_shifts[['CheckIn', 'CheckOut']].drop_duplicates()
            palette = sns.color_palette("husl", len(unique_combinations))
            color_map = dict(zip([tuple(x) for x in unique_combinations.values], palette))
            # Assign colors to each bar based on the CheckInHour and CheckOutHour combination
            bar_colors = attendance_with_shifts.apply(
                lambda row: color_map[(row['CheckIn'], row['CheckOut'])],
                axis=1)
            shift_totals.plot(kind='bar', color= bar_colors,alpha=0.7,  edgecolor='black')
            plt.title("All Employees Transactions by Assigned Shifts")
            plt.xlabel("Assigned Shift")
            plt.ylabel("Total Transactions")
            plt.xticks(rotation=45, ha='right')  
            plt.grid()
            st.pyplot(plt)
            plt.close()
        except Exception as e:
            logging.error(f"Error plot Employees Transactions by Assigned Shifts: {e}")
            return
        
    def plot_assigend_shifts_for_all_sorted(self):
        try:
            plt.figure(figsize=(10, 6))
            shifts_plot = self.shifts.copy()
            shifts_plot.rename(columns={'CheckInTime': 'CheckIn', 'CheckOutTime': 'CheckOut'}, inplace=True)
            # Merge attendance_data with shifts to include CheckIn and CheckOut
            attendance_with_shifts = self.attendance_data.merge(
                shifts_plot, 
                left_on='AssignedShift', 
                right_on='Shift_Id', 
                how='left')
            # Create a new column for the shift label (CheckIn - CheckOut)
            attendance_with_shifts['ShiftLabel'] = attendance_with_shifts.apply(
                lambda row: f"{row['CheckIn']} - {row['CheckOut']}", axis=1)
            # Group by ShiftLabel and calculate the total transactions, then sort by totals
            shift_totals = attendance_with_shifts.groupby('ShiftLabel').size().sort_values(ascending=True)
            # Plot horizontally and assign colors based on unique CheckIn and CheckOut combinations
            unique_combinations = attendance_with_shifts[['CheckIn', 'CheckOut']].drop_duplicates()
            palette = sns.color_palette("husl", len(unique_combinations))
            color_map = dict(zip([tuple(x) for x in unique_combinations.values], palette))
            # Assign colors to each bar based on the CheckIn and CheckOut combination
            bar_colors = [color_map[tuple(label.split(' - '))] for label in shift_totals.index]
            # Plot the bar chart horizontally
            shift_totals.plot(kind='barh', color=bar_colors, alpha=0.7, edgecolor='black')
            plt.title("All Employees Transactions by Assigned Shifts")
            plt.xlabel("Total Transactions")
            plt.ylabel("Assigned Shift (CheckIn - CheckOut)")
            plt.grid(axis='x', linestyle='--', alpha=0.7)
            plt.tight_layout()
            st.pyplot(plt)
            plt.close()

        except Exception as e:
            logging.error(f"Error plotting Employees Transactions by Assigned Shifts:  {e}")
            return

