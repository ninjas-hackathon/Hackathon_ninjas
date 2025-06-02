import streamlit as st
import google.generativeai as genai
from langchain_core.messages import AIMessage, HumanMessage
from config import initialize_gemini

def generate_ai_response(user_input, chat_history, weather_data=None):
    """Generate AI response using Google Gemini API"""
    model = initialize_gemini()
    
    if not model:
        return "Please configure your Google API key in the Settings tab."
    
    try:
        # Check available models (for debugging, only once)
        if not hasattr(generate_ai_response, 'models_checked'):
            try:
                available_models = list(genai.list_models())
                st.write("Available models:", [m.name for m in available_models[:5]])
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