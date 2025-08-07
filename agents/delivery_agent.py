import os
import json
from bs4 import BeautifulSoup
import http.client
from dotenv import load_dotenv
from models import AgentState,StudentRoadMaps, Roadmap
from langchain_core.messages import AIMessage

load_dotenv()

class DeliveryAgent:
    def __init__(self):
        self.conn = http.client.HTTPSConnection("the-web-scraping-api.p.rapidapi.com")

        self.api_key = os.getenv("RAPIDAPI_KEY")

    def extract_and_cleanup(self, page_data : str) -> str:
        """Extracts and cleans up content from scraped page html content.
        Args:
            page_data : str -> The HTML content of the page.
        Returns:
            str -> Cleaned text content from the page.
        """
        soup = BeautifulSoup(page_data, 'html.parser')
        for script_or_style in soup(['script', 'style']):
            script_or_style.extract()

        cleaned_content = soup.get_text(separator = "\n")
        cleaned_content = "\n".join(
            line.strip() for line in cleaned_content.splitlines() if line.strip()
        )

        return cleaned_content

    def scrape_content(self, state: AgentState) -> dict:
        """
        Scrapes content resource urls provided as a part pf the roadmap by the Designer agent.
        Args:
            state : AgentState -> The current state of the agent containing the roadmap.
        Returns:
            dict -> Updated state with scraped content messages.
        """
        headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': "the-web-scraping-api.p.rapidapi.com"
        }
        
        conn_string = "/browser?headers=%7B%7D&method=GET&payload=%7B%7D&screenshot=false&fullScreenshot=false&url={url}"

        student_roadmap : StudentRoadMaps = state["roadmap"]
        roadmaps : list[Roadmap] = student_roadmap.roadmaps

        topicwise_extracted_data = None

        for roadmap in roadmaps:
            url_resources = roadmap.url_resources
            sub_topic = roadmap.sub_topic
            extracted_resource_data = []
            for url in url_resources:
                print(f"Fetching content from {url}")
                conn_string_with_url = conn_string.format(url=url)
                self.conn.request("GET", conn_string_with_url, headers = headers)
                
                res = self.conn.getresponse()
                data = res.read()
                decoded_data = data.decode("utf-8")

                data_obj = json.loads(decoded_data)
                page_data = data_obj["data"] if hasattr(data_obj, "data") else ""

                cleaned_content = self.extract_and_cleanup(page_data)

                extracted_resource_data.append({
                    "sub_topic": sub_topic,
                    "content": cleaned_content
                })
            
            topicwise_extracted_data = {
                "topic": roadmap.topic,
                "sub_topic_data": extracted_resource_data
            }

            response_msg = AIMessage(content = f"{topicwise_extracted_data}")
            state["messages"] = state["messages"] + [response_msg]

        return {
            "messages": state["messages"],
        }
