import os
from models import StudentLessons
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:

    def __init__(self):
        self.db_name = os.getenv("DB_NAME")
        self.mongo_uri = os.getenv("MONGO_URI")

    def add_lessons(self, student_lessons: StudentLessons):
        try:
            client = MongoClient(self.mongo_uri)
            db = client[self.db_name]
            collection = db["lessons"]
            collection.insert_one(student_lessons.model_dump())
        except Exception as e:
            print(f"Error inserting token holders: {e}")
            return False
        return True