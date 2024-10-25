import os
from dotenv import load_dotenv
from pymongo import MongoClient

def get_all_quiz():
    load_dotenv()

    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    MONGO_SERVER = os.getenv("MONGO_SERVER")
    MONGO_DB = os.getenv("MONGO_DB")
    mongo_connecter = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_SERVER}/"
    try:
        db = MongoClient(mongo_connecter)[MONGO_DB]
        all_quiz = list(db['quizList'].find())
        return all_quiz
    except Exception as e:
        print('エラー：', e)


if __name__ == '__main__':
    print(get_all_quiz())