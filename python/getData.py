import os
import uvicorn
from dotenv import load_dotenv
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可（必要に応じて制限できます）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_set_quiz(qid):
    load_dotenv()

    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    MONGO_SERVER = os.getenv("MONGO_SERVER")
    MONGO_DB = os.getenv("MONGO_DB")
    mongo_connecter = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_SERVER}/"
    try:
        db = MongoClient(mongo_connecter)[MONGO_DB]
        quiz = db['quizList'].find_one({"Qid": qid}, {'_id': 0})
        return quiz
    except Exception as e:
        print('エラー：', e)
        return None

def get_all_quiz():
    load_dotenv()

    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    MONGO_SERVER = os.getenv("MONGO_SERVER")
    MONGO_DB = os.getenv("MONGO_DB")
    mongo_connecter = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_SERVER}/"
    try:
        db = MongoClient(mongo_connecter)[MONGO_DB]
        all_quiz = list(db['quizList'].find({}, {'_id': 0}))
        return all_quiz
    except Exception as e:
        print('エラー：', e)
        return None

@app.get('/api/quizzes')
def quizzes():
    quiz_data = get_all_quiz()
    return JSONResponse(content=quiz_data)

@app.get('/api/quizzes/{qid}')
def quiz_set(qid: int):
    quiz_data = get_set_quiz(qid)
    if quiz_data is not None:
        return JSONResponse(content=quiz_data)
    raise HTTPException(status_code=404, detail="Entry not found")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)