import streamlit as st
import hashlib
import json
import os
from datetime import datetime
from typing import Dict, Optional

class UserAuth:
    def __init__(self):
        self.users_file = "auth/users.json"
        self.ensure_auth_dir()
        self.load_users()
    
    def ensure_auth_dir(self):
        """Ensure auth directory exists"""
        os.makedirs("auth", exist_ok=True)
    
    def load_users(self):
        """Load users from JSON file"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
            else:
                self.users = {}
        except:
            self.users = {}
    
    def save_users(self):
        """Save users to JSON file"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=2)
        except:
            pass
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username: str, password: str, email: str) -> bool:
        """Create a new user account"""
        if username in self.users:
            return False
        
        self.users[username] = {
            "password": self.hash_password(password),
            "email": email,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "api_key": None
        }
        self.save_users()
        return True
    
    def verify_user(self, username: str, password: str) -> bool:
        """Verify user credentials"""
        if username not in self.users:
            return False
        
        stored_password = self.users[username]["password"]
        return stored_password == self.hash_password(password)
    
    def login(self, username: str, password: str) -> bool:
        """Login user and update session"""
        if self.verify_user(username, password):
            # Update last login
            self.users[username]["last_login"] = datetime.now().isoformat()
            self.save_users()
            
            # Set session state
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.user_data = self.users[username]
            return True
        return False
    
    def logout(self):
        """Logout user and clear session"""
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.user_data = None
        if "user_api_key" in st.session_state:
            del st.session_state.user_api_key
    
    def save_user_api_key(self, username: str, api_key: str):
        """Save user's API key"""
        if username in self.users:
            self.users[username]["api_key"] = api_key
            self.save_users()
            # Reload users to ensure data is fresh
            self.load_users()
            return True
        return False
    
    def get_user_api_key(self, username: str) -> Optional[str]:
        """Get user's saved API key"""
        # Reload users to get latest data
        self.load_users()
        if username in self.users:
            return self.users[username].get("api_key")
        return None
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return st.session_state.get("authenticated", False)
    
    def get_current_user(self) -> Optional[str]:
        """Get current logged in user"""
        if self.is_authenticated():
            return st.session_state.get("username")
        return None

def show_auth_page():
    """Show login/signup page"""
    auth = UserAuth()
    
    st.markdown("""
    <div style="text-align: center;">
        <h1>🤖 AI Learning Assistant</h1>
        <p>Your personalized AI tutor powered by Google Gemini</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for login and signup
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])
    
    with tab1:
        st.subheader("Welcome Back!")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                login_button = st.form_submit_button("🔑 Login", use_container_width=True)
            
            if login_button:
                if username and password:
                    if auth.login(username, password):
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.warning("⚠️ Please fill in all fields")
    
    with tab2:
        st.subheader("Create Your Account")
        
        with st.form("signup_form"):
            new_username = st.text_input("Choose Username", placeholder="Enter a unique username")
            new_email = st.text_input("Email", placeholder="Enter your email address")
            new_password = st.text_input("Password", type="password", placeholder="Choose a strong password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                signup_button = st.form_submit_button("📝 Sign Up", use_container_width=True)
            
            if signup_button:
                if new_username and new_email and new_password and confirm_password:
                    if new_password != confirm_password:
                        st.error("❌ Passwords don't match")
                    elif len(new_password) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    elif new_username in auth.users:
                        st.error("❌ Username already exists")
                    else:
                        if auth.create_user(new_username, new_password, new_email):
                            st.success("✅ Account created successfully! Please login.")
                            st.info("💡 Switch to the Login tab to access your account")
                        else:
                            st.error("❌ Failed to create account")
                else:
                    st.warning("⚠️ Please fill in all fields")
    
    # Add some helpful info
    st.markdown("---")
    st.markdown("""
    ### 🌟 Features
    - **Quick Answer**: Fast, straightforward responses
    - **Deep Dive**: Comprehensive explanations with examples
    - **Multiple Viewpoints**: Different expert perspectives
    - **Interactive Tutor**: Memory-enabled conversations
    
    ### 🔐 Security
    - Your account data is stored locally
    - You provide your own Google API key
    - No data is shared with third parties
    """)

def check_authentication():
    """Check if user is authenticated, show auth page if not"""
    auth = UserAuth()
    
    if not auth.is_authenticated():
        show_auth_page()
        return False, None
    
    return True, auth

def show_user_info():
    """Show user info in sidebar"""
    auth = UserAuth()
    current_user = auth.get_current_user()
    
    if current_user:
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"👤 **Logged in as:** {current_user}")
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            auth.logout()
            st.rerun()