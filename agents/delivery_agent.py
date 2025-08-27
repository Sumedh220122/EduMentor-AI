from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler, CrawlResult, CacheMode, CrawlerRunConfig
from dotenv import load_dotenv
from models import AgentState, StudentRoadMaps, Roadmap, StudentLessons
from langchain_core.messages import AIMessage

from database.lessons_collection import DatabaseConnection

load_dotenv()

class DeliveryAgent:
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def extract_and_cleanup(self, page_data : str) -> str:
        """
        Extracts and cleans up content from scraped page html content.
        Args:
            page_data : str -> The HTML content of the page.
        Returns:
            str -> Cleaned text content from the page.
        """

        if page_data is None:
            return "No lessons to display here."

        soup = BeautifulSoup(page_data, 'html.parser')
        for script_or_style in soup(['script', 'style']):
            script_or_style.extract()

        cleaned_content = soup.get_text(separator = "\n")
        cleaned_content = ".".join(
            line.strip() for line in cleaned_content.splitlines() if line.strip()
        )

        return cleaned_content
    
    async def scrape_content(self, url: str):
        """
        Scrapes content from url resources provided by the designer agent using Crawl4AI
        Args:
            url: str -> The resource url which is to be scraped
        Returns:
            cleaned page content from the url
        """
        crawler_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            check_robots_txt=True,
            stream = False
        )

        async with AsyncWebCrawler() as crawler:
            result: CrawlResult = await crawler.arun(
                url = url,
                config = crawler_config
            )

        return result.cleaned_html

    async def deliver_resources(self, state: AgentState) -> dict:
        """
        Scrapes content resource urls provided as a part pf the roadmap by the Designer agent.
        Args:
            state : AgentState -> The current state of the agent containing the roadmap.
        Returns:
            dict -> Updated state with scraped content messages.
        """
        student_roadmap : StudentRoadMaps = state["roadmap"]
        roadmaps : list[Roadmap] = student_roadmap.roadmaps

        lessons = []

        topicwise_extracted_data = None

        for roadmap in roadmaps:
            url_resources = roadmap.url_resources
            sub_topic = roadmap.sub_topic
            extracted_resource_data = []
            for url in url_resources:
                print(f"Fetching content from {url}")
                
                page_data = await self.scrape_content(url)

                cleaned_content = self.extract_and_cleanup(page_data)

                extracted_resource_data.append({
                    "week" : roadmap.week,
                    "sub_topic": sub_topic,
                    "content": cleaned_content
                })
            
            topicwise_extracted_data = {
                "topic": roadmap.topic,
                "sub_topic_data": extracted_resource_data
            }

            lessons.append(topicwise_extracted_data)

            response_msg = AIMessage(content = f"{topicwise_extracted_data}")
            state["messages"] = state["messages"] + [response_msg]


        student_name = state["details"].name

        student_lessons = StudentLessons(
            name = student_name,
            lessons = lessons
        )

        self.db_connection.add_lessons(student_lessons)

        return {
            "messages": state["messages"],
        }
