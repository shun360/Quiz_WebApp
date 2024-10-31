import os
from typing import List
from dotenv import load_dotenv
from pymongo import MongoClient
import json
from jsonschema import validate, ValidationError

def insert_quiz(path, qid = -1):
    if qid >= 0:
        one = True
        with open(r'..\json\schema\a_quiz_schema.json', encoding="utf-8") as file:
            json_schema = json.load(file)
    else:
        one = False
        with open(r'..\json\schema\quizzes_schema.json', encoding="utf-8") as file:
            json_schema = json.load(file)
    
    with open(path, encoding='utf-8') as file:
        quiz = json.load(file)
    try:
        validate(quiz, json_schema)
    except ValidationError as e:
        print('エラー/バリデート：', e.message)
        return False
    
    load_dotenv()
    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    MONGO_SERVER = os.getenv("MONGO_SERVER")
    MONGO_DB = os.getenv("MONGO_DB")
    mongo_connecter = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_SERVER}/"
    
    db = MongoClient(mongo_connecter)[MONGO_DB]
    collection = db["quizList"]
    if one:
        try:
            result = collection.update_one({"Qid": qid}, {"$push":{"questions": quiz}}, upsert=False)
            return result.modified_count > 0
        except Exception as e:
            print('エラー/作成時：', e)
            return False
    else:
        try:
            collection.insert_one(quiz)
            return True
        except Exception as e:
            print('エラー/作成時：', e)
            return False


if __name__ == '__main__':
    testQ = r"..\json\quizzes\test_quiz.json"
    is_insert_set = int(input("一問のみ追加の場合は0、クイズセットを追加したい場合は1を入力してください:"))
    if is_insert_set:
        path = input("[セット追加]追加するJSONファイルのパスを指定してください:")
        result = insert_quiz(path)
    else:
        qid = int(input("[一問追加]Qidを入力してください"))
        path = input("[一問追加]追加するJSONファイルのパスを指定してください")
        result = insert_quiz(path, qid)
    if result:
        print("追加しました")
    else:
        print("追加できませんでした")