import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class EmployeesShiftsAssignment:

    def __init__(self, assigned_shift_data):
        self.assigned_shift_data = assigned_shift_data
    def __getitem__(self, key):
        return self.assigned_shift_data[key]
    
    def plot_stacked_bar(self,data):
        try:
            #data['EmployeeLabel'] = data['EmployeeId'] + " - " + data['EmployeeName']
            # Pivot the data to create a format suitable for a stacked bar plot
            pivot_data = data.pivot(index='EmployeeId', columns='AssignedShift', values='Percentage').fillna(0)
            # Plot the stacked bar chart
            pivot_data.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='tab20')
            plt.title("Percentage Distribution of Assigned Shifts")
            plt.xlabel("Employee Id")
            plt.ylabel("Percentage (%)")
            plt.legend(title="Assigned Shift", bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            st.pyplot(plt)
            plt.close()
        except Exception as e:
            logging.error(f"Error plot Percentage Distribution of Assigned Shifts:  {e}")
            return

    def plot_grouped_bar(self,data):
        try:
            #data['EmployeeLabel'] = data['EmployeeId'] + " - " + data['EmployeeName']
            # Pivot the data to create a format suitable for a grouped bar plot
            pivot_data = data.pivot(index='EmployeeId', columns='AssignedShift', values='Percentage').fillna(0)
            # Plot the grouped bar chart
            ax = pivot_data.plot(kind='bar', figsize=(10, 6), colormap='tab20', width=0.8)
            plt.title("Percentage Distribution of Assigned Shifts")
            plt.xlabel("Employee ID")
            plt.ylabel("Percentage (%)")
            plt.legend(title="Assigned Shift", bbox_to_anchor=(1.05, 1), loc='upper left')
            for p in ax.patches:
                height = p.get_height()
                if height > 0:  # Only annotate if the bar has a value
                    ax.annotate(f'{height:.1f}%', 
                                (p.get_x() + p.get_width() / 2., height),
                                ha='center', va='bottom', fontsize=10)
            plt.tight_layout()
            st.pyplot(plt)
            plt.close()
        except Exception as e:
            logging.error(f"Error plot Percentage Distribution of Assigned Shifts:  {e}")
            return
        
    def plot_grouped_bar_horz(self,data):
        try:
            #data['EmployeeLabel'] = data['EmployeeId'] + " - " + data['EmployeeName']
            # Pivot the data to create a format suitable for a grouped bar plot
            pivot_data = data.pivot(index='EmployeeId', columns='AssignedShift', values='Percentage').fillna(0)
            # Plot the grouped bar chart
            ax = pivot_data.plot(kind='barh', figsize=(10, 6), colormap='tab20', width=0.8)
            plt.title("Percentage Distribution of Assigned Shifts")
            plt.xlabel("Employee ID")
            plt.ylabel("Percentage (%)")
            plt.legend(title="Assigned Shift", bbox_to_anchor=(1.05, 1), loc='upper left')
            # Add percentage values next to each bar
            for p in ax.patches:
                width = p.get_width()  # The value of the bar
                if width > 0:  # Only annotate bars with a value
                    ax.annotate(f'{width:.1f}%', 
                                (width, p.get_y() + p.get_height() / 2.),  # Position: end of the bar
                                ha='left', va='center', fontsize=10)  # Align text to the left of the bar
            plt.tight_layout()
            st.pyplot(plt)
            plt.close()
        except Exception as e:
            logging.error(f"Error plot Percentage Distribution of Assigned Shifts:  {e}")
            return
        
    def plot_pie_chart(self,data):
        try:
            employees = data['EmployeeId'].unique()
            for employee_id in employees:
                employee_data = data[data['EmployeeId'] == employee_id]
               # employee_get_name = employee_data['EmployeeName'].unique()
              #  employee_name = employee_get_name
                plt.figure(figsize=(6, 6))
                plt.pie(
                    employee_data['Percentage'], 
                    labels=employee_data['AssignedShift'], 
                    autopct='%1.1f%%', 
                    startangle=90, 
                    colors=plt.cm.tab20.colors
                )
                plt.title(f"Shift Percentage Distribution for Employee {employee_id}")
                st.pyplot(plt)
                plt.close()
        except Exception as e:
                logging.error(f"Error plot Percentage Distribution:  {e}")
                return
        
    def plot_heatmap(self,data):
        try:
            #data['EmployeeLabel'] = data['EmployeeId']+ " - " + data['EmployeeName']
            pivot_data = data.pivot(index='EmployeeId', columns='AssignedShift', values='Percentage').fillna(0)
            plt.figure(figsize=(10, 6))
            sns.heatmap(pivot_data, annot=True, cmap='YlGnBu', cbar_kws={'label': 'Percentage'})
            plt.title("Heatmap of Assigned Shifts Percentage Distribution ")
            plt.xlabel("Assigned Shift")
            plt.ylabel("Employee Id")
            st.pyplot(plt)
            plt.close()
        except Exception as e:
            logging.error(f"Error Plot Heatmap of Assigned Shifts Percentage Distribution:  {e}")
            return

