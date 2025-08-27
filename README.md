# EduMentor-AI
**Edumentor** is a Multi-Agentic system that can generate personalized roadmaps, lesson plans and learning resources for students based on their interests and capabilities.

**What is the utlity of EduMentor?**
1. Simplifies searching for study resources: You can choose a maximum of 3 topics of your choice to study and just sit back. 
   Edumentor does the job for you, from fetching these resources to displaying them in a convenient manner.
2. Creating personalized roadmaps based on individual learning pace and capabilities

**Tech Stack Used**
:This is a python project. EduMentor is a *Multi-Agentic* assistant that has been built with the help of Langgraph and Langchain
frameworks in python. *Cohere* is used as the llm across all agents. *DuckDuckGo* is used for searching resources on web and *Crawl4AI* is used for scraping resources fetched from the web.

**Steps to run this file**

1. Clone the repository
   ```
   git clone https://github.com/Sumedh220122/EduMentor-AI.git
   cd EduMentor-AI
   ```
2. Create a virtual environment<br>
   ```
   python -m venv .venv
   ```
3. Install requirements</br>
    ```
    pip install -r requirements.txt
    ```
4. Setup MongoDB
      - create a database on MongoDB
      - create a new database
      - copy the name of the created database and connection string

4. Create a .env file in the root and set up the following env variables</br>
   ```
   COHERE_API_KEY=YOUR_COHERE_API_KEY
   MONGO_URI=YOUR_MONGO_URI (copied connection string)
   DB_NAME=YOUR_DB_NAME (copied db name)
   ```
5. Run the main file:</br>
   ```
   python main.py
   ```

You can get your Cohere API key for free at: https://cohere.com/<br>

**Future Enhancements(In progress)**
1. Make use of text summarizers to summarize and shorten learning material
2. Incorporate more agents into the workflow for user feedback.

