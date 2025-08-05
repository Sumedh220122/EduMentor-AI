from langchain_cohere import ChatCohere
from dotenv import load_dotenv
from models import AgentState, StudentDetails
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage

from prompts import get_data_extraction_prompt

load_dotenv()

class Profiler:
    def __init__(self):
        self.llm = ChatCohere()

    def profile(self, state: AgentState) -> dict:
        """
            Extract student details into a structured student object
        """
        print("Extracting student profile data...")
        student_data = state["messages"][-1].content

        template = get_data_extraction_prompt()

        parser = PydanticOutputParser(pydantic_object = StudentDetails)

        prompt = PromptTemplate(
            input_variables=["details"],
            partial_variables={"schema": parser.get_format_instructions()},
            template=template,
        )

        chain = prompt | self.llm | parser

        response: StudentDetails = chain.invoke({
            "details": student_data,
        })

        response_msg = AIMessage(content = f"Extracted student profile: {response}")
        updated_messages = state["messages"] + [response_msg]

        print("Successfully extracted student profile data")

        return {
            "messages" : updated_messages,
            "details": response
        }


        

        

