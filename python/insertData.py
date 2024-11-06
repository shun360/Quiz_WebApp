import os
from typing import List
from dotenv import load_dotenv
from pymongo import MongoClient
import json
from jsonschema import validate, ValidationError
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

def insert_one_quiz(quiz, qid, path_opened = False):
    # MongoDBの接続情報設定
    load_dotenv()
    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    MONGO_SERVER = os.getenv("MONGO_SERVER")
    MONGO_DB = os.getenv("MONGO_DB")
    mongo_connecter = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_SERVER}/"
    db = MongoClient(mongo_connecter)[MONGO_DB]
    collection = db["quizList"]

    # スキーマの読み込み
    with open(r'..\json\schema\a_quiz_schema.json', encoding="utf-8") as file:
        json_schema = json.load(file)
    
    # JSONファイルの読み込みとバリデーション
    if not path_opened:
        with open(quiz, encoding='utf-8') as file:
            quiz = json.load(file)
    try:
        validate(quiz, json_schema)
    except ValidationError as e:
        print('エラー/バリデート：', e.message)
        return False

    try:
        # Qidに一致する質問の最大noを取得しインクリメント
        max_no = collection.aggregate([
            {"$match": {"Qid": qid}},
            {"$unwind": "$questions"},
            {"$group": {"_id": None, "max_no": {"$max": "$questions.no"}}}
        ])
        max_no = next(max_no, {"max_no": 0})["max_no"]
        quiz["no"] = max_no + 1
        print(qid)
        print(max_no)
        # Qidが一致するドキュメントのquestionsに追加
        result = collection.update_one({"Qid": qid}, {"$push":{"questions": quiz}}, upsert=False)
        return result.modified_count > 0
    except Exception as e:
        print('エラー/作成時：', e)
        return False

def insert_quiz(path):
    # MongoDBの接続情報設定
    load_dotenv()
    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    MONGO_SERVER = os.getenv("MONGO_SERVER")
    MONGO_DB = os.getenv("MONGO_DB")
    mongo_connecter = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_SERVER}/"
    
    db = MongoClient(mongo_connecter)[MONGO_DB]
    collection = db["quizList"]

    with open(r'..\json\schema\quizzes_schema.json', encoding="utf-8") as file:
        json_schema = json.load(file)
    # JSONファイルの読み込みとバリデーション
    with open(path, encoding='utf-8') as file:
        quiz = json.load(file)
    try:
        validate(quiz, json_schema)
    except ValidationError as e:
        print('エラー/バリデート：', e.message)
        return False
    
    # クイズセットの外側と内側を切り離し、外側だけ格納する。次に内側のクイズをinsert_one_quiz()に反復で受け渡す
    try:
        max_qid = collection.aggregate([
            {"$group": {"_id": None, "max_qid": {"$max": "$Qid"}}}
        ])
        max_qid = next(max_qid, {"max_qid": 0})["max_qid"]
        quiz["Qid"] = max_qid + 1

        quiz_list = [q for q in quiz["questions"]]

        quiz.update({"questions": []})
        result = []
        result.append(collection.insert_one(quiz))
        
        for q in quiz_list:
            res = insert_one_quiz(q, quiz["Qid"], path_opened = True)
            print(f"一問ずつの結果：{res}")
            result.append(res)
        return all(result)

    except Exception as e:
        print('エラー/作成時：', e)
        return False

class One_quiz(BaseModel):
    text: str
    choices: list[str]
    correctAnswer: int
    explanation: str

class Quizzes(BaseModel):
    title: str
    questions: list[One_quiz]
# @app.post("/api/")
#def create_quizzes():

if __name__ == '__main__':
    testQ = r"..\json\quizzes\test_quiz.json"
    is_insert_set = int(input("一問のみ追加の場合は0、クイズセットを追加したい場合は1を入力してください:"))
    if is_insert_set:
        path = input("[セット追加]追加するJSONファイルのパスを指定してください:")
        result = insert_quiz(path)
    else:
        qid = int(input("[一問追加]Qidを入力してください:"))
        path = input("[一問追加]追加するJSONファイルのパスを指定してください:")
        result = insert_one_quiz(path, qid)
    if result:
        print("追加しました")
    else:
        print("追加できませんでした")
