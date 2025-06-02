import streamlit as st
from pages import chat, weather, settings, instructions, energy_prices
from config import setup_page_config
from utils.session_state import initialize_session_state

# Set up page configuration
setup_page_config()

# Initialize session state
initialize_session_state()



# Footer
st.markdown("""
---
🚀 **Multi-Tab AI Assistant** | Made with ❤️ using [Streamlit](https://streamlit.io), [Google Gemini](https://ai.google.dev), and [LangChain](https://langchain.com)
""")