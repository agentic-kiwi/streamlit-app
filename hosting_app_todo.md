# Complete Template Repository Setup InstructionsStep 
## 1: Prepare Your Code for Template Repository1.

### 1 Create Streamlit App File

```
bash

touch streamlit_app.py

```
Already actioned

### 1.2 Create Web Requirements File

```
bash
pip freeze > requirements.txt
echo "streamlit" >> requirements.txt

```
### 1.3 Update config/gemini_setup.py for Dual Security

```
python
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
        st.text_input("App Password", type="password", on_change=password_entered, key="password")
        st.info("Enter the app password to continue")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("App Password", type="password", on_change=password_entered, key="password")
        st.error("Incorrect password")
        return False
    return True

def get_user_api_key():
    """Second security layer - user provides their own API key"""
    api_key = st.sidebar.text_input(
        "Your Google API Key", 
        type="password",
        help="Get your API key from https://aistudio.google.com/app/apikey"
    )
    
    if not api_key:
        st.sidebar.warning("Please enter your Google API Key")
        st.sidebar.info("This ensures you control your own usage and costs")
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

```

## Step 2: Create Documentation Files

# AI Learning Assistant

A personalized AI tutor built with LangChain and Google Gemini that provides multiple analysis modes for learning any topic.

## Features

- **Basic Q&A**: Quick questions and answers
- **Structured Analysis**: Organized learning content with defined fields
- **Conversational Chat**: Memory-enabled conversations
- **Parallel Analysis**: Multiple expert perspectives simultaneously

## Quick Start

### 1. Get Your Google API Key
- Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
- Create a new API key
- Keep it secure - you'll enter it in the app

### 2. Deploy to Streamlit
- Fork this repository
- Go to [share.streamlit.io](https://share.streamlit.io)
- Sign in with GitHub
- Click "New app" and select your forked repo
- Set main file to `streamlit_app.py`
- Click Deploy

### 3. Configure Your App
- In Streamlit Cloud, go to app settings > Secrets
- Add your configuration:
```toml
APP_PASSWORD = "your_chosen_password"
CURRENT_TOPIC = "your_learning_topic"

4. Use Your App

Enter your app password
Enter your Google API key
Start learning!
```

### Step 3: GitHub Repository Setup

```
bash

git add .
git commit -m "Prepare for template repository - add Streamlit interface and dual security"
git push origin main

```
## 3.2 Make Repository a Template

- Go to your GitHub repository
- Click Settings tab
- Scroll down to "Template repository" section
- Check "Template repository" box
- Save changes

## 3.3 Add Repository Topics
Add these topics to help users find your template:

- streamlit
- langchain
- ai-tutor
- gemini
- learning-assistant

### Step 4: Create Usage Instructions for Users

## 4.1 Update README with Clear Instructions

Include step-by-step deployment guide, API key setup, and customization options.

## 4.2 Test the Template

1.  Use your own template to create a new repository
2. Deploy it to verify the process works
3. Test all security layers and functionality

This approach gives each user complete ownership of their instance while minimizing your ongoing maintenance burden. Users can customize their learning topics, control their costs, and deploy independently.