import streamlit as st
import requests
import pandas as pd
from config import WEATHER_API_KEY, WEATHER_API_URL, WEATHER_API_PARAMS

def fetch_weather_data():
    """Fetch weather data from Rebase Energy API"""
    if not WEATHER_API_KEY:
        st.info("💡 Add your Rebase Energy API key to display weather data")
        return pd.DataFrame()
    
    try:
        # Prepare headers
        if not WEATHER_API_KEY.startswith('Bearer '):
            headers = {"Authorization": f"Bearer {WEATHER_API_KEY}"}
        else:
            headers = {"Authorization": WEATHER_API_KEY}
        
        # Make API request
        response = requests.get(WEATHER_API_URL, headers=headers, params=WEATHER_API_PARAMS)
        
        # Handle different response statuses
        if response.status_code == 401:
            st.error("❌ Weather API: Unauthorized - Please check your API key")
            return pd.DataFrame()
        elif response.status_code == 403:
            st.error("❌ Weather API: Forbidden - API key doesn't have access to this endpoint")
            return pd.DataFrame()
        elif response.status_code != 200:
            st.error(f"❌ Weather API Error: Status code {response.status_code}")
            return pd.DataFrame()
        
        # Process successful response
        json_data = response.json()
        st.success("✅ Weather API connected successfully!")
        
        # Convert to DataFrame
        if isinstance(json_data, list):
            return pd.DataFrame(json_data)
        elif isinstance(json_data, dict) and 'data' in json_data:
            return pd.DataFrame(json_data['data'])
        else:
            st.warning("Unexpected JSON format from weather API")
            return pd.DataFrame()
            
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