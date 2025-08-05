from dotenv import load_dotenv
import json
from langgraph.graph import StateGraph, START, END
from models import AgentState, StudentRoadMaps
from agents.profiler_agent import Profiler
from agents.designer import Designer

load_dotenv()

profiler = Profiler()
designer = Designer()

graph_builder = StateGraph(AgentState)
graph_builder.add_node("profiler", profiler.profile)
graph_builder.add_node("designer", designer.design_roadmap)

graph_builder.add_edge(START, "profiler")
graph_builder.add_edge("profiler", "designer")
graph_builder.add_edge("designer", END)

graph = graph_builder.compile()

details = {
  "name": "Aarav Sharma",
  "age": 19,
  "what_are_your_interests": "I'm fascinated by robotics, artificial intelligence, and how machines can learn. I also enjoy physics and playing the guitar.",
  "what_you_like_to_do": "I'm a curious and creative person. I love building DIY projects, reading sci-fi novels, and hiking during the weekends. I'm always looking for ways to combine tech and creativity.",
  "how_good_are_you?": "I would say I'm intermediate. I’ve done some personal projects and taken online courses, but I still have a lot to learn.",
  "how_long_are_you_willing_to_commit_to_learning": "Around 6-8 hours a week consistently, more during vacations."
}

output = graph.invoke({"messages": [{"role" : "user", "content" : json.dumps(details)}]})

with open("student_roadmap.json", "w") as f:
    roadmap : StudentRoadMaps = output["roadmap"]
    json.dump(roadmap.model_dump(), f, indent=4)
