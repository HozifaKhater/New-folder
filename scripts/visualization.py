import streamlit as st
from scripts.file_saver import FileSaver
from scripts.employees_shifts_assignment import EmployeesShiftsAssignment
from scripts.employees_assigend_shifts_report import EmployeesAssigendShiftsReport

  

class Visualization:
    @staticmethod
    def render_employees_shifts_percentage(data):
        #Render reports and visualizations for Employees Shifts Percentage.
        try:
            report_data = EmployeesAssigendShiftsReport(data)
            st.markdown("---")
            st.title("Employee Data Search: ")
            pdf_buffer = report_data.employees_assigendshifts_pdf()
            FileSaver.pdf_download_button(pdf_buffer, "AssignedShiftsReport.pdf")

            data['EmployeeId'] = data['EmployeeId'].astype(str)
            selected_employees = st.multiselect("Select Employees", options=data['EmployeeId'].unique())
            assignment = EmployeesShiftsAssignment(data)
            if selected_employees:
                filtered_data = data[data['EmployeeId'].isin(selected_employees)]
                Visualization.render_visualizations(filtered_data, assignment)
            else:
                filtered_data = data
        except Exception as e:
            st.error(f"An error occurred while rendering the employees' shifts percentage: {e}")

    @staticmethod
    def render_visualizations(data, assignment):
        #Render visualizations based on employee data.
        try:
            assignment.plot_stacked_bar(data)
            assignment.plot_grouped_bar(data)
            assignment.plot_grouped_bar_horz(data)
            assignment.plot_pie_chart(data)
            assignment.plot_heatmap(data)
        except Exception as e:
            st.error(f"An error occurred while rendering visualizations: {e}")
