
def get_data_extraction_prompt() -> str:
    """
    prompt template for student data extraction
    """
    template = (
        """
        You are an intelligent assistant helping to build a personalized learning profile for a student based on their answers to onboarding questions. 

        As an input, you will be given details that contain student details like name, age, personal preferences etc.
        Your task is to carefully analyze these details and extract student details in accordance with the foll schema:
        {schema}

        Return only the extracted details and no additional text.

        Student Details:
        {details}            
        """
    )
    return template

def get_breakdown_prompt() -> str:
    """
    prompt template for breaking down student interests into topics and sub-topics
    """
    template = (
        """
        You are an intelligent assistant who can analyze a given set of user preferences and break them down into concrete topics
        and sub topics. You do this activity with an aim of breaking down complex tasks into simpler ones with great attention to detail.

        You are given a set of details for a given student who is aiming to find a good learning plan for himself to study
        about his topics of interest, according to his own learning pace and grasping abilities.

        Your task is to analyze these details and construct an object that consists of a set of high level topics and their sub-topics.
        
        Each object shall have the following schema:
            {{ 
                topic: str
                sub_topics: list[str]
            }}

        You must return a JSON Object with key "breakdown_details" and value equal to a list of objects with the above schema.

        Return only the json object and no other extra text along with it.

        Student Details: {student_details}
        """
    )

    return template

def roadmap_design_prompt():
    """
    Prompt for designing a study roadmap based on student topic of interests, available resources and other metadata.
    """
    template = (
        """
        You are an expert education planner and learning path designer.

        You will be given the following information about a student:
        - A list of **topics the student is interested in**
        - A breakdown of **sub-topics** within each topic
        - Details about the student, such as:
            - Their **preferred learning pace**
            - **Time commitment** per day/week
            - Their **current knowledge level**
            - Their **learning goals**

        Your task is to:
        1. Analyze the student’s background and preferences
        2. Break down the topics and sub-topics into a structured learning plan
        3. Distribute the topics into weekly (or daily) goals based on the student's learning pace and time availability
        4. Recommend the best **sequence** of learning (from foundational to advanced)
        5. Optionally include suggested **learning resources** (videos, articles, books) or types of activities (practice, quizzes, projects)

        The final output should be:
        - Structured into weeks or phases
        - Balanced based on time and difficulty
        - Motivating and tailored to the student's goals

        STUDENT PROFILE:
        {student_profile}

        TOPICS AND SUB-TOPICS:
        {topics_and_subtopics}

        Now, generate a complete, personalized learning roadmap.

        You must generate an output object according to the following schema:

        {schema}

        Return only the output object and no other extra text along with it. 
        """
    )

    return template
