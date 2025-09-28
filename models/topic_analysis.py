from pydantic import BaseModel, Field
from typing import List

class TopicExplanation(BaseModel):
    main_topic: str = Field(description="What is the main topic?")
    sub_topics: List[str] = Field(description="List all of the subtopics, with a very brief description of each subtopic")
    real_world_examples: List[str] = Field(description="Provide real world examples for the sub_topics")
    connection_to_main_topic: str = Field(description="How does each subtopic connect to the main topic?")
    future_learning_resources: List[str] = Field(description="Provide links to future learning resources for each subtopic")
    quizz_me_on_it: List[str] = Field(description="Create a short quiz with answers to test my understanding of the main topic and subtopics")

    