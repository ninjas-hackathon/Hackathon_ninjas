import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import entsoeController as entsoe
from config import ENERGY_COUNTRY_CODES

def fetch_energy_prices():
    """Fetch energy prices using the entsoeController"""
    try:
        # Set date range
        start = pd.Timestamp('20250601', tz='Europe/Brussels')
        end = pd.Timestamp('20250602', tz='Europe/Brussels')
        
        dfs = []
        for country_code in ENERGY_COUNTRY_CODES:
            df = entsoe.get_day_ahead_prices(country_code, start=start, end=end)
            df.name = country_code
            dfs.append(df)
        
        combined_df = pd.concat(dfs, axis=1)
        return combined_df
        
    except Exception as e:
        st.error(f"❌ Error fetching energy prices: {e}")
        return None

def display_energy_prices(prices_df):
    """Display energy prices with visualization"""
    if prices_df is not None:
        st.success("✅ Energy prices fetched successfully!")
        st.dataframe(prices_df, use_container_width=True)
        
        # Create visualization
        fig, ax = plt.subplots(figsize=(10, 5))
        prices_df.plot(ax=ax, title='Day Ahead Prices', ylabel='EUR/MWh', xlabel='Time')
        st.pyplot(fig)
    else:
        st.error("Failed to fetch energy prices")