
import streamlit as st
from streamlit_chat import message
from langchain_core.messages import AIMessage, HumanMessage
import requests
import pandas as pd
import google.generativeai as genai
import entsoeController as entsoe
import matplotlib.pyplot as plt
from entsoe import EntsoePandasClient

# Initialize Google Gemini API
GOOGLE_API_KEY = 'AIzaSyBJiitah4ELmIRv4G1CLtAk2LmxcTrbQAw'  # Insert your actual Google API key here
genai.configure(api_key=GOOGLE_API_KEY)

# Try to use the latest Gemini model
try:
    model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model name
except:
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')  # Alternative model
    except:
        model = genai.GenerativeModel('models/gemini-1.5-flash')  # With models/ prefix

# Weather API call
your_weather_api_key = 'CBzCpmJBH5PzBr8AmQcS43TnfRGRCukE2v4tIkm9smE'  # Insert your actual Rebase Energy API key
url = "https://api.rebase.energy/weather/v2/query"

# Only make the weather API call if API key is provided
if your_weather_api_key:
    try:
        # Check if API key format is correct (should start with 'Bearer ' or be a token)
        if not your_weather_api_key.startswith('Bearer '):
            headers = {"Authorization": f"Bearer {your_weather_api_key}"}
        else:
            headers = {"Authorization": your_weather_api_key}
        
        params = {
            'model': 'DWD_ICON-EU',
            'start-date': '2023-02-01',
            'end-date': '2023-02-03',
            'latitude': '60.1, 61.2, 59.33',
            'longitude': '17.2, 13.1, 18.05',
            'variables': 'Temperature, WindSpeed',
            'output-format': 'json',
            'output-schema': 'list'
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        # Check response status
        if response.status_code == 401:
            st.error("❌ Weather API: Unauthorized - Please check your API key")
            st.info("Make sure your Rebase Energy API key is correct and has the right permissions")
            df = pd.DataFrame()
        elif response.status_code == 403:
            st.error("❌ Weather API: Forbidden - API key doesn't have access to this endpoint")
            df = pd.DataFrame()
        elif response.status_code != 200:
            st.error(f"❌ Weather API Error: Status code {response.status_code}")
            st.write("Response:", response.text)
            df = pd.DataFrame()
        else:
            json_data = response.json()
            st.success("✅ Weather API connected successfully!")
            
            # Convert to DataFrame
            if isinstance(json_data, list):
                df = pd.DataFrame(json_data)
            elif isinstance(json_data, dict) and 'data' in json_data:
                df = pd.DataFrame(json_data['data'])
            else:
                st.warning("Unexpected JSON format from weather API")
                st.write("Raw JSON data:", json_data)
                df = pd.DataFrame()
            
            # Display the DataFrame
            if not df.empty:
                st.title("Weather Data from Rebase Energy API")
                st.write("Weather data for specified locations:")
                st.dataframe(df)
                
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Network error fetching weather data: {e}")
        df = pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error processing weather data: {e}")
        df = pd.DataFrame()
else:
    df = pd.DataFrame()
    st.info("💡 Add your Rebase Energy API key to the `your_weather_api_key` variable to display weather data")
    st.markdown("""
    **To get a Rebase Energy API key:**
    1. Visit [Rebase Energy](https://www.rebase.energy/)
    2. Sign up for an account
    3. Get your API key from the dashboard
    4. Add it to the code above
    """)

# Function to generate AI response using Google Gemini API
def generate_ai_response(user_input, chat_history, weather_data=None):
    try:
        # First, let's check what models are available (for debugging)
        if not hasattr(generate_ai_response, 'models_checked'):
            try:
                available_models = list(genai.list_models())
                st.write("Available models:", [m.name for m in available_models[:5]])  # Show first 5
                generate_ai_response.models_checked = True
            except:
                pass
        
        # Prepare context with weather data if available
        context = ""
        if weather_data is not None and not weather_data.empty:
            context = f"\n\nAvailable weather data:\n{weather_data.to_string()}\n\n"
        
        # Prepare chat history for context
        history_context = ""
        for msg in chat_history[-10:]:  # Include last 10 messages for context
            if isinstance(msg, HumanMessage):
                history_context += f"User: {msg.content}\n"
            elif isinstance(msg, AIMessage):
                history_context += f"Assistant: {msg.content}\n"
        
        # Create the prompt
        prompt = f"""You are a helpful assistant with access to weather data. {context}

Previous conversation:
{history_context}

Current question: {user_input}

Please provide a helpful and informative response. If the user asks about weather and you have weather data available, use that information in your response."""

        # Try different ways to make the API call
        try:
            # Method 1: Direct generation
            response = model.generate_content(prompt)
            return response.text
        except Exception as e1:
            try:
                # Method 2: With generation config
                generation_config = genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=1000,
                )
                response = model.generate_content(prompt, generation_config=generation_config)
                return response.text
            except Exception as e2:
                # Method 3: Try with a different model
                try:
                    backup_model = genai.GenerativeModel('models/gemini-1.5-flash')
                    response = backup_model.generate_content(prompt)
                    return response.text
                except Exception as e3:
                    return f"API Error: {str(e1)}. Tried alternative methods but failed. Please check your API key and try again."
        
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}. Please make sure your Google API key is set correctly and you have access to the Gemini API."

