import os
import uvicorn
from dotenv import load_dotenv
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# FastAPIのインスタンスを作成
app = FastAPI()

# CORS設定：クライアントとサーバー間でクロスオリジンリクエストを許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可（必要に応じて制限できます）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDBから指定したクイズIDに基づいてクイズデータを取得する関数
def get_set_quiz(qid):
    load_dotenv()  # 環境変数をロード
    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    MONGO_SERVER = os.getenv("MONGO_SERVER")
    MONGO_DB = os.getenv("MONGO_DB")
    
    # MongoDB接続URLを作成
    mongo_connecter = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_SERVER}/"
    
    try:
        # MongoDBに接続し、データベースとコレクションを指定
        db = MongoClient(mongo_connecter)[MONGO_DB]
        quiz = db['quizList'].find_one({"Qid": qid}, {'_id': 0})  # 指定したQidに基づいてクイズを取得
        return quiz
    except Exception as e:
        print('エラー：', e)
        return None

# 全てのクイズデータを取得する関数
def get_all_quiz():
    load_dotenv()  # 環境変数をロード
    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    MONGO_SERVER = os.getenv("MONGO_SERVER")
    MONGO_DB = os.getenv("MONGO_DB")
    
    mongo_connecter = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_SERVER}/"
    
    try:
        db = MongoClient(mongo_connecter)[MONGO_DB]
        # クイズデータ全体を取得（'quizList'コレクションから全てのデータを取得）
        all_quiz = list(db['quizList'].find({}, {'_id': 0}))
        return all_quiz
    except Exception as e:
        print('エラー：', e)
        return None

# クイズデータを全て取得するAPIエンドポイント
@app.get('/api/quizzes')
def quizzes():
    quiz_data = get_all_quiz()
    if quiz_data:
        # クイズデータが存在すればJSON形式で返す
        return JSONResponse(content=quiz_data)
    raise HTTPException(status_code=404, detail="クイズデータが見つかりません")

# 特定のクイズデータを取得するAPIエンドポイント
@app.get('/api/quizzes/{qid}')
def quiz_set(qid: int):
    quiz_data = get_set_quiz(qid)
    if quiz_data is not None:
        # 特定のIDに基づくクイズデータが見つかれば返す
        return JSONResponse(content=quiz_data)
    raise HTTPException(status_code=404, detail="指定されたクイズデータが見つかりません")

# アプリケーションを起動
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
