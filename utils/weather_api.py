import streamlit as st
import requests
import pandas as pd
import json
from config import WEATHER_API_KEY, WEATHER_API_URL, WEATHER_API_PARAMS

def fetch_weather_data():
    """Fetch weather data from Rebase Energy API"""
    if not WEATHER_API_KEY:
        st.info("💡 Add your Rebase Energy API key to display weather data")
        return pd.DataFrame()
    
    try:
        # Prepare headers
        headers = {
            "Authorization": WEATHER_API_KEY,
            "Content-Type": "application/json"
        }
        
        # Make API request
        response = requests.post(WEATHER_API_URL, headers=headers, data=json.dumps(WEATHER_API_PARAMS))
        
        return response.json()
        
            
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Network error fetching weather data: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error processing weather data: {e}")
        return pd.DataFrame()

def display_weather_setup_instructions():
    """Display instructions for setting up weather API"""
    st.markdown("""
    **To get a Rebase Energy API key:**
    1. Visit [Rebase Energy](https://www.rebase.energy/)
    2. Sign up for an account
    3. Get your API key from the dashboard
    4. Add it to the config.py file
    """)