# Set up the Streamlit app
st.title("🤖 AI Assistant with Weather Data")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to handle user input and generate response
def handle_input(user_input):
    # Add user message to session state
    user_message = HumanMessage(content=user_input)
    st.session_state.messages.append(user_message)
    
    # Generate AI response using Google Gemini API
    ai_response_text = generate_ai_response(
        user_input, 
        st.session_state.messages, 
        df if not df.empty else None
    )
    
    # Add AI message to session state
    ai_message = AIMessage(content=ai_response_text)
    st.session_state.messages.append(ai_message)
    
    return ai_response_text

# Create tabs for different views
tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Chat", "🌤️ Weather Data", "⚙️ Settings", "📖 Instructions", "Energy Prices"])

with tab1:
    st.header("Chat with Gemini AI")
    
    # Display chat messages
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            message(msg.content, is_user=True)
        elif isinstance(msg, AIMessage):
            message(msg.content, is_user=False)
    
    # Input box for user to type messages
    user_input = st.text_input("You:", key="user_input")
    
    # Create two columns for buttons
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Send", type="primary"):
            if user_input:
                if not GOOGLE_API_KEY:
                    st.error("Please set your Google API key in the Settings tab.")
                else:
                    with st.spinner("Generating response..."):
                        response = handle_input(user_input)
                    # Clear the input box by rerunning the app
                    st.rerun()
            else:
                st.warning("Please enter a message before sending.")
    
    with col2:
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    # Show chat statistics
    if st.session_state.messages:
        st.sidebar.metric("Messages", len(st.session_state.messages))
        st.sidebar.metric("User Messages", len([m for m in st.session_state.messages if isinstance(m, HumanMessage)]))
        st.sidebar.metric("AI Messages", len([m for m in st.session_state.messages if isinstance(m, AIMessage)]))

with tab2:
    st.header("Weather Data Analysis")
    
    if not df.empty:
        st.success("✅ Weather data loaded successfully!")
        
        # Weather data display with better formatting
        st.subheader("📊 Raw Weather Data")
        st.dataframe(df, use_container_width=True)
        
        # Basic statistics if data is available
        if not df.empty:
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
        st.info("Configure your weather API key in the Settings tab to load weather data.")

with tab3:
    st.header("⚙️ Configuration Settings")
    
    st.subheader("🔑 API Keys")
    
    # Google API Key status
    if GOOGLE_API_KEY:
        st.success("✅ Google API Key: Configured")
    else:
        st.error("❌ Google API Key: Not configured")
        st.code("GOOGLE_API_KEY = 'your-api-key-here'")
    
    # Weather API Key status
    if your_weather_api_key:
        st.success("✅ Weather API Key: Configured")
    else:
        st.warning("⚠️ Weather API Key: Not configured")
        st.code("your_weather_api_key = 'your-weather-api-key-here'")
    
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
        except:
            st.write("Could not fetch available models")
    
    st.subheader("📊 Current Session Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Chat Messages", len(st.session_state.messages))
    with col2:
        weather_status = "✅ Loaded" if not df.empty else "❌ Not loaded"
        st.metric("Weather Data", weather_status)

