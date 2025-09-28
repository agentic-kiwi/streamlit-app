from config.gemini_setup import get_gemini_model, get_topic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from models.topic_analysis import TopicExplanation
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(return_messages=True)

def chat_with_memory(question: str, api_key: str) -> str:
    """Chat with memory about the current learning topic."""
    template = ChatPromptTemplate.from_messages([
        ("system", " You are a helpful and fun tutor who understands the {topic} well. You will always respond in simple terms and explain the foundations of the {topic} clearly. "),
        ("placeholder","{chat_history}"),
        ("human", "{question}")
    ])
    chain = template | get_gemini_model(api_key=api_key) 
    
    topic = get_topic()
    chat_history = memory.chat_memory.messages
    response = chain.invoke({"question": question, "topic": topic, "chat_history": chat_history})
    memory.save_context({"input": question}, {"output": response.content})
    
    return response.content