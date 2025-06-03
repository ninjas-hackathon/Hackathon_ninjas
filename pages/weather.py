import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from plotly.subplots import make_subplots
from datetime import datetime
from utils.weather_api import fetch_weather_data, display_weather_setup_instructions
from utils.session_state import get_weather_data, set_weather_data
from utils.data_processing import create_weather_dataframe

def create_temperature_chart(df):
    """Create temperature time series chart"""
    fig = px.line(df, 
                  x='valid_datetime', 
                  y='Temperature',
                  title='Temperature Over Time',
                  labels={'Temperature': 'Temperature (°C)', 'valid_datetime': 'Date & Time'},
                  line_shape='spline')
    
    fig.update_layout(
        xaxis_title="Date & Time",
        yaxis_title="Temperature (°C)",
        hovermode='x unified',
        showlegend=False
    )
    
    fig.update_traces(
        line=dict(color='#FF6B6B', width=3),
        hovertemplate='<b>%{y:.1f}°C</b><br>%{x}<extra></extra>'
    )
    
    return fig

def create_solar_radiation_chart(df):
    """Create solar radiation time series chart"""
    fig = px.line(df, 
                  x='valid_datetime', 
                  y='SolarDownwardRadiation',
                  title='Solar Radiation Over Time',
                  labels={'SolarRadiation': 'Solar Radiation (W/m²)', 'valid_datetime': 'Date & Time'},
                  line_shape='spline')
    
    fig.update_layout(
        xaxis_title="Date & Time",
        yaxis_title="Solar Radiation (W/m²)",
        hovermode='x unified',
        showlegend=False
    )
    
    fig.update_traces(
        line=dict(color='#FFD700', width=3),
        hovertemplate='<b>%{y:.1f} W/m²</b><br>%{x}<extra></extra>'
    )
    
    return fig

def create_windspeed_chart(df):
    """Create wind speed time series chart"""
    fig = px.line(df, 
                  x='valid_datetime', 
                  y='WindSpeed',
                  title='Wind Speed Over Time',
                  labels={'WindSpeed': 'Wind Speed (m/s)', 'valid_datetime': 'Date & Time'},
                  line_shape='spline')
    
    fig.update_layout(
        xaxis_title="Date & Time",
        yaxis_title="Wind Speed (m/s)",
        hovermode='x unified',
        showlegend=False
    )
    
    fig.update_traces(
        line=dict(color='#4ECDC4', width=3),
        hovertemplate='<b>%{y:.1f} m/s</b><br>%{x}<extra></extra>'
    )
    
    return fig

def create_combined_chart(df):
    """Create combined temperature and solar radiation chart with dual y-axes"""
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Temperature trace (left y-axis)
    fig.add_trace(
        go.Scatter(
            x=df['valid_datetime'],
            y=df['Temperature'],
            name='Temperature',
            line=dict(color='#FF6B6B', width=3),
            hovertemplate='<b>Temperature: %{y:.1f}°C</b><br>%{x}<extra></extra>'
        ),
        secondary_y=False,
    )

    # Solar radiation trace (right y-axis)
    fig.add_trace(
        go.Scatter(
            x=df['valid_datetime'],
            y=df['SolarDownwardRadiation'],
            name='Solar Radiation',
            line=dict(color='#FFD700', width=3),
            hovertemplate='<b>Solar Radiation: %{y:.1f} W/m²</b><br>%{x}<extra></extra>'
        ),
        secondary_y=True,
    )

    # Axis labels
    fig.update_yaxes(title_text="Temperature (°C)", secondary_y=False)
    fig.update_yaxes(title_text="Solar Radiation (W/m²)", secondary_y=True)

    # Layout
    fig.update_layout(
        title="Temperature and Solar Radiation Over Time",
        xaxis_title="Date & Time",
        hovermode='x unified'
    )

    return fig

def create_daily_summary_chart(df):
    """Create daily summary charts"""
    daily_stats = df.groupby('Date').agg({
        'Temperature': ['min', 'max', 'mean'],
        'WindSpeed': ['min', 'max', 'mean'],
        'SolarDownwardRadiation': ['min', 'max', 'mean']
    }).round(2)
    
    # Flatten column names
    daily_stats.columns = ['_'.join(col).strip() for col in daily_stats.columns]
    daily_stats = daily_stats.reset_index()
    
    # Create subplots for daily summary
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=('Daily Temperature Range', 'Daily Wind Speed Range', 'Daily Solar Radiation Range'),
        vertical_spacing=0.1
    )
    
    # Temperature range
    fig.add_trace(
        go.Scatter(x=daily_stats['Date'], 
                  y=daily_stats['Temperature_max'],
                  fill=None,
                  mode='lines+markers',
                  name='Max Temp',
                  line=dict(color='#FF8E8E')),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=daily_stats['Date'], 
                  y=daily_stats['Temperature_min'],
                  fill='tonexty',
                  mode='lines+markers',
                  name='Min Temp',
                  line=dict(color='#FFB4B4')),
        row=1, col=1
    )
    
    # Wind speed range
    fig.add_trace(
        go.Scatter(x=daily_stats['Date'], 
                  y=daily_stats['WindSpeed_max'],
                  fill=None,
                  mode='lines+markers',
                  name='Max Wind',
                  line=dict(color='#4ECDC4')),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=daily_stats['Date'], 
                  y=daily_stats['WindSpeed_min'],
                  fill='tonexty',
                  mode='lines+markers',
                  name='Min Wind',
                  line=dict(color='#A8E6E1')),
        row=2, col=1
    )

    # Solar radiation range
    fig.add_trace(
        go.Scatter(x=daily_stats['Date'], 
                  y=daily_stats['SolarDownwardRadiation_max'],
                  fill=None,
                  mode='lines+markers',
                  name='Max Solar',
                  line=dict(color='#FFD700')),
        row=3, col=1
    )
    fig.add_trace(
        go.Scatter(x=daily_stats['Date'], 
                  y=daily_stats['SolarDownwardRadiation_min'],
                  fill='tonexty',
                  mode='lines+markers',
                  name='Min Solar',
                  line=dict(color='#FFF9C4')),
        row=3, col=1
    )
    
    fig.update_yaxes(title_text="Temperature (°C)", row=1, col=1)
    fig.update_yaxes(title_text="Wind Speed (m/s)", row=2, col=1)
    fig.update_yaxes(title_text="Solar Radiation (W/m²)", row=3, col=1)
    fig.update_layout(height=600, title_text="Daily Weather Summary")
    
    return fig, daily_stats

