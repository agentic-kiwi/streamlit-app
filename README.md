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
```

### 4. Use Your App

- Enter your app password
- Enter your Google API key
- Start learning!