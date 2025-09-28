from config.gemini_setup import get_gemini_model, get_topic
from models.topic_analysis import TopicExplanation
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

def analyze_topic(question: str, api_key: str) -> TopicExplanation:
    """Analyze a question about the current learning topic."""
    parser = PydanticOutputParser(pydantic_object=TopicExplanation)
    format_instructions = parser.get_format_instructions()
    
    template = ChatPromptTemplate.from_messages([
        ("system", " You are a helpful and fun tutor who understands the {topic} well. You will always respond in simple terms and explain the foundations of the {topic} clearly. "
        "When you answer, make sure to follow the format instructions: {format_instructions}"),
        ("human" , "{question}")
    ])
    chain = template | get_gemini_model(api_key=api_key) | parser
    
    topic = get_topic()
    response = chain.invoke({"question": question, "topic": topic, "format_instructions": format_instructions})
    return response

