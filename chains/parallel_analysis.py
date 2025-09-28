from config.gemini_setup import get_gemini_model, get_topic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from models.topic_analysis import TopicExplanation
from langchain_core.runnables import RunnableParallel

simple_template = ChatPromptTemplate.from_messages([
    ("system", "You are a simple explainer who breaks down {topic} concepts into easy-to-understand parts for beginners. Use analogies and simple language."),
    ("human", "{question}")
])

technical_template = ChatPromptTemplate.from_messages([
    ("system", "You are a technical expert in {topic} who provides detailed and in-depth explanations with precise terminology. Use technical terms and provide comprehensive insights."),
    ("human", "{question}")
])
code_template = ChatPromptTemplate.from_messages([
    ("system", "You are a coding assistant who provides code examples and explanations related to {topic}. Focus on practical coding aspects and best practices."),
    ("human", "{question}")
])

history_template = ChatPromptTemplate.from_messages([
    ("system", "You are a historical analyst who explains the historical context and evolution of {topic}. Provide timelines and significant milestones."),
    ("human", "{question}")
])

simple_chain = simple_template | get_gemini_model()
technical_chain = technical_template | get_gemini_model()
code_chain = code_template | get_gemini_model()
history_chain = history_template | get_gemini_model()

parallel_analysis = RunnableParallel(
    simple = simple_chain,
    technical = technical_chain,
    code = code_chain,
    history = history_chain
)

def analyze_from_multiple_perspectives(question: str) -> dict:
    """Analyze a question about the current learning topic from multiple expert perspectives simultaneously."""
    
    topic = get_topic()
    responses = parallel_analysis.invoke({
        "question": question,
        "topic": topic
    })
    return responses