with tab4:
    st.header("📖 Instructions & Setup")
    
    st.subheader("🚀 Quick Start")
    st.markdown("""
    1. **Configure API Keys** in the Settings tab
    2. **Load Weather Data** (optional) 
    3. **Start Chatting** in the Chat tab
    """)
    
    st.subheader("🔧 Installation")
    st.code("""
pip install google-generativeai streamlit streamlit-chat langchain-core pandas requests
    """)
    
    st.subheader("🔑 Getting API Keys")
    
    with st.expander("Google Gemini API Key"):
        st.markdown("""
        1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
        2. Sign in with your Google account
        3. Create a new API key
        4. Copy and paste it into the code
        5. Make sure Gemini API is available in your region
        """)
    
    with st.expander("Weather API Key (Optional)"):
        st.markdown("""
        1. Visit [Rebase Energy](https://www.rebase.energy/)
        2. Sign up for an account
        3. Get your API key from the dashboard
        4. Add it to the `your_weather_api_key` variable
        
        **Note:** Weather data is optional - the chat will work without it.
        """)
    
    st.subheader("✨ Features")
    st.markdown("""
    - **💬 AI Chat:** Powered by Google Gemini
    - **🌤️ Weather Integration:** AI can reference weather data in responses
    - **📊 Data Analysis:** View and analyze weather data
    - **⚙️ Configuration:** Easy setup and monitoring
    - **🗂️ Organized Interface:** Tabbed layout for better UX
    """)
    
    st.subheader("🆘 Troubleshooting")
    st.markdown("""
    - **Chat not working?** Check your Google API key in Settings
    - **Weather data not loading?** Check your weather API key and permissions
    - **Model errors?** Try different Gemini model names in the code
    - **Regional issues?** Some APIs may not be available in all regions
    """)

with tab5:
    # use the entsoeController to fetch energy prices
    st.header("💡 Energy Prices")
    st.markdown("""
    This tab will display energy prices using the `entsoeController` module.
    Make sure you have the `entsoe` package installed and configured with your API key.
    """)
    if 'entsoe_prices' not in st.session_state:
        st.session_state.entsoe_prices = None
    if st.button("Fetch Energy Prices"):
        try:
            # Fetch energy prices using the entsoeController
            start = pd.Timestamp('20250601', tz='Europe/Brussels')
            end = pd.Timestamp('20250602', tz='Europe/Brussels')
            country_codes = ["SE_3", "SE_4"]
            
            dfs = []
            for country_code in country_codes:
                df = entsoe.get_day_ahead_prices(country_code, start=start, end=end)
                df.name = country_code
                dfs.append(df)
            
            combined_df = pd.concat(dfs, axis=1)
            st.session_state.entsoe_prices = combined_df
            
            st.success("✅ Energy prices fetched successfully!")
            st.dataframe(combined_df, use_container_width=True)
            # visualize the prices
            fig, ax = plt.subplots(figsize=(10, 5))
            combined_df.plot(ax=ax, title='Day Ahead Prices', ylabel='EUR/MWh', xlabel='Time')
            st.pyplot(fig)
        except Exception as e:
            st.error(f"❌ Error fetching energy prices: {e}")
    else:
        if st.session_state.entsoe_prices is not None:
            st.success("✅ Energy prices loaded from previous fetch!")
            st.dataframe(st.session_state.entsoe_prices, use_container_width=True)
        else:
            st.info("Click the button above to fetch energy prices.")
# Streamlit app for AI Assistant with Weather Data and Energy Prices

# Footer
st.markdown("""
---
🚀 **Multi-Tab AI Assistant** | Made with ❤️ using [Streamlit](https://streamlit.io), [Google Gemini](https://ai.google.dev), and [LangChain](https://langchain.com)
""")