import streamlit as st
import logging


class FileSaver:

    def __init__(self, df):
        self.df = df


    def to_csv(self):
        try:
            # Convert the DataFrame to CSV format
            return self.df.to_csv(index=False)
        except AttributeError as e:
            st.error(f"DataFrame attribute error: {e}")
            return None
        except ValueError as e:
            st.error(f"DataFrame value error: {e}")
            return None
        except Exception as e:
            st.error(f"An unexpected error occurred while converting to CSV: {e}")
            return None
        
    def download_button(self, button_label="Download CSV", filename="data.csv", key="Download - csv"):
        try:
            csv = self.to_csv()  # Get the CSV data
            if csv is None:
                st.error("Failed to generate CSV. Please ensure the data is valid.")
                return            
            # Create the download button
            st.download_button(
                button_label,
                csv,
                filename,
                "Shifts Data",
                key=key)
        except FileNotFoundError as e:
            st.error(f"File not found: {e}")
        except TypeError as e:
            st.error(f"Type error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred while creating the download button: {e}")

    def pdf_download_button(pdf_buffer, filename):
        try:

            if pdf_buffer:
                st.download_button(
                    label="Pdf - Download Assigend Shifts Report",
                    data=pdf_buffer,
                    file_name=filename,
                    mime="application/pdf"
                )     
                logging.info("Downlaod button display.")
            else:
                st.error("Failed to generate the PDF file")
                logging.error("PDF buffer is empty.")

        except FileNotFoundError as e:
            st.error(f"File not found: {e}")
        except TypeError as e:
            st.error(f"Type error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred while creating the download button: {e}")
