import streamlit as st
from scripts.attendance_proposed_shifts import AttendanceProposedShifts
from scripts.file_saver import FileSaver
from scripts.attendance_data_processor import AttendanceDataProcessor
from scripts.upload_chosen_shifts import UploadChosenShifts
from scripts.chosen_shifts_assignment import ChosenShiftAssignment
from scripts.attendance_gaussian import AttendanceGaussian
from scripts.attendance_heatmap import AttendanceHeatmap
from scripts.visualization import Visualization

class TabsManager:

    def process_data_in_tabs(data): #Process data and display results in tabs
        try:
            tab1, tab2, tab3, tab4, tab5 = st.tabs(
                ["Data Processing", "Gaussian", "Heatmap", "Processed Shifts", "Allocation"]
            )
            # Data Processing Tab
            with tab1:
                st.header("Data Processing")
                final_data = process_attendance_data(data)
            # Gaussian Tab
            with tab2:
                st.header("Gaussian Analysis")
                if final_data is not None:
                    render_gaussian_analysis(final_data)
            # Heatmap Tab
            with tab3:
                st.header("Heatmap Analysis")
                if final_data is not None:
                    render_heatmap_analysis(final_data)
            
            # Processed Shifts Tab
            with tab4:
                st.header("Processed Shifts")
                if final_data is not None:
                    render_processed_shifts(final_data)
            
            # Allocation Tab
            with tab5:
                st.header("Shift Allocation")
                if final_data is not None:
                    handle_shift_allocation(final_data)
        except Exception as e:
            st.error(f"An error occurred while processing data in tabs: {e}")


def render_processed_shifts(final_data): #Render processed shifts visualizations
    try:
        proposed_shifts = AttendanceProposedShifts(final_data)
        proposed_shifts.process_data()  # Process the data to group by hours
        proposed_shifts.create_pivot()   # Create the pivot table for plotting
        proposed_shifts.define_shifts()
        proposed_shifts.print_proposed_shifts()
        proposed_shifts.plot_shifts()    
        proposed_shifts.plot_shifts_half()
        proposed_shifts.plot_shifts_quarter()
        proposed_shifts.plot_shifts_sorted()
        proposed_shifts.plot_shifts_quarter_sorted()
    except Exception as e:
        st.error(f"An error occurred while rendering processed shifts: {e}")

def process_attendance_data(data): #Process attendance data and render visualizations
    try:
        processor = AttendanceDataProcessor(data)
        preprocess_data_text = st.empty() 
        filter_transactions_text = st.empty() 
        aggregate_data_text = st.empty()  
        with st.container(border = True):    
            preprocess_data_text.markdown("- **Preprocessing Data**: In Progress...")
            processor.preprocess_data()
            preprocess_data_text.markdown("- **Preprocessing Data**: <span style='color: blue;'>Completed!</span>", unsafe_allow_html=True)
            # Filtering Transactions
            filter_transactions_text.markdown("- **Filtering Transactions**: In Progress...")
            processor.filter_transactions()
            filter_transactions_text.markdown("- **Filtering Transactions**: <span style='color: blue;'>Completed!</span>", unsafe_allow_html=True)
            # Aggregating Data
            aggregate_data_text.markdown("- **Aggregating Data**: In Progress...")
            processor.aggregate_data()
            aggregate_data_text.markdown("- **Aggregating Data**: <span style='color: blue;'>Completed!</span>", unsafe_allow_html=True)
        final_data = processor.final_data
        st.dataframe(final_data.head(5))
        FileSaver(final_data).download_button(
            button_label="Download Processed Data as CSV",
            filename="processed_data.csv",
            key="Attendance Data")
        return final_data
    except Exception as e:
        st.error(f"An error occurred while processing attendance data: {e}")
        return None

def handle_shift_allocation(final_data): #Handle allocation of shifts and render visualizations
    try:
        get_chosen_shifts = UploadChosenShifts()
        chosen_shifts = get_chosen_shifts.upload_shifts()
        if chosen_shifts is not None:
            shift_assignment = ChosenShiftAssignment(final_data, chosen_shifts, len(chosen_shifts))
            shift_assignment.preprocess_data()
            shift_assignment.apply_KNN()
            shift_assignment.plot_scatter_KNN()
            shift_assignment.calculate_shift_percentages()
            shift_assignment.plot_assigend_shifts_for_all_sorted() 
            shift_assignment_data = shift_assignment.attendance_data
            st.dataframe(shift_assignment_data.head(5))
            file_saver = FileSaver(shift_assignment_data)
            file_saver.download_button(button_label="Download Shift Allocation Data as CSV", filename="Shift_Allocation_data.csv", key="Allocation Shifts")
            detailed_shift_counts_Data = shift_assignment.detailed_assigend_shifts_employees
            st.dataframe(detailed_shift_counts_Data.head(5))
            file_saver = FileSaver(detailed_shift_counts_Data)
            file_saver.download_button(button_label="Download Employees Shifts Percentage Data as CSV", filename="Employees_Shifts_Percentage.csv", key="Employees Shifts")
            Visualization.render_employees_shifts_percentage(detailed_shift_counts_Data)

    except Exception as e:
        st.error(f"An error occurred while handling shift allocation: {e}")


def render_gaussian_analysis(final_data): #Render Gaussian analysis for processed data
    try:
        gaussian = AttendanceGaussian(final_data)
        gaussian.expand_checkin_quarter_data()
        gaussian.expand_checkout_quarter_data()
        gaussian.expand_checkout_data()
        gaussian.expand_checkin_data() 
        fit_gaussian_checkin_text = st.empty()
        fit_gaussian_checkin_text.markdown("- **Fit Gaussian Check In**: In Progress...")
        gaussian.fit_gaussian()
        fit_gaussian_checkin_text.markdown("- **Fit Gaussian Check In**: <span style='color: blue;'>Completed!</span>", unsafe_allow_html=True) 
        with st.container(border = True):    
            gaussian.plot_checkin_histogram()
            gaussian.plot_checkout_histogram()
            gaussian.plot_check_in_out_histogram() 
            gaussian.plot_checkin_quarter_histogram()
            gaussian.plot_checkout_quarter_histogram()
    except Exception as e:
        st.error(f"An error occurred during Gaussian analysis: {e}")

def render_heatmap_analysis(final_data): #Render heatmap analysis for processed data
    try:
        heatmap = AttendanceHeatmap(final_data)
        heatmap.process_data()
        heatmap.create_pivot()
        st.subheader("Check-In and Check-Out Heatmap") 
        heatmap.plot_heatmap()
        proposed_shift_heatmap = AttendanceProposedShifts(final_data)
        proposed_shift_heatmap.process_data()  # Process the data to group by hours
        proposed_shift_heatmap.create_pivot()   # Create the pivot table for plotting
        proposed_shift_heatmap.define_shifts()  
        st.subheader("Check-In and Check-Out Transaction Heatmap")
        proposed_shift_heatmap.plot_heatmap()   # Plot the heatmap
        proposed_shift_heatmap.plot_quarter_heatmap()
        proposed_shift_heatmap.plot_half_heatmap()
    except Exception as e:
        st.error(f"An error occurred while rendering the heatmap analysis: {e}")

