import os
from dotenv import load_dotenv
from pymongo import MongoClient
import json
from jsonschema import validate, ValidationError

def update_quiz(qid, no, path):
    with open(r'..\json\schema\a_quiz_schema.json', encoding="utf-8") as q_json:
        json_schema = json.load(q_json)

    with open(path, encoding='utf-8') as file:
        quiz = json.load(file)

    try:
        validate(quiz, json_schema)
    except ValidationError as e:
        print('エラー/バリデート時:', e.message)
        return
    load_dotenv()

    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    MONGO_SERVER = os.getenv("MONGO_SERVER")
    MONGO_DB = os.getenv("MONGO_DB")

    mongo_connecter = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_SERVER}/"

    try:
        db = MongoClient(mongo_connecter)[MONGO_DB]
        collection = db['quizList']
        result = collection.update_one({"Qid": qid, "questions.no": no}, 
            {"$set": {
                "questions.$.text": quiz["text"],
                "questions.$.choices": quiz["choices"],
                "questions.$.correctAnswer": quiz["correctAnswer"],
                "questions.$.explanation": quiz["explanation"]
            }})
        return result.modified_count
    except Exception as e:
        print('エラー/更新時：', e)
        return

if __name__ == '__main__':

    qid = int(input('Qidを入力してください：'))
    no = int(input('noを入力してください：'))
    path = input("クイズ一問のファイルパスを入力してください:")
    result = update_quiz(qid, no, path)
    if result > 0:
        print("更新に成功しました")
    else:
        print("更新されませんでした")
