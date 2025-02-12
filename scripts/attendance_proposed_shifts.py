import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from mpl_toolkits.mplot3d import Axes3D


# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AttendanceProposedShifts:
    def __init__(self, df):
        self.df = df
        self.transaction_count_by_hour = None  
        self.pivot_data = None
        self.pivot_data_half = None
        self.pivot_data_quarter = None
        
    def process_data(self):
        #Group by CheckInHour and CheckOutHour to get the count of transactions.
        try:
            # Check for required columns
            if 'CheckInTime' in self.df.columns and 'CheckOutTime' in self.df.columns:
                # Convert CheckInTime and CheckOutTime to datetime
                self.df['CheckInTime'] = pd.to_datetime(self.df['CheckInTime'], format='%H:%M:%S', errors='coerce')
                self.df['CheckOutTime'] = pd.to_datetime(self.df['CheckOutTime'], format='%H:%M:%S', errors='coerce')
                # Extract hour
                self.df['CheckInHour'] = self.df['CheckInTime'].dt.hour
                self.df['CheckOutHour'] = self.df['CheckOutTime'].dt.hour   
                # Calculate quarter-hour
                self.df['CheckInQHour'] = self.df['CheckInHour'] + (self.df['CheckInTime'].dt.minute // 15) / 4.0
                self.df['CheckOutQHour'] = self.df['CheckOutHour'] + (self.df['CheckOutTime'].dt.minute // 15) / 4.0
                # Calculate Half-hour
                self.df['CheckInHalfHour'] = self.df['CheckInHour'] + (self.df['CheckInTime'].dt.minute // 30) / 2.0
                self.df['CheckOutHalfHour'] = self.df['CheckOutHour'] + (self.df['CheckOutTime'].dt.minute // 30) / 2.0
            else:
                raise ValueError("DataFrame must contain 'CheckInTime' and 'CheckOutTime' columns.")

            # Count transactions (instead of unique EmployeeId)
            self.transaction_count_by_hour = self.df.groupby(['CheckInHour', 'CheckOutHour']).size().reset_index(name='TransactionCount')
            self.transaction_count_by_quarter_hour = self.df.groupby(['CheckInQHour', 'CheckOutQHour']).size().reset_index(name='TransactionCount')
            self.transaction_count_by_half_hour = self.df.groupby(['CheckInHalfHour', 'CheckOutHalfHour']).size().reset_index(name='TransactionCount')
            self.transaction_count_by_both = self.df.groupby(['CheckInHour', 'CheckOutHour','CheckInQHour', 'CheckOutQHour']).size().reset_index(name='TransactionCount')
            logging.info("Data processed successfully.")
        except Exception as e:
            logging.error(f"Error processing data: {e}")

    def create_pivot(self):
        #Create a pivot table from the grouped data
        try:
            self.pivot_data = self.transaction_count_by_hour.pivot(index='CheckInHour', columns='CheckOutHour', values='TransactionCount').fillna(0)
            self.pivot_data_quarter = self.transaction_count_by_quarter_hour.pivot(index='CheckInQHour', columns='CheckOutQHour', values='TransactionCount').fillna(0)
            self.pivot_data_half = self.transaction_count_by_half_hour.pivot(index='CheckInHalfHour', columns='CheckOutHalfHour', values='TransactionCount').fillna(0)
            logging.info("Pivot table created successfully.")
        except Exception as e:
            logging.error(f"Error creating pivot table: {e}")

    def define_shifts(self):
        #Define shifts based on maximum transactions for each CheckInHour
        try:
             # Create a DataFrame to store shifts
            shifts = pd.DataFrame(columns=['CheckInHour', 'CheckOutHour', 'MaxTransactions', 'Percentage'])
            shifts_quarter = pd.DataFrame(columns=['CheckInQHour', 'CheckOutQHour', 'Quarter_Transactions'])
            shifts_half  = pd.DataFrame(columns=['CheckInHalfHour', 'CheckOutHalfHour', 'HalfHour_Transactions'])
            
            if self.pivot_data is not None:
                # Calculate total transactions
                total_transactions = self.pivot_data.values.sum()
                threshold = total_transactions * 0.001  # 1% of total transactions               
                # Iterate through each CheckInHour
                for checkin_hour in self.pivot_data.index:
                    max_checkout_hour = self.pivot_data.loc[checkin_hour].idxmax()  # Get CheckOutHour with max transactions
                    max_transactions = self.pivot_data.loc[checkin_hour, max_checkout_hour]  # Get the max transactions
                    shift_percentage = (max_transactions / total_transactions) * 100
                    # Filter shifts based on the threshold
                    if max_transactions > threshold:
                        temp_df = pd.DataFrame({'CheckInHour': [checkin_hour], 'CheckOutHour': [max_checkout_hour], 'MaxTransactions': [max_transactions], 'Percentage': [shift_percentage]})
                        # Filter out empty or all-NA columns in temp_df before concatenation
                        temp_df_filtered = temp_df.dropna(axis=1, how='all')
                        # Drop all-NA columns from both DataFrames
                        temp_df_filtered = temp_df_filtered.dropna(axis=1, how='all')
                        shifts = shifts.dropna(axis=1, how='all')
                        # Check if temp_df_filtered is not empty after dropping all-NA columns
                        if not temp_df_filtered.empty:
                            shifts = pd.concat([shifts, temp_df_filtered], ignore_index=True)
                        else:
                            print("temp_df_filtered is empty after dropping all-NA columns.")
                self.shifts = shifts  

            if self.pivot_data_quarter is not None:
                # Iterate through each CheckInHour quarter
                for checkin_hour_quarter in self.pivot_data_quarter.index:
                    max_checkout_hour_quarter = self.pivot_data_quarter.loc[checkin_hour_quarter].idxmax()  # Get CheckInQHour with max transactions
                    max_transactions_quarter = self.pivot_data_quarter.loc[checkin_hour_quarter, max_checkout_hour_quarter]  # Get the max transactions
                    temp_df_quarter = pd.DataFrame({'CheckInQHour': [checkin_hour_quarter], 'CheckOutQHour': [max_checkout_hour_quarter], 'Quarter_Transactions': [max_transactions_quarter]})
                    # Filter out empty or all-NA columns in temp_df before concatenation
                    temp_df_quarter_filtered = temp_df_quarter.dropna(axis=1, how='all')
                    temp_df_quarter_filtered = temp_df_quarter_filtered.dropna(axis=1, how='all')
                    shifts_quarter = shifts_quarter.dropna(axis=1, how='all')
                    # Check if temp_df_filtered is not empty after dropping all-NA columns
                    if not temp_df_quarter_filtered.empty:
                             shifts_quarter = pd.concat([shifts_quarter, temp_df_quarter_filtered], ignore_index=True)
                    else:
                            print("temp_df_filtered is empty after dropping all-NA columns.")
                self.shifts_quarter = shifts_quarter 

            self.shifts_quarter['CheckInHour'] = self.shifts_quarter['CheckInQHour'] // 1  # Extract hour part
            self.shifts_quarter['CheckOutHour'] = self.shifts_quarter['CheckOutQHour'] // 1  # Extract hour part
            self.filtered_shifts_quarter = pd.merge(
            self.shifts_quarter,  # The shift_quarter DataFrame
            self.shifts[['CheckInHour', 'CheckOutHour']],  # The shifts DataFrame
            on=['CheckInHour', 'CheckOutHour'],  # Common columns for filtering
            how='inner'  # Only keep rows that match in both DataFrames 
            )  
            self.transaction_count_by_half_hour['CheckInHour'] = self.transaction_count_by_half_hour['CheckInHalfHour'] // 1  # Extract hour part
            self.transaction_count_by_half_hour['CheckOutHour'] = self.transaction_count_by_half_hour['CheckOutHalfHour'] // 1  # Extract hour part
            self.filtered_shifts_half = pd.merge(
            self.transaction_count_by_half_hour,  # The shift_half DataFrame
            self.shifts[['CheckInHour', 'CheckOutHour']],  # The shifts DataFrame
            on=['CheckInHour', 'CheckOutHour'],  # Common columns for filtering
            how='inner'  # Only keep rows that match in both DataFrames
            )            
        except Exception as e:
            logging.error(f"Error defining shifts: {e}")

    def print_proposed_shifts(self):# Print the proposed shifts in text format.        
        try:
            if self.shifts is not None and not self.shifts.empty:
                # Replace NaN with 0 for specific columns
                self.shifts[['CheckInHour', 'CheckOutHour', 'MaxTransactions', 'Percentage']] = (
                    self.shifts[['CheckInHour', 'CheckOutHour', 'MaxTransactions', 'Percentage']].fillna(0).astype(int)
                )
                num_columns = 3  
                # Split the shifts into rows of columns
                for i in range(0, len(self.shifts), num_columns):
                    cols = st.columns(num_columns)  
                    for col, (index, row) in zip(cols, self.shifts.iloc[i:i+num_columns].iterrows()):
                        # Build shift info text
                        shift_info = (
                            f"**Shift {index + 1}:**\n"
                            f"- **Check-In Hour:** {row['CheckInHour']:02d}:00\n"
                            f"- **Check-Out Hour:** {row['CheckOutHour']:02d}:00\n"
                            f"- **Max Transactions:** {int(row['MaxTransactions'])}\n"
                            f"- **Shift percentage:** {int(row['Percentage'])} **%**"
                        )
                        # Display the shift info in the current column
                        col.markdown(shift_info)
            else:
                st.markdown("No significant shifts found.")
        except Exception as e:
            logging.error(f"Error printing proposed shifts: {e}")
            st.markdown("An error occurred while generating the proposed shifts.")

    def plot_shifts_half(self):
        #Plot a bar chart where each unique CheckInHour and CheckOutHour combination has a different color."""
        try:
            plt.figure(figsize=(16, 10))
            # Create composite labels for the x-axis
            shift_labels = self.filtered_shifts_half.apply(
                lambda row: f"{row['CheckInHalfHour']} - {row['CheckOutHalfHour']}", 
                axis=1
            )
            # Generate a color palette with as many colors as unique CheckInHour and CheckOutHour combinations
            unique_combinations = self.filtered_shifts_half[['CheckInHour', 'CheckOutHour']].drop_duplicates()
            palette = sns.color_palette("husl", len(unique_combinations))
            color_map = dict(zip([tuple(x) for x in unique_combinations.values], palette))
            # Assign colors to each bar based on the CheckInHour and CheckOutHour combination
            bar_colors = self.filtered_shifts_half.apply(
                lambda row: color_map[(row['CheckInHour'], row['CheckOutHour'])],
                axis=1
            )
            # Plot the bar chart with the composite labels and assigned colors
            plt.bar(shift_labels, 
                    self.filtered_shifts_half['TransactionCount'], 
                    color=bar_colors, 
                    alpha=0.7, 
                    label='Half Hour Transactions')
            # Set title and labels
            plt.title('Proposed Shifts by Half Hour Transactions')
            plt.xlabel('CheckIn and CheckOut Times (Hours and Half Hours)')
            plt.ylabel('Half Transactions')
            # Display grid and plot
            plt.xticks(rotation=45, ha='right')  # Rotate labels for readability
            plt.grid()
            plt.legend(loc='upper left', title='Half Hour Transactions')
            st.pyplot(plt)
        except Exception as e:
            logging.error(f"Error while plotting shift half hour data with unique colors: {e}")

    def plot_shifts_quarter(self):
        #Plot a bar chart where each unique CheckInHour and CheckOutHour combination has a different color."""
        try:
            plt.figure(figsize=(10, 6))
            # Create composite labels for the x-axis
            shift_labels = self.filtered_shifts_quarter.apply(
                lambda row: f"{row['CheckInQHour']} - {row['CheckOutQHour']}", 
                axis=1
            )
            # Generate a color palette with as many colors as unique CheckInHour and CheckOutHour combinations
            unique_combinations = self.filtered_shifts_quarter[['CheckInHour', 'CheckOutHour']].drop_duplicates()
            palette = sns.color_palette("husl", len(unique_combinations))
            color_map = dict(zip([tuple(x) for x in unique_combinations.values], palette))
            # Assign colors to each bar based on the CheckInHour and CheckOutHour combination
            bar_colors = self.filtered_shifts_quarter.apply(
                lambda row: color_map[(row['CheckInHour'], row['CheckOutHour'])],
                axis=1
            )
            # Plot the bar chart with the composite labels and assigned colors
            plt.bar(shift_labels, 
                    self.filtered_shifts_quarter['Quarter_Transactions'], 
                    color=bar_colors, 
                    alpha=0.7, 
                    label='Quarter Transactions')
            plt.title('Proposed Shifts by Quarter Transactions')
            plt.xlabel('CheckIn and CheckOut Times (Hours and Quarter Hours)')
            plt.ylabel('Quarter Transactions')
            plt.xticks(rotation=45, ha='right')  
            plt.grid()
            plt.legend(loc='upper left', title='Quarter Transactions')
            st.pyplot(plt)
            plt.close()
        except Exception as e:
            logging.error(f"Error while plotting shift quarter data with unique colors: {e}")

    def plot_shifts_quarter_sorted(self):        
            try:
                plt.figure(figsize=(13, 6))
                sorted_shifts = self.shifts.sort_values(by='MaxTransactions', ascending=True)              
                sorted_pairs = sorted_shifts[['CheckInHour', 'CheckOutHour']].drop_duplicates().reset_index(drop=True)                
                sorted_pairs['sort_order'] = sorted_pairs.index
                shift_quarter_with_order = self.filtered_shifts_quarter.merge(
                    sorted_pairs, 
                    on=['CheckInHour', 'CheckOutHour'], 
                    how='left'
                )
                sorted_shift_quarter = shift_quarter_with_order.sort_values(by='sort_order').drop(columns='sort_order')
                shift_labels = sorted_shift_quarter.apply(
                    lambda row: f"{row['CheckInQHour']} - {row['CheckOutQHour']}", 
                    axis=1
                )
                unique_combinations = sorted_shift_quarter[['CheckInHour', 'CheckOutHour']].drop_duplicates()
                palette = plt.get_cmap("tab20")  # Use a more vibrant colormap
                colors = [palette(i % 20) for i in range(len(unique_combinations))]  # Ensure vibrant colors by looping over the colormap
                color_map = dict(zip([tuple(x) for x in unique_combinations.values], colors))
                # Assign colors to each bar based on the CheckInHour and CheckOutHour combination
                bar_colors = sorted_shift_quarter.apply(
                        lambda row: color_map[(row['CheckInHour'], row['CheckOutHour'])],
                        axis=1
                )
                # Plot the bar chart with the composite labels
                plt.barh(shift_labels, 
                        sorted_shift_quarter['Quarter_Transactions'], 
                        color=bar_colors, 
                        alpha=0.7, 
                        label='Quarter Transactions')
                plt.title('Proposed Shifts (Horizontal Bar Plot - Sorted by Max Transactions)')
                plt.xlabel('Max Transactions')
                plt.ylabel('CheckInHour to CheckOutHour')
                plt.legend(loc='upper right')
                plt.grid()
                st.pyplot(plt)  
                plt.close()      
            except Exception as e:
                logging.error(f"Error while plotting shift quarter data: {e}")
       
    def plot_shifts(self):
        
        plt.figure(figsize=(10, 6))
        shift_indices = self.shifts.apply(
                lambda row: f"{row['CheckInHour']} - {row['CheckOutHour']}", 
                axis=1
        )
        plt.bar(shift_indices.astype(str), 
                self.shifts ['MaxTransactions'], 
                color='b', 
                alpha=0.7, 
                label='Max Transactions')
        # Add a secondary axis for percentage
        ax2 = plt.gca().twinx()  # Create a twin Axes sharing the xaxis
        ax2.plot(shift_indices.astype(str), 
                self.shifts ['Percentage'], 
                color='r', 
                marker='o', 
                label='Percentage')
        plt.title(' Proposed Shifts')
        plt.xlabel('CheckInHour to CheckOutHour')
        plt.ylabel('Max Transactions')
        ax2.set_ylabel('Percentage (%)')
        plt.legend(loc='upper left')
        ax2.legend(loc='upper right')
        plt.grid()
        st.pyplot(plt)        
        plt.close()

    def plot_shifts_sorted(self):
        # Sort the shifts DataFrame by 'MaxTransactions' in ascending order
        sorted_shifts = self.shifts.sort_values(by='MaxTransactions', ascending=True)
        plt.figure(figsize=(10, 6))
        shift_indices = sorted_shifts.apply(
                lambda row: f"{row['CheckInHour']} - {row['CheckOutHour']}", 
              axis=1
        )
        # Plot the horizontal bar chart
        plt.barh(shift_indices.astype(str), 
                sorted_shifts['MaxTransactions'], 
                color='b', 
                alpha=0.7, 
                label='Max Transactions')
        plt.title('Proposed Shifts (Horizontal Bar Plot - Sorted by Max Transactions)')
        plt.xlabel('Max Transactions')
        plt.ylabel('CheckInHour to CheckOutHour')
        plt.legend(loc='upper right')
        plt.grid()
        st.pyplot(plt)
        plt.close()

    def plot_heatmap(self):
        #Plot the heatmap for CheckInHour vs CheckOutHour
        try:
            plt.figure(figsize=(16, 12))
            sns.heatmap(self.pivot_data, annot=True, fmt='.0f', cmap='coolwarm')
            plt.title('CheckInHour - CheckOutHour Transaction Count')
            plt.xlabel('CheckOutHour')
            plt.ylabel('CheckInHour')
            st.pyplot(plt)
            plt.close()
            logging.info("Heatmap plotted successfully.")
        except Exception as e:
            logging.error(f"Error plotting heatmap: {e}")
 
    def plot_quarter_heatmap(self):
        #Plot the heatmap for CheckInHour vs CheckOutHour
        try:
            plt.figure(figsize=(30, 20))
            sns.heatmap(self.pivot_data_quarter, annot=True, fmt='.0f', cmap='coolwarm')
            plt.title('CheckIn Quarter Hour - CheckOut Quarter Hour Transaction Count')
            plt.xlabel('CheckOutQHour')
            plt.ylabel('CheckInQHour')
            st.pyplot(plt)
            plt.close()
            logging.info("Heatmap plotted successfully.")
        except Exception as e:
            logging.error(f"Error plotting heatmap: {e}")

    def plot_half_heatmap(self):
        #Plot the heatmap for CheckInHour vs CheckOutHour
        try:
            plt.figure(figsize=(30, 20))
            sns.heatmap(self.pivot_data_half, annot=True, fmt='.0f', cmap='coolwarm')
            plt.title('CheckIn Half Hour - CheckOut Half Hour Transaction Count')
            plt.xlabel('CheckHalfHour')
            plt.ylabel('CheckInHalfHour')
            st.pyplot(plt)
            plt.close()
            logging.info("Heatmap plotted successfully.")
        except Exception as e:
            logging.error(f"Error plotting heatmap: {e}")

    def plot_heatmap_shifts_quarter(self):
        #Plot the heatmap for CheckInHour vs CheckOutHour.
        try:
            Shift_details = self.filtered_shifts_quarter.drop(columns=['CheckInHour', 'CheckOutHour'])
            self.pivot_data_shifts_quarter = Shift_details.pivot(index=['CheckInQHour'], columns=['CheckOutQHour'], values='Quarter_Transactions').fillna(0)
            plt.figure(figsize=(16, 12))
            sns.heatmap(self.pivot_data_shifts_quarter, annot=True, fmt='.0f', cmap='coolwarm')
            plt.title('CheckInQHour - CheckOutQHour Transaction Count')
            plt.xlabel('CheckOutQHour')
            plt.ylabel('CheckInQHour')
            st.pyplot(plt)
            plt.close()
            logging.info("Heatmap plotted successfully.")
        except Exception as e:
            logging.error(f"Error plotting heatmap both: {e}")


