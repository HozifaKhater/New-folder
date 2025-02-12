import streamlit as st
from matplotlib import rcParams
from scripts.styles import apply_styles


class AppConfig:
    @staticmethod
    def configure_app():  
        try:
            #Set global styles
            apply_styles()
            st.image("assets/MOHRAI.png", caption="", width=600)
            rcParams['font.family'] = 'Arial'
        except Exception as e:
            st.error(f"An error occurred while configuring the app: {e}")
