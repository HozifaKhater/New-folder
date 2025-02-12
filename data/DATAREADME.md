We have two types of Data:

1- raw folder(raw data) -> data expoported for the database
       we have 4 subfolder for the clients             
2- procced folder (processed data)-> data after applying data 
    analysis and transformation

    # we have 4 subfolder for the clients
    # the file name client_Prepsred_data.csv is the out put  from the Notebook :  /notebook/client/client_data_preprocessing.ipynb
    # the file name client_transformation_data.csv is the out put of the notebook : notebook/client/client_data_transformation.ipynb

    Note: replace client with  3340_giza or any other.


---

# Data to upload:

1. upload csv file for the attendance data for any client. the data must enclude: required_columns = ['EmployeeId', 'TransDateTime', 'Type']

2. upload csv file for the chosen shifts from the client. the data must enclude: required_columns = ['Shift_Id', 'CheckInTime', 'CheckOutTime']



