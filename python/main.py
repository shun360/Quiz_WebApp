import os
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient

load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_SERVER = os.getenv("MONGO_SERVER")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB = os.getenv("MONGO_DB")


mongo_connecter = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_SERVER}:{MONGO_PORT}/"

# クイズ一問のクラス
class Quiz(BaseModel):
    no: int
    text: str
    choices: List[str]
    correctAnswer: int
    explanation: str

# クイズエントリーのモデル
class QuizEntry(BaseModel):
    Qid: int
    title: str
    questions: List[Quiz]

@asynccontextmanager
async def lifespan(app: FastAPI):
    with MongoClient(mongo_connecter) as client:
        app.db = client[MONGO_DB]
        yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Read クイズすべて読み込み
@app.get("/quizList/", response_model=List[QuizEntry])
def get_quizlist():
    quiz_all = list(app.db["quizList"].find())
    return quiz_all

