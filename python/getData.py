import os
from dotenv import load_dotenv
from pymongo import MongoClient
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

def get_all_quiz():
    load_dotenv()

    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    MONGO_SERVER = os.getenv("MONGO_SERVER")
    MONGO_DB = os.getenv("MONGO_DB")
    mongo_connecter = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_SERVER}/"
    try:
        db = MongoClient(mongo_connecter)[MONGO_DB]
        all_quiz = list(db['quizList'].find({}, {'_id: 0'}))
        return all_quiz
    except Exception as e:
        print('エラー：', e)
        return []

@app.get('/api/quizzes')
def quizzes():
    quiz_data = get_all_quiz()
    return JSONResponse(content=quiz_data)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)