import streamlit as st

def show():
    """Display the instructions page"""
    st.header("📖 Instructions & Setup")
    
    st.subheader("🚀 Quick Start")
    st.markdown("""
    1. **Configure API Keys** in the Settings tab or `config.py`
    2. **Load Weather Data** (optional) in the Weather Data tab
    3. **Start Chatting** in the Chat tab
    """)
    
    st.subheader("🔧 Installation")
    st.code("""
pip install google-generativeai streamlit streamlit-chat langchain-core pandas requests matplotlib entsoe-py
    """)
    
    st.subheader("📁 Project Structure")
    st.code("""
my_ai_assistant/
├── main.py                 # Entry point
├── config.py              # Configuration and API keys
├── pages/
│   ├── __init__.py
│   ├── chat.py           # Chat interface
│   ├── weather.py        # Weather data display
│   ├── settings.py       # Settings and configuration
│   ├── instructions.py   # This page
│   └── energy_prices.py  # Energy pricing data
├── utils/
│   ├── __init__.py
│   ├── session_state.py  # Session state management
│   ├── weather_api.py    # Weather API functions
│   ├── ai_helper.py      # AI response generation
│   └── energy_api.py     # Energy pricing functions
└── entsoeController.py   # Energy data controller
    """)
    
    st.subheader("🔑 Getting API Keys")
    
    with st.expander("Google Gemini API Key"):
        st.markdown("""
        1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
        2. Sign in with your Google account
        3. Create a new API key
        4. Copy and paste it into `config.py`
        5. Make sure Gemini API is available in your region
        
        **Add to config.py:**
        ```python
        GOOGLE_API_KEY = 'your-actual-api-key-here'
        ```
        """)
    
    with st.expander("Weather API Key (Optional)"):
        st.markdown("""
        1. Visit [Rebase Energy](https://www.rebase.energy/)
        2. Sign up for an account
        3. Get your API key from the dashboard
        4. Add it to `config.py`
        
        **Add to config.py:**
        ```python
        WEATHER_API_KEY = 'your-weather-api-key-here'
        ```
        
        **Note:** Weather data is optional - the chat will work without it.
        """)
    
    with st.expander("ENTSO-E API Key (For Energy Prices)"):
        st.markdown("""
        1. Visit [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/)
        2. Register for an account
        3. Generate an API key in your account settings
        4. Configure it in your `entsoeController.py`
        
        **Note:** Required for energy pricing functionality.
        """)
    
    st.subheader("✨ Features")
    st.markdown("""
    - **💬 AI Chat:** Powered by Google Gemini with context awareness
    - **🌤️ Weather Integration:** AI can reference weather data in responses
    - **💡 Energy Prices:** Real-time energy pricing from ENTSO-E
    - **📊 Data Analysis:** View and analyze weather and energy data
    - **⚙️ Configuration:** Easy setup and monitoring
    - **🗂️ Organized Interface:** Tabbed layout for better UX
    - **🏗️ Modular Architecture:** Clean, maintainable code structure
    """)
    
    st.subheader("🆘 Troubleshooting")
    st.markdown("""
    - **Chat not working?** Check your Google API key in Settings or config.py
    - **Weather data not loading?** Check your weather API key and permissions
    - **Energy prices not working?** Verify ENTSO-E API configuration
    - **Model errors?** Try different Gemini model names in config.py
    - **Import errors?** Make sure all required packages are installed
    - **Regional issues?** Some APIs may not be available in all regions
    """)
    
    st.subheader("🏃‍♂️ Running the Application")
    st.code("""
# Navigate to your project directory
cd my_ai_assistant

# Run the Streamlit app
streamlit run main.py
    """)
    
    st.subheader("🔄 Code Organization Benefits")
    st.markdown("""
    **Why this structure is better:**
    - **Maintainability**: Each component has a single responsibility
    - **Reusability**: Functions can be easily reused across pages
    - **Testing**: Individual components can be tested in isolation
    - **Collaboration**: Multiple developers can work on different parts
    - **Scalability**: Easy to add new features and pages
    - **Debugging**: Easier to locate and fix issues
    """)

show()