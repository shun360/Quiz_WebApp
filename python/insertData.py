import os
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel
from pymongo import MongoClient
import json
from jsonschema import validate, ValidationError

def insert_quiz(quiz):
    with open('python\quiz_schema.json', encoding="utf-8") as q_json:
        json_schema = json.load(q_json)
    
    try:
        validate(quiz, json_schema)
    except ValidationError as e:
        print('エラー：', e.message)
        return False
    load_dotenv()

    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    MONGO_SERVER = os.getenv("MONGO_SERVER")
    MONGO_DB = os.getenv("MONGO_DB")

    mongo_connecter = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_SERVER}/"

    try:
        db = MongoClient(mongo_connecter)[MONGO_DB]
        db["quizList"].insert_one(quiz)
        return True
    except Exception as e:
        print('エラー：', e)
        return False

        


if __name__ == '__main__':
    testQ = {
        'Qid': 0, 
        'title':'test', 
        'questions':[{
            "no": 1,
            "text": "1 + 1 = ",
            "choices": ["1", "2", "3", "4"],
            "correctAnswer": 2,
            "explanation": ""
        }]
    }
    print(insert_quiz(testQ))