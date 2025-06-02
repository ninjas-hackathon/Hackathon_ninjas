import streamlit as st
from utils.energy_api import fetch_energy_prices, display_energy_prices
from utils.session_state import get_energy_prices, set_energy_prices

def show():
    """Display the energy prices page"""
    st.header("💡 Energy Prices")
    st.markdown("""
    This tab displays energy prices using the `entsoeController` module.
    Make sure you have the `entsoe` package installed and configured with your API key.
    """)
    
    # Get current energy prices from session state
    current_prices = get_energy_prices()
    
    # Button to fetch energy prices
    if st.button("Fetch Energy Prices"):
        with st.spinner("Fetching energy prices..."):
            prices_df = fetch_energy_prices()
            if prices_df is not None:
                set_energy_prices(prices_df)
                display_energy_prices(prices_df)
            else:
                st.error("Failed to fetch energy prices. Please check your ENTSO-E API configuration.")
    
    # Display existing prices if available
    elif current_prices is not None:
        st.success("✅ Energy prices loaded from previous fetch!")
        display_energy_prices(current_prices)
    else:
        st.info("Click the button above to fetch energy prices.")
        
        # Show setup instructions
        with st.expander("How to configure ENTSO-E API"):
            st.markdown("""
            **To set up energy price fetching:**
            
            1. **Install the ENTSO-E package:**
            ```bash
            pip install entsoe-py
            ```
            
            2. **Get an API key:**
            - Visit [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/)
            - Register for an account
            - Generate an API key in your account settings
            
            3. **Configure your entsoeController.py:**
            ```python
            from entsoe import EntsoePandasClient
            
            # Your ENTSO-E API key
            API_KEY = 'your-entsoe-api-key-here'
            client = EntsoePandasClient(api_key=API_KEY)
            
            def get_day_ahead_prices(country_code, start, end):
                return client.query_day_ahead_prices(country_code, start=start, end=end)
            ```
            
            4. **Supported country codes:**
            - SE_1, SE_2, SE_3, SE_4 (Sweden zones)
            - DE_LU (Germany/Luxembourg)
            - FR (France)
            - And many more...
            """)
    
    # Show current configuration
    if current_prices is not None:
        st.subheader("📊 Data Information")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Data Points", len(current_prices))
        with col2:
            st.metric("Countries/Zones", len(current_prices.columns))

show()  # Call the show function to display the page content