def show():
    """Display the weather data page with enhanced visualizations"""
    st.header("🌤️ Weather Data Analysis")
    
    # Get current weather data from session state
    weather_data = get_weather_data()
    
    # Button to fetch new weather data
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🔄 Refresh Weather Data", use_container_width=True):
            with st.spinner("Fetching weather data..."):
                new_data = fetch_weather_data()
                set_weather_data(new_data)
                weather_data = new_data
                st.rerun()
    
    # Convert to DataFrame
    df = create_weather_dataframe(weather_data)
    
    # Display weather data if available
    if not df.empty:
        st.success("✅ Weather data loaded successfully!")
        
        # Key metrics at the top
        st.subheader("📊 Current Weather Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            current_temp = df['Temperature'].iloc[-1] if len(df) > 0 else 0
            st.metric("Current Temperature", f"{current_temp:.1f}°C")
        
        with col2:
            current_wind = df['WindSpeed'].iloc[-1] if len(df) > 0 else 0
            st.metric("Current Wind Speed", f"{current_wind:.1f} m/s")
        
        with col3:
            avg_temp = df['Temperature'].mean()
            st.metric("Average Temperature", f"{avg_temp:.1f}°C")
        
        with col4:
            max_wind = df['WindSpeed'].max()
            st.metric("Max Wind Speed", f"{max_wind:.1f} m/s")
        
        # Visualization tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📈 Combined View", "🌡️ Temperature", "💨 Wind Speed", "Solar Radiation", "📅 Daily Summary", "📋 Raw Data"])
        
        with tab1:
            st.subheader("Temperature and Wind Speed Over Time")
            combined_fig = create_combined_chart(df)
            st.plotly_chart(combined_fig, use_container_width=True)
        
        with tab2:
            st.subheader("Temperature Trend")
            temp_fig = create_temperature_chart(df)
            st.plotly_chart(temp_fig, use_container_width=True)
            
            # Temperature statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Min Temperature", f"{df['Temperature'].min():.1f}°C")
            with col2:
                st.metric("Max Temperature", f"{df['Temperature'].max():.1f}°C")
            with col3:
                st.metric("Temperature Range", f"{df['Temperature'].max() - df['Temperature'].min():.1f}°C")
        
        with tab3:
            st.subheader("Wind Speed Trend")
            wind_fig = create_windspeed_chart(df)
            st.plotly_chart(wind_fig, use_container_width=True)
            
            # Wind statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Min Wind Speed", f"{df['WindSpeed'].min():.1f} m/s")
            with col2:
                st.metric("Max Wind Speed", f"{df['WindSpeed'].max():.1f} m/s")
            with col3:
                st.metric("Average Wind Speed", f"{df['WindSpeed'].mean():.1f} m/s")
        
        with tab4:
            st.subheader("Solar Radiation Trend")
            if 'SolarDownwardRadiation' in df.columns:
                solar_fig = create_solar_radiation_chart(df)
                st.plotly_chart(solar_fig, use_container_width=True)
                
                # Solar radiation statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Min Solar Radiation", f"{df['SolarDownwardRadiation'].min():.1f} W/m²")
                with col2:
                    st.metric("Max Solar Radiation", f"{df['SolarDownwardRadiation'].max():.1f} W/m²")
                with col3:
                    st.metric("Average Solar Radiation", f"{df['SolarDownwardRadiation'].mean():.1f} W/m²")
            else:
                st.warning("⚠️ Solar radiation data not available in the dataset.")
        
        with tab5:
            st.subheader("Daily Weather Summary")
            if len(df) > 0:
                daily_fig, daily_stats = create_daily_summary_chart(df)
                st.plotly_chart(daily_fig, use_container_width=True)
                
                st.subheader("Daily Statistics Table")
                st.dataframe(daily_stats, use_container_width=True)
        
        with tab6:
            st.subheader("📊 Raw Weather Data")
            # Display formatted dataframe
            display_df = df[['DateTime', 'Temperature', 'WindSpeed']].copy()
            st.dataframe(display_df, use_container_width=True)
            
            # Basic statistics
            st.subheader("📈 Statistical Summary")
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            if len(numeric_cols) > 0:
                stats_df = df[numeric_cols].describe().round(2)
                st.dataframe(stats_df, use_container_width=True)
            
            # Dataset info
            st.subheader("ℹ️ Dataset Information")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Records", len(df))
            with col2:
                st.metric("Date Range (Days)", len(df['Date'].unique()))
            with col3:
                st.metric("Hours of Data", len(df))
    
    else:
        st.warning("⚠️ No weather data available")
        st.info("Click 'Refresh Weather Data' to load weather data, or configure your API key in the Settings tab.")
        
        # Show setup instructions
        with st.expander("📋 How to get Weather API access"):
            display_weather_setup_instructions()

# Only call show() if this script is run directly (not imported)
if __name__ == "__main__":
    show()