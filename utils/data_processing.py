import pandas as pd
from datetime import datetime

def create_weather_dataframe(weather_data):
    """Convert weather JSON data to pandas DataFrame"""

    df = pd.DataFrame(weather_data)
    
    # Convert datetime strings to datetime objects
    df['valid_datetime'] = pd.to_datetime(df['valid_datetime'])
    df['ref_datetime'] = pd.to_datetime(df['ref_datetime'])
    
    # Create a more readable datetime column for display
    df['DateTime'] = df['valid_datetime'].dt.strftime('%Y-%m-%d %H:%M')
    df['Date'] = df['valid_datetime'].dt.date
    df['Hour'] = df['valid_datetime'].dt.hour
    
    return df