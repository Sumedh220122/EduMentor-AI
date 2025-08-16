import json
import httpx
import json_repair
from langchain_cohere import ChatCohere
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote
from models import AgentState, StudentDetails, StudentRoadMaps
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.messages import AIMessage
from langchain_community.tools.tavily_search import TavilySearchResults

from prompts import get_breakdown_prompt, roadmap_design_prompt

load_dotenv()

class Designer:
    def __init__(self):
        self.llm = ChatCohere()
        self.user_agent = "Puch/1.0 (Autonomous)"

    def break_user_interests(self, state: AgentState) -> None:
        """
        Break user interests into topics and sub-topics
        """
        print("Breaking down student interests into sub topics")

        student_details: StudentDetails = state["details"]
        
        template = get_breakdown_prompt()

        prompt = PromptTemplate(
            input_variables = ["student_details"],
            template = template,
        )

        chain = prompt | self.llm

        response = chain.invoke({
            "student_details": student_details.model_dump_json(),
        })

        topicwise_breakdown = json_repair.loads(response.content)

        if not isinstance(topicwise_breakdown, dict):
            raise ValueError(f"The agent response must be a dict and not {type(topicwise_breakdown)}")
        
        if not topicwise_breakdown.get("breakdown_details"):
            raise ValueError("Could not find the key breakdown_details in the agent response")
        
        for item in topicwise_breakdown.get("breakdown_details"):
            if not item.get("topic") or not item.get("sub_topics"):
                raise ValueError("Could not find topic or sub-topic details")

        response_msg = AIMessage(content = f"{json.dumps(topicwise_breakdown)}")
        state["messages"] = state["messages"] + [response_msg]

    
    def design_roadmap(self, state: AgentState) -> dict:
        """
        Craft a personalized roadmap for the given student
        """
        print("Beginning to design a personalized student roadmap")

        self.break_user_interests(state)
        topicwise_details = json.loads(state["messages"][-1].content)["breakdown_details"]
        
        topic_resources = []

        for detail in topicwise_details:
            sub_topics = detail["sub_topics"]
            subtopic_metadata = []
            for sub_topic in sub_topics:
                search_query = f"Online resources on medium.com for {sub_topic}"
                resources = self.search_web(search_query, max_results = 2)
                resource_urls = [self.decode_url(url) for url in resources]

                subtopic_metadata.append({
                    "sub_topic": sub_topic,
                    "online_resources": resource_urls
                })
                
            topic_resources.append(
                {
                    "topic" : detail["topic"],
                    "subtopic_metadata": subtopic_metadata
                }
            )

        self.create_roadmap_with_llm(topic_resources, state)

        print("Created Student roadmap: ", state["roadmap"])

        return {
            "details" : state["details"],
            "messages": state["messages"],
            "roadmap": state["roadmap"]
        }

    def create_roadmap_with_llm(self, topic_resources : list[dict], state: AgentState) -> None:
        """
        Use an llm to generate a roadmap plan for the given student.
        params:
            topic_resources: list of objects. Each object has:
                 topic: the topic of interest.
                 sub_topics: the sub topics for the given topic
                 online_resources: online resources for each sub topic as a list of urls
        """

        template = roadmap_design_prompt()

        student_details: StudentDetails = state["details"]

        parser = PydanticOutputParser(pydantic_object = StudentRoadMaps)

        prompt = PromptTemplate(
            input_variables=["student_profile", "topics_and_subtopics"],
            partial_variables={"schema": parser.get_format_instructions()},
            template=template,
        )

        chain = prompt | self.llm | parser

        response: StudentRoadMaps = chain.invoke({
            "student_profile": student_details.model_dump_json(),
            "topics_and_subtopics": "\n".join([json.dumps(resource) for resource in topic_resources]) 
        })

        response_msg = AIMessage(content = f"Constructed Roadmap: {response}")
        updated_messages = state["messages"] + [response_msg]

        state["messages"] = updated_messages

        state["roadmap"] = response

    def search_web(self, search_query : str, max_results: int) -> list[str]:
        """
        Perform a scoped DuckDuckGo search and return a list of URLs corresponding to the search query.
        """
        ddg_url = f"https://html.duckduckgo.com/html/?q={search_query.replace(' ', '+')}"
        links = []

        try:
            with httpx.Client() as client:
                resp = client.get(ddg_url, headers={"User-Agent": self.user_agent})
                if resp.status_code != 200:
                    return ["<error>Failed to perform search.</error>"]
        except httpx.RequestError as e:
            return [f"<error>{e}</error>"]

        soup = BeautifulSoup(resp.text, "html.parser")
        for a in soup.find_all("a", class_="result__a", href=True):
            href = a["href"]
            if "http" in href:
                links.append(href)
            if len(links) >= max_results:
                break
        
        print(f"Fetched resources from the web for search_query: {search_query}")

        return links or ["<error>No results found.</error>"]
    
    def decode_url(self, url: str) -> str:
        """
        Take a URL-encoded duckduckgo url and return the decoded version
        """
        # Extract uddg parameter and decode
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        real_url = unquote(params.get("uddg", [""])[0])
        return real_url