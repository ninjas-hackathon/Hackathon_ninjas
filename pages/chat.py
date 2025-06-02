import streamlit as st
from streamlit_chat import message
from langchain_core.messages import AIMessage, HumanMessage
from utils.session_state import get_chat_messages, add_message, clear_chat, get_weather_data
from utils.ai_helper import generate_ai_response
from config import GOOGLE_API_KEY

def show():
    """Display the chat page"""
    st.header("Chat with Gemini AI")
    
    messages = get_chat_messages()
    weather_data = get_weather_data()
    
    # Display chat messages
    for msg in messages:
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
                        response = handle_input(user_input, weather_data)
                    st.rerun()
            else:
                st.warning("Please enter a message before sending.")
    
    with col2:
        if st.button("Clear Chat"):
            clear_chat()
            st.rerun()
    
    # Show chat statistics in sidebar
    if messages:
        st.sidebar.metric("Messages", len(messages))
        st.sidebar.metric("User Messages", len([m for m in messages if isinstance(m, HumanMessage)]))
        st.sidebar.metric("AI Messages", len([m for m in messages if isinstance(m, AIMessage)]))

def handle_input(user_input, weather_data):
    """Handle user input and generate AI response"""
    # Add user message to session state
    user_message = HumanMessage(content=user_input)
    add_message(user_message)
    
    # Generate AI response using Google Gemini API
    messages = get_chat_messages()
    ai_response_text = generate_ai_response(
        user_input, 
        messages, 
        weather_data if not weather_data.empty else None
    )
    
    # Add AI message to session state
    ai_message = AIMessage(content=ai_response_text)
    add_message(ai_message)
    
    return ai_response_text

show()