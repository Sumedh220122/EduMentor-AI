import json
from langgraph.graph import StateGraph, START, END
from models import AgentState
from agents.profiler_agent import Profiler
from agents.designer import Designer
from agents.delivery_agent import DeliveryAgent

class EduMentor:
    def __init__(self):
      self.profiler_agent = Profiler()
      self.designer_agent = Designer()
      self.delivery_agent = DeliveryAgent()

    def init_graph(self):
      graph_builder = StateGraph(AgentState)
      graph_builder.add_node("profiler", self.profiler_agent.profile)
      graph_builder.add_node("designer", self.designer_agent.design_roadmap)
      graph_builder.add_node("delivery_agent", self.delivery_agent.scrape_content)

      graph_builder.add_edge(START, "profiler")
      graph_builder.add_edge("profiler", "designer")
      graph_builder.add_edge("designer", "delivery_agent")
      graph_builder.add_edge("delivery_agent", END)

      return graph_builder
    
    def create_lessons(self, student_info: dict):
      graph_builder = self.init_graph()
      graph = graph_builder.compile()

      output = graph.invoke({"messages": [{"role" : "user", "content" : json.dumps(student_info)}]})

      for i in range(-1, -4, -1):
        print(f"Message {i}: {len(output['messages'][i].content)}")

if __name__ == "__main__":
    student_info ={
       "name": "Aarav Sharma",
      "age": 19,
      "what_are_your_interests": """
          Data structures and algorithms, AI and ML.
        """,
      "what_you_like_to_do": """
          I'm a curious and creative person. 
          I love solving problems and building things.
          I enjoy coding, reading about new technologies, and exploring different fields of knowledge.
        """,
      "how_good_are_you?": "I would say I'm intermediate. "
        "I've done some personal projects and taken online courses, but I still have a lot to learn.",
      "how_long_are_you_willing_to_commit_to_learning": "Around 6-8 hours a week consistently, more during vacations."
    }

    edu_mentor = EduMentor()
    edu_mentor.create_lessons(student_info)
    print("Lessons created successfully.")


