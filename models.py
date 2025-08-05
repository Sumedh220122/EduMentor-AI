from pydantic import BaseModel, Field
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class StudentDetails(BaseModel):
    name: str = Field(..., description="The name of the student whose details are being recorded")
    age: str = Field(..., description="The age of the student")
    subjects_interest : list = Field(..., description="Subjects the student is interested in")
    expertise_level: str = Field(..., description="Indicates the knowledge level of the student")
    time_committment: str = Field(..., description="How much time is the student willing to dedicate for learning")
    goal: str = Field(..., description="What is the goal of the student at the end of the day?")

class Roadmap(BaseModel):
    topic: str
    roadmap: str
    url_resources : list[str]

class StudentRoadMaps(BaseModel):
    name: str
    roadmaps: list[Roadmap]

class AgentState(TypedDict):
    details : StudentDetails
    roadmap: StudentRoadMaps
    messages : Annotated[list, add_messages]