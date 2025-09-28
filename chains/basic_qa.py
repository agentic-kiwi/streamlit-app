from config.gemini_setup import get_gemini_model, get_topic
from langchain_core.prompts import ChatPromptTemplate 


template = ChatPromptTemplate.from_messages([
    ("system", " You are a helpful and fun tutor who understand the {topic} well. You will always respond in simple terms and explain the foundations of the {topic} clearly"),
    ("human" , "{question}")
])

chain = template | get_gemini_model()

def ask_question(question: str) -> str:
    """Ask a question about the current learning topic."""
    topic = get_topic()
    response = chain.invoke({"question": question, "topic": topic})
    return response.content

