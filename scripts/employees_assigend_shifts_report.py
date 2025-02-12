import traceback
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import logging
from io import BytesIO


# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EmployeesAssigendShiftsReport:
    def __init__(self, data):
        self.data = data
    
    def employees_assigendshifts_pdf(self, group_size = 5):
        #Validate input data
        try:             
            unique_ids = self.data['EmployeeId'].unique()
        except Exception as e:
            logging.error(f"Error accessing EmployeeId from data:  {e}")
            print(traceback.format_exc())
            return
        # Split EmployeeIds into groups
        try:
            grouped_ids = [unique_ids[i:i + group_size] for i in range(0, len(unique_ids), group_size)]
        except Exception as e:
            logging.error(f"Error splitting EmployeeId into groups:  {e}")
            print(traceback.format_exc())
            return
        #Create the PDF
        try:

            pdf_buffer = BytesIO()
            with PdfPages(pdf_buffer) as pdf:
                for i, group in enumerate(grouped_ids):
                    try:
                        group_data = self.data[self.data['EmployeeId'].isin(group)]
                        pivot_data = group_data.pivot(index='EmployeeId', columns='ShiftTime', values='Percentage').fillna(0)
                        pivot_data = pivot_data.sort_index(ascending=False)
                        ax = pivot_data.plot(kind='barh', figsize=(10, 6), colormap='tab20', width=0.8)
                        plt.title(f"Percentage Distribution of Assigned Shifts (Group {i+1})")
                        plt.xlabel("Percentage (%)")
                        plt.ylabel("Employee ID")
                        plt.legend(title="Shift (CheckIn - CheckOut)", bbox_to_anchor=(1.05, 1), loc='upper left')
                        for p in ax.patches:
                            width = p.get_width()
                            if width > 0:
                                ax.annotate(f'{width:.1f}%',
                                            (width, p.get_y() + p.get_height() / 2.),
                                            ha='left', va='center', fontsize=10)      
                        plt.tight_layout()
                        pdf.savefig()
                        plt.clf()
                        plt.close()
                            
                    except Exception as e:
                        logging.error(f"Error processing group: {e}")
                        print(traceback.format_exc())
                        continue  # Skip to the next group
            pdf_buffer.seek(0)
            #logging.info("PDF generated successfully.")
            return pdf_buffer
        except Exception as e:
                logging.error(f"Error creating or saving the PDF: {e}")
                print(traceback.format_exc())
                return
        finally:
            # Close the buffer to release memory
       #     pdf_buffer.close()
            logging.info("PDF buffer memory released.")