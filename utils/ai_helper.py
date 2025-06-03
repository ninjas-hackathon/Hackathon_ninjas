import streamlit as st
import google.generativeai as genai
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from config import initialize_gemini
import pandas as pd
from datetime import datetime, timedelta
from utils.data_processing import create_weather_dataframe 

def create_energy_advisor_prompt():
    """Create a comprehensive prompt template for energy usage advice"""
    
    system_template = """You are an expert Energy Usage Advisor with access to weather forecasts and day-ahead energy pricing data. 
    Your role is to help users optimize their energy consumption based on:
    1. Weather conditions (temperature, solar radiation, wind, etc.)
    2. Energy price fluctuations throughout the day
    3. Typical household energy usage patterns
    
    Key principles for your advice:
    - Recommend high-energy activities (washing, drying, heating, cooling) during LOW price periods
    - Consider weather impact on energy needs (heating/cooling requirements)
    - Factor in solar generation potential for users with solar panels
    - Suggest load shifting strategies to save money
    - Provide specific time recommendations when possible
    - Consider comfort vs. cost trade-offs
    
    Always be practical and consider real-world constraints in your recommendations."""
    
    human_template = """Current Context:
    
    WEATHER FORECAST DATA:
    {weather_data}
    
    DAY-AHEAD ENERGY PRICES:
    {energy_prices}
    
    CONVERSATION HISTORY:
    {chat_history}
    
    CURRENT QUESTION: {user_input}
    
    Please provide specific, actionable advice for optimizing energy usage based on the available data. 
    Include timing recommendations and explain your reasoning."""
    
    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(human_template)
    ])

def format_weather_data(weather_data):
    """Format weather data for the prompt"""
    if weather_data is None or weather_data.empty:
        return "No weather data available"
    
    # Assuming weather_data has columns like: datetime, temperature, humidity, solar_radiation, wind_speed
    formatted = "Weather Forecast Summary:\n"
    
    if 'datetime' in weather_data.columns:
        for _, row in weather_data.head(24).iterrows():  # Next 24 hours
            formatted += f"- {row.get('datetime', 'N/A')}: "
            formatted += f"Temp: {row.get('temperature', 'N/A')}°C, "
            formatted += f"Humidity: {row.get('humidity', 'N/A')}%, "
            formatted += f"Solar: {row.get('solar_radiation', 'N/A')} W/m², "
            formatted += f"Wind: {row.get('wind_speed', 'N/A')} m/s\n"
    else:
        formatted += weather_data.to_string()
    
    return formatted

def format_energy_prices(energy_prices):
    """Format energy price data for the prompt"""
    if energy_prices is None or energy_prices.empty:
        return "No energy price data available"
    
    formatted = "Day-Ahead Energy Prices:\n"
    
    if 'hour' in energy_prices.columns and 'price' in energy_prices.columns:
        for _, row in energy_prices.iterrows():
            hour = row.get('hour', 'N/A')
            price = row.get('price', 'N/A')
            formatted += f"- Hour {hour}:00 - {price} €/MWh\n"
    else:
        formatted += energy_prices.to_string()
    
    # Add price analysis
    if 'price' in energy_prices.columns:
        min_price = energy_prices['price'].min()
        max_price = energy_prices['price'].max()
        avg_price = energy_prices['price'].mean()
        
        cheapest_hours = energy_prices.nsmallest(3, 'price')
        expensive_hours = energy_prices.nlargest(3, 'price')
        
        formatted += f"\nPrice Analysis:\n"
        formatted += f"- Average price: {avg_price:.2f} €/MWh\n"
        formatted += f"- Cheapest hours: {', '.join([str(h) + ':00' for h in cheapest_hours['hour']])}\n"
        formatted += f"- Most expensive hours: {', '.join([str(h) + ':00' for h in expensive_hours['hour']])}\n"
    
    return formatted

def format_chat_history(chat_history):
    """Format chat history for context"""
    if not chat_history:
        return "No previous conversation"
    
    history_text = ""
    for msg in chat_history[-6:]:  # Last 6 messages for context
        if isinstance(msg, HumanMessage):
            history_text += f"User: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            history_text += f"Assistant: {msg.content}\n"
    
    return history_text if history_text else "No previous conversation"

def generate_ai_response(user_input, chat_history, weather_data=None, energy_prices=None):
    """Generate AI response using LangChain and Google Gemini API"""
    
    try:
        # Initialize the LangChain ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.7,
            max_output_tokens=1000,
            google_api_key=st.secrets.get("GOOGLE_API_KEY") or st.session_state.get("google_api_key")
        )
        
        # Create the prompt template
        prompt_template = create_energy_advisor_prompt()
        
        # Format the data
        formatted_weather = create_weather_dataframe(weather_data)
        formatted_prices = format_energy_prices(energy_prices)
        formatted_history = format_chat_history(chat_history)
        
        # Create the prompt
        messages = prompt_template.format_messages(
            weather_data=formatted_weather,
            energy_prices=formatted_prices,
            chat_history=formatted_history,
            user_input=user_input
        )
        
        # Generate response
        response = llm.invoke(messages)
        return response.content
        
    except Exception as e:
        # Fallback to the original method if LangChain fails
        return generate_ai_response_fallback(user_input, chat_history, weather_data, energy_prices, str(e))

def generate_ai_response_fallback(user_input, chat_history, weather_data=None, energy_prices=None, error_msg=""):
    """Fallback method using direct Google Gemini API"""
    model = initialize_gemini()
    if not model:
        return "Please configure your Google API key in the Settings tab."
    
    try:
        # Prepare comprehensive context
        context = "You are an Energy Usage Advisor. Help users optimize their energy consumption.\n\n"
        
        if weather_data is not None and not weather_data.empty:
            context += f"WEATHER FORECAST:\n{format_weather_data(weather_data)}\n\n"
        
        if energy_prices is not None and not energy_prices.empty:
            context += f"ENERGY PRICES:\n{format_energy_prices(energy_prices)}\n\n"
        
        # Add chat history
        history_context = format_chat_history(chat_history)
        context += f"CONVERSATION HISTORY:\n{history_context}\n\n"
        
        # Create the full prompt
        prompt = f"""{context}
Based on the weather forecast and energy price data above, please provide specific advice for when to use energy-intensive appliances and activities. Consider:
1. Times when energy is cheapest
2. Weather conditions affecting heating/cooling needs
3. Opportunities for load shifting
4. Solar generation potential (if applicable)

Current question: {user_input}

Provide practical, actionable recommendations with specific timing when possible."""
        
        # Generate response
        response = model.generate_content(prompt)
        
        if error_msg:
            return f"(Using fallback method due to: {error_msg})\n\n{response.text}"
        else:
            return response.text
            
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}. Please make sure your Google API key is set correctly."
