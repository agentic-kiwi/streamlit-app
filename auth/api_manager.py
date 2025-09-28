import streamlit as st
from auth.user_auth import UserAuth

def get_user_api_key():
    """Get user's API key with persistence across sessions"""
    auth = UserAuth()
    current_user = auth.get_current_user()
    
    if not current_user:
        return None
    
    # Check if user has saved API key
    saved_api_key = auth.get_user_api_key(current_user)
    
    # Initialize session state with saved key if available
    if "user_api_key" not in st.session_state:
        st.session_state.user_api_key = saved_api_key or ""
    
    # If we have a saved key but session is empty, load it
    if not st.session_state.user_api_key and saved_api_key:
        st.session_state.user_api_key = saved_api_key
    
    # Show current status if API key exists
    if st.session_state.user_api_key:
        st.sidebar.success("✅ API Key Connected")
        if saved_api_key == st.session_state.user_api_key:
            st.sidebar.info("🔐 Using saved API key")
        else:
            st.sidebar.info("📝 Session API key")
            
        col1, col2 = st.sidebar.columns([3, 1])
        with col1:
            masked_key = "*" * 8 + st.session_state.user_api_key[-4:]
            st.sidebar.text(f"Key: {masked_key}")
        with col2:
            if st.sidebar.button("🔄", help="Change API Key", key="change_api_key"):
                st.session_state.user_api_key = ""
                st.rerun()
        return st.session_state.user_api_key
    
    # Input for new API key
    st.sidebar.markdown("### 🔑 API Key Setup")
    
    # Show if user has a saved key
    if saved_api_key:
        st.sidebar.info(f"💡 You have a saved API key ending in ...{saved_api_key[-4:]}")
        if st.sidebar.button("🔑 Load Saved Key", key="load_saved_key"):
            st.session_state.user_api_key = saved_api_key
            st.rerun()
    
    api_key = st.sidebar.text_input(
        "Your Google API Key", 
        type="password",
        help="Get your API key from Google AI Studio",
        placeholder="Enter your Google Gemini API key...",
        key="api_key_input"
    )
    
    # Option to save API key
    save_key = st.sidebar.checkbox("💾 Remember my API key", help="Save API key for future sessions", value=True)
    
    if api_key:
        # Validate API key format
        if api_key.startswith("AIza") and len(api_key) > 30:
            st.session_state.user_api_key = api_key
            
            # Save to user profile if requested
            if save_key:
                auth.save_user_api_key(current_user, api_key)
                st.sidebar.success("🔐 API Key saved to your account!")
            else:
                st.sidebar.success("✅ API Key set for this session!")
            st.rerun()
        else:
            st.sidebar.error("❌ Invalid API key format. Should start with 'AIza'")
            return None
    else:
        st.sidebar.warning("🔑 Please enter your Google API Key")
        st.sidebar.info("💡 This ensures you control your own usage and costs")
        st.sidebar.markdown("[🔗 Get your API key](https://aistudio.google.com/app/apikey)")
        return None
    
    return api_key