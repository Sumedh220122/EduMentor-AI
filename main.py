import json
import pandas as pd
from langgraph.graph import StateGraph, START, END
from models import AgentState
from agents.profiler_agent import Profiler
from agents.designer import Designer
from agents.delivery_agent import DeliveryAgent

from database.lessons_collection import DatabaseConnection

class EduMentor:
    def __init__(self):
      self.profiler_agent = Profiler()
      self.designer_agent = Designer()
      self.delivery_agent = DeliveryAgent()

      self.db_connection = DatabaseConnection()

    def init_graph(self):
      """
        Initialize the graph with agents and edges
      """
      graph_builder = StateGraph(AgentState)
      graph_builder.add_node("profiler", self.profiler_agent.profile)
      graph_builder.add_node("designer", self.designer_agent.design_roadmap)
      graph_builder.add_node("delivery_agent", self.delivery_agent.deliver_resources)

      graph_builder.add_edge(START, "profiler")
      graph_builder.add_edge("profiler", "designer")
      graph_builder.add_edge("designer", "delivery_agent")
      graph_builder.add_edge("delivery_agent", END)
      # graph_builder.add_edge("designer", END)

      return graph_builder
    
    async def create_lessons(self, student_info: dict) -> pd.DataFrame:
      graph_builder = self.init_graph()
      graph = graph_builder.compile()

      output = await graph.ainvoke({"messages": [{"role" : "user", "content" : json.dumps(student_info)}]})

      from models import Roadmap
      roadmaps : list[Roadmap] = output["roadmap"].roadmaps

      data = [
          {
              "Week": roadmap.week,
              "Topic": roadmap.topic,
              "Sub-topic": roadmap.sub_topic,
              "Resources": "\n".join(roadmap.url_resources)
          }
          for roadmap in roadmaps
      ]

      df = pd.DataFrame(data)
      
      return df
    
    def get_student_lessons(self, student_name: str):
      """
      Get all lessons for a student by his name
      """
      student_lessons = self.db_connection.get_lessons(student_name)

      return student_lessons

# Comment out for testing
# if __name__ == "__main__":
#     student_info ={
#        "name": "Aarav Sharma",
#       "age": 19,
#       "what_are_your_interests": """
#           Data structures and algorithms, AI and ML.
#         """,
#       "what_you_like_to_do": """
#           I'm a curious and creative person. 
#           I love solving problems and building things.
#           I enjoy coding, reading about new technologies, and exploring different fields of knowledge.
#         """,
#       "how_good_are_you?": "I would say I'm intermediate. "
#         "I've done some personal projects and taken online courses, but I still have a lot to learn.",
#       "how_long_are_you_willing_to_commit_to_learning": "Around 6-8 hours a week consistently, more during vacations."
#     }
#     import asyncio
#     edu_mentor = EduMentor()
#     output = asyncio.run(edu_mentor.create_lessons(student_info))
#     print("Lessons created successfully.")


