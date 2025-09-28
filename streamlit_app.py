import streamlit as st
import os
from dotenv import load_dotenv
from chains.basic_qa import ask_question
from chains.conversational import chat_with_memory
from chains.parallel_analysis import analyze_from_multiple_perspectives
from chains.structured_analysis import analyze_topic
from config.gemini_setup import get_gemini_model, get_topic
from langchain.memory import ConversationBufferMemory

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Learning Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_memory" not in st.session_state:
    st.session_state.conversation_memory = ConversationBufferMemory(return_messages=True)
if "current_topic" not in st.session_state:
    st.session_state.current_topic = get_topic()

# Custom CSS for better UI
st.markdown("""
    <style>
    .stChat {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.title("🎓 Learning Assistant Settings")
    
    # Topic management
    st.subheader("📚 Topic Configuration")
    current_topic = st.text_input(
        "Learning Topic",
        value=st.session_state.current_topic,
        help="Enter the topic you want to learn about"
    )
    
    if current_topic != st.session_state.current_topic:
        st.session_state.current_topic = current_topic
        os.environ["CURRENT_TOPIC"] = current_topic
        st.success(f"Topic updated to: {current_topic}")
    
    st.divider()
    
    # Mode selection
    st.subheader("🔧 Chat Mode")
    mode = st.selectbox(
        "How would you like to learn?",
        ["Quick Answer", "Deep Dive", "Multiple Viewpoints", "Interactive Tutor"],
        help="Choose your preferred learning style"
    )
    
    # Mode descriptions
    with st.expander("ℹ️ What's the difference?"):
        st.write("""
        **🚀 Quick Answer**: Get fast, straightforward responses to your questions
        
        **🔍 Deep Dive**: Receive comprehensive explanations with examples and key takeaways
        
        **👥 Multiple Viewpoints**: See the same topic explained from different angles (beginner, practical, technical)
        
        **💬 Interactive Tutor**: Have a back-and-forth conversation where I remember what we discussed
        """)
    
    st.divider()
    
    # Advanced settings
    with st.expander("⚙️ Advanced Settings"):
        temperature = st.slider(
            "Response Creativity",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher values make responses more creative but less focused"
        )
        
        model_name = st.selectbox(
            "Model",
            ["gemini-2.5-flash", "gemini-1.5-pro"],
            help="Select the AI model to use"
        )
    
    st.divider()
    
    # Clear conversation button
    if st.button("🗑️ Clear Conversation", type="secondary", use_container_width=True):
        st.session_state.messages = []
        st.session_state.conversation_memory = ConversationBufferMemory(return_messages=True)
        st.rerun()
    
    # Footer
    st.caption("Built with LangChain & Gemini")

# Main content area
st.title(f"🤖 AI Learning Assistant")

# Display current topic and mode
col1, col2 = st.columns(2)
with col1:
    st.info(f"📖 **Current Topic:** {st.session_state.current_topic}")
with col2:
    st.info(f"🔧 **Mode:** {mode}")

# Message container
message_container = st.container()

# Display chat history
with message_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant" and "type" in message:
                if message["type"] == "structured":
                    st.markdown("### 🔍 Deep Dive Analysis")
                    st.json(message["content"])
                elif message["type"] == "parallel":
                    st.markdown("### 👥 Multiple Viewpoints")
                    for perspective, content in message["content"].items():
                        with st.expander(f"**{perspective.capitalize()} Perspective**", expanded=True):
                            st.write(content)
                else:
                    st.markdown(message["content"])
            else:
                st.markdown(message["content"])

# Input area
if prompt := st.chat_input("Ask me anything about " + st.session_state.current_topic + "..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                if mode == "Quick Answer":
                    response = ask_question(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })
                
                elif mode == "Deep Dive":
                    response = analyze_topic(prompt)
                    st.markdown("### 🔍 Deep Dive Analysis")
                    
                    # Try to parse as structured data
                    try:
                        import json
                        if isinstance(response, str):
                            # Try to extract JSON from the response
                            if "{" in response and "}" in response:
                                json_start = response.find("{")
                                json_end = response.rfind("}") + 1
                                json_str = response[json_start:json_end]
                                structured_data = json.loads(json_str)
                                
                                # Display structured data nicely
                                if "topic" in structured_data:
                                    st.subheader(f"Topic: {structured_data['topic']}")
                                if "key_concepts" in structured_data:
                                    st.write("**Key Concepts:**")
                                    for concept in structured_data["key_concepts"]:
                                        st.write(f"• {concept}")
                                if "explanation" in structured_data:
                                    st.write("**Explanation:**")
                                    st.write(structured_data["explanation"])
                                if "practical_examples" in structured_data:
                                    st.write("**Practical Examples:**")
                                    for example in structured_data["practical_examples"]:
                                        st.write(f"• {example}")
                                if "summary" in structured_data:
                                    st.write("**Summary:**")
                                    st.write(structured_data["summary"])
                            else:
                                st.write(response)
                        else:
                            st.json(response)
                    except:
                        # Fallback to plain text display
                        st.write(response)
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "type": "structured",
                        "content": response
                    })
                
                elif mode == "Multiple Viewpoints":
                    results = analyze_from_multiple_perspectives(prompt)
                    st.markdown("### 👥 Multiple Viewpoints")
                    
                    perspectives_content = {}
                    for perspective, response in results.items():
                        with st.expander(f"**{perspective.capitalize()} Perspective**", expanded=True):
                            content = response.content if hasattr(response, 'content') else str(response)
                            st.write(content)
                            perspectives_content[perspective] = content
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "type": "parallel",
                        "content": perspectives_content
                    })
                
                elif mode == "Interactive Tutor":
                    # Use the conversational chain with memory
                    chat_history = st.session_state.conversation_memory.chat_memory.messages
                    
                    # Get response using the existing chain
                    from langchain_core.prompts import ChatPromptTemplate
                    from config.gemini_setup import get_gemini_model
                    
                    template = ChatPromptTemplate.from_messages([
                        ("system", f"You are a helpful and fun tutor who understands {st.session_state.current_topic} well. You will always respond in simple terms and explain the foundations clearly."),
                        ("placeholder", "{chat_history}"),
                        ("human", "{question}")
                    ])
                    
                    chain = template | get_gemini_model()
                    response = chain.invoke({
                        "question": prompt,
                        "chat_history": chat_history
                    })
                    
                    response_content = response.content if hasattr(response, 'content') else str(response)
                    st.markdown(response_content)
                    
                    # Save to memory
                    st.session_state.conversation_memory.save_context(
                        {"input": prompt},
                        {"output": response_content}
                    )
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_content
                    })
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.warning("Please check your API key and internet connection.")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Error: {str(e)}"
                })

# Help section at the bottom
with st.expander("💡 How to use this assistant"):
    st.markdown("""
    1. **Set your topic** in the sidebar to focus the AI's responses
    2. **Choose your learning style**:
       - **Quick Answer** - for fast, straightforward responses
       - **Deep Dive** - for comprehensive explanations with examples
       - **Multiple Viewpoints** - to understand from different perspectives
       - **Interactive Tutor** - for back-and-forth conversations
    3. **Type your question** in the chat input below
    4. **Clear conversation** when you want to start fresh
    
    **Tips:**
    - Start with Quick Answer to get familiar with a topic
    - Use Deep Dive when you need thorough understanding
    - Try Multiple Viewpoints to see different angles
    - Switch to Interactive Tutor for follow-up questions
    """)