import streamlit as st
import streamlit.components.v1 as components

def apply_styles():
    st.markdown(
        """
        
        <style>
        .title {
            font-family: 'Arial', sans-serif;  /* Change to your desired font */
            font-size: 20px;
            font-weight: bold;
            color: blue;
        }
        .subheader {
            font-family: 'Arial', sans-serif;  
            font-size: 10px;
            font-weight: bold;
        }
        .stDownloadButton > button {
            background-color: #113e99;;  /* Change to your desired button color */
            color: white;  /* Change button text color */
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
        }
        .stDownloadButton > button:hover {
            background-color: #45a049;  
        }
        body {
            background-image: url("MOHRAI_background.png");
            background-size: cover;
        }
            .stApp {
        background-color: #a2dafa; /* Change this color to your preferred background color */

        }
        .stFileUploader > label {
            background-color: #113e99;
            color: white;  
            padding: 5px 72px;
            border-radius: 5px; 
            font-size: 20px;
            display: inline-block; 
            cursor: pointer;  
        }
        input[type='file'] {
            display: none;  /* Hide the default file input */
        }
        .stTabs > div {
            background-color: weight;  /* Change to your desired background color for tabs */
            color: #333;  /* Change text color */
            font-weight: bold;  /* Make tab header text bold */
            border-radius: 20px;
            font-size: 40px;  /* Increase font size for tab headers */
        }
        .stTabs > div > button:hover {

        }
            /* Style the tab content background */
        .stTabs [data-baseweb="tab"] {
            background-color: #f0f0f0;  /* Light gray background */
            color: #333;  /* Dark text color */
            border-radius: 5px;  /* Rounded corners */
            padding: 10px;  /* Padding for spacing */
        }
            [data-testid="stSidebar"] {
        background-color: #dfe5e8; 
        }
        /* Style the active tab */
        .stTabs [aria-selected="true"] {
            background-color: #1c6785;  /* Green background for active tab */
            color: white;  /* White text color for active tab */
        }
        /* Style the tab labels */
        .stTabs [data-baseweb="tab"] p {
            font-size: 16px;  /* Font size for tab labels */
            font-weight: bold;  /* Bold text */
        }
            function openTab(tabId) {
        // Hide all tab content
        var tabs = document.getElementsByClassName('tab-content');
        for (var i = 0; i < tabs.length; i++) {
            tabs[i].style.display = 'none';
        }
        // Show the selected tab content
        document.getElementById(tabId).style.display = 'block';
        }

        .stButton > button {
            background-color: #113e99;;  /* Change to your desired button color */
            color: white;  /* Change button text color */
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
