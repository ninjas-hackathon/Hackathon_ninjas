import streamlit as st
import google.generativeai as genai
from config import GOOGLE_API_KEY, WEATHER_API_KEY
from utils.session_state import get_chat_messages, get_weather_data

def show():
    """Display the settings page"""
    st.header("⚙️ Configuration Settings")
    
    st.subheader("🔑 API Keys")
    
    # Google API Key status
    if GOOGLE_API_KEY:
        st.success("✅ Google API Key: Configured")
        st.code("GOOGLE_API_KEY = 'AIzaSy...' (hidden for security)")
    else:
        st.error("❌ Google API Key: Not configured")
        st.code("GOOGLE_API_KEY = 'your-api-key-here'")
        st.info("Add your Google API key to config.py")
    
    # Weather API Key status
    if WEATHER_API_KEY:
        st.success("✅ Weather API Key: Configured")
        st.code("WEATHER_API_KEY = 'CBzCp...' (hidden for security)")
    else:
        st.warning("⚠️ Weather API Key: Not configured")
        st.code("WEATHER_API_KEY = 'your-weather-api-key-here'")
        st.info("Add your Weather API key to config.py (optional)")
    
    st.subheader("🤖 Model Information")
    st.info("Currently using Google Gemini AI models")
    
    # Show available models (if possible)
    if GOOGLE_API_KEY:
        try:
            available_models = list(genai.list_models())
            if available_models:
                st.write("**Available Models:**")
                for model in available_models[:5]:  # Show first 5
                    st.write(f"- {model.name}")
        except Exception as e:
            st.write(f"Could not fetch available models: {e}")
    
    st.subheader("📊 Current Session Stats")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        messages = get_chat_messages()
        st.metric("Chat Messages", len(messages))
    
    with col2:
        weather_data = get_weather_data()
        weather_status = "✅ Loaded" if not weather_data.empty else "❌ Not loaded"
        st.metric("Weather Data", weather_status)
    
    with col3:
        # Show memory usage or other stats
        import sys
        memory_mb = sys.getsizeof(st.session_state) / 1024 / 1024
        st.metric("Session Memory", f"{memory_mb:.2f} MB")
    
    # Configuration file locations
    st.subheader("📁 Configuration Files")
    st.info("""
    **File Structure:**
    - `config.py` - API keys and configuration
    - `pages/` - Individual page modules
    - `utils/` - Helper functions and utilities
    """)
    
    # Show current configuration values
    with st.expander("Current Configuration Values"):
        st.write("**Google API Key:**", "Configured" if GOOGLE_API_KEY else "Not set")
        st.write("**Weather API Key:**", "Configured" if WEATHER_API_KEY else "Not set")
        st.write("**Weather API URL:**", "https://api.rebase.energy/weather/v2/query")

show()