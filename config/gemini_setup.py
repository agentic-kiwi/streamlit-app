import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

def check_password():
    """First security layer - password protection"""
    def password_entered():
        if st.session_state["password"] == st.secrets.get("APP_PASSWORD", "demo123"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("### 🔐 App Access")
        st.text_input("App Password", type="password", on_change=password_entered, key="password", placeholder="Enter app password...")
        st.info("💡 Default password is 'demo123' - ask admin to change it in app settings")
        st.markdown("---")
        return False
    elif not st.session_state["password_correct"]:
        st.markdown("### 🔐 App Access")
        st.text_input("App Password", type="password", on_change=password_entered, key="password", placeholder="Enter app password...")
        st.error("❌ Incorrect password")
        st.info("💡 Contact admin if you need the current password")
        st.markdown("---")
        return False
    return True

def get_user_api_key():
    """Second security layer - user provides their own API key with persistence"""
    # Initialize session state for API key
    if "user_api_key" not in st.session_state:
        st.session_state.user_api_key = ""
    
    # Show current status
    if st.session_state.user_api_key:
        st.sidebar.success("✅ API Key Connected")
        col1, col2 = st.sidebar.columns([3, 1])
        with col1:
            st.sidebar.text("Key: " + "*" * 8 + st.session_state.user_api_key[-4:])
        with col2:
            if st.sidebar.button("🔄", help="Change API Key"):
                st.session_state.user_api_key = ""
                st.rerun()
        return st.session_state.user_api_key
    
    # Input for new API key
    api_key = st.sidebar.text_input(
        "Your Google API Key", 
        type="password",
        help="Get your API key from https://aistudio.google.com/app/apikey",
        placeholder="Enter your Google Gemini API key..."
    )
    
    if api_key:
        # Validate API key format (basic check)
        if api_key.startswith("AIza") and len(api_key) > 30:
            st.session_state.user_api_key = api_key
            st.sidebar.success("API Key saved for this session!")
            st.rerun()
        else:
            st.sidebar.error("Invalid API key format. Should start with 'AIza'")
            return None
    else:
        st.sidebar.warning("Please enter your Google API Key")
        st.sidebar.info("💡 This ensures you control your own usage and costs")
        st.sidebar.markdown("[Get your API key →](https://aistudio.google.com/app/apikey)")
        return None
    
    return api_key

def get_gemini_model(model_name="gemini-2.5-flash", temperature=0.7, api_key=None):
    """Create and return a Gemini model instance using provided API key."""
    
    if not api_key:
        raise ValueError("API key is required!")
    
    model = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=temperature
    )
    
    return model

def get_topic():
    """Get the current learning topic from environment or Streamlit secrets."""
    if hasattr(st, 'secrets') and 'CURRENT_TOPIC' in st.secrets:
        return st.secrets['CURRENT_TOPIC']
    return os.getenv("CURRENT_TOPIC", "RAG")