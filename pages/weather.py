import streamlit as st
from utils.weather_api import fetch_weather_data, display_weather_setup_instructions
from utils.session_state import get_weather_data, set_weather_data

def show():
    """Display the weather data page"""
    st.header("Weather Data Analysis")
    
    # Get current weather data from session state
    df = get_weather_data()
    
    # Button to fetch new weather data
    if st.button("Refresh Weather Data"):
        with st.spinner("Fetching weather data..."):
            new_data = fetch_weather_data()
            set_weather_data(new_data)
            df = new_data
            st.rerun()
    
    # Display weather data if available
    if not df.empty:
        st.success("✅ Weather data loaded successfully!")
        
        # Weather data display with better formatting
        st.subheader("📊 Raw Weather Data")
        st.dataframe(df, use_container_width=True)
        
        # Basic statistics if data is available
        st.subheader("📈 Data Summary")
        
        # Check if we have numeric columns for statistics
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_cols) > 0:
            st.write("**Numeric Data Statistics:**")
            st.dataframe(df[numeric_cols].describe(), use_container_width=True)
        
        # Show data info
        st.subheader("ℹ️ Dataset Information")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Rows", len(df))
        with col2:
            st.metric("Total Columns", len(df.columns))
        
        st.write("**Column Names:**", list(df.columns))
        
    else:
        st.warning("⚠️ No weather data available")
        st.info("Click 'Refresh Weather Data' to load weather data, or configure your API key in the Settings tab.")
        
        # Show setup instructions
        with st.expander("How to get Weather API access"):
            display_weather_setup_instructions()

show()