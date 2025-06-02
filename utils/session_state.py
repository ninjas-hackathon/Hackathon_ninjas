import streamlit as st
import pandas as pd

def initialize_session_state():
    """Initialize all session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "weather_data" not in st.session_state:
        st.session_state.weather_data = pd.DataFrame()
    
    if "entsoe_prices" not in st.session_state:
        st.session_state.entsoe_prices = None

def get_chat_messages():
    """Get chat messages from session state"""
    return st.session_state.messages

def add_message(message):
    """Add a message to chat history"""
    st.session_state.messages.append(message)

def clear_chat():
    """Clear chat history"""
    st.session_state.messages = []

def get_weather_data():
    """Get weather data from session state"""
    return st.session_state.weather_data

def set_weather_data(data):
    """Set weather data in session state"""
    st.session_state.weather_data = data

def get_energy_prices():
    """Get energy prices from session state"""
    return st.session_state.entsoe_prices

def set_energy_prices(prices):
    """Set energy prices in session state"""
    st.session_state.entsoe_prices = prices