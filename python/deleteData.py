import os
from dotenv import load_dotenv
from pymongo import MongoClient

def delete_quizzes(qid, no = -1):
    load_dotenv()

    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    MONGO_SERVER = os.getenv("MONGO_SERVER")
    MONGO_DB = os.getenv("MONGO_DB")

    mongo_connecter = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_SERVER}/"

    try:
        db = MongoClient(mongo_connecter)[MONGO_DB]
        collection = db['quizList']
        if no < 0:
            result = collection.delete_one({"Qid": qid})
            return result.deleted_count
        else:
            result = collection.update_one({"Qid": qid}, {"$pull": {"questions": {"no": no}}})
            return result.modified_count
    except Exception as e:
        print('エラー：', e)
        return 0

if __name__ == '__main__':
    is_delete_one = int(input('一問のみ削除の場合は0、クイズセットを削除したい場合は1を入力してください：'))
    
    if is_delete_one:
        qid = int(input('[セット削除] Qidを入力してください：'))
        print(delete_quizzes(qid), '件が削除されました')
    else:
        qid = int(input('[一問削除] Qidを入力してください：'))
        no = int(input('[一問削除] noを入力してください：'))
        print(delete_quizzes(qid, no), '件が削除されました')
