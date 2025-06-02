import streamlit as st
import google.generativeai as genai

# API Keys
GOOGLE_API_KEY = 'AIzaSyBJiitah4ELmIRv4G1CLtAk2LmxcTrbQAw'  # Insert your actual Google API key here
WEATHER_API_KEY = 'q1XdYSQwrujtCGDkQztRkd2cVNuxutzxk1SK81HhI60'  # Insert your actual Rebase Energy API key

# Weather API Configuration
WEATHER_API_URL = "https://api.rebase.energy/weather/v2/query"

WEATHER_API_PARAMS = {
    'model': 'DWD_ICON-EU',
    'start-date': '2025-06-02',
    'end-date': '2025-06-05',
    "latitude": "59.3293",   # Stockholm
    "longitude": "18.0686",
    'variables': 'Temperature, WindSpeed, SolarDownwardRadiation',
    'output-format': 'json',
    'output-schema': 'list'
}

# Energy API Configuration
ENERGY_COUNTRY_CODES = ["SE_3", "SE_4"]

def setup_page_config():
    """Set up Streamlit page configuration"""
    st.set_page_config(
        page_title="🤖 AI Assistant with Weather Data",
        layout="wide",
        initial_sidebar_state="auto"
    )

def initialize_gemini():
    """Initialize Google Gemini API"""
    if GOOGLE_API_KEY:
        genai.configure(api_key=GOOGLE_API_KEY)
        
        # Try to use the latest Gemini model
        try:
            return genai.GenerativeModel('gemini-1.5-flash')
        except:
            try:
                return genai.GenerativeModel('gemini-1.5-pro')
            except:
                return genai.GenerativeModel('models/gemini-1.5-flash')
    return None