## .envファイルの作成

MONGO_USER=
MONGO_PASSWORD=
MONGO_SERVER=webthequiz.34zrr.mongodb.net
MONGO_DB=quizDB

各自で.envファイルを作成し、↑をコピぺして、USERとPASSWORDを自分のものを埋める

## Python仮想環境の作成
1. VS Codeのターミナルを開いて、カレントディレクトリがプロジェクトのものであることを確認する。
2. ```python -m venv venv```
を実行
3. ```\venv\Scripts\activate```
を実行
4. 表示されているパスの頭に(venv)があることを確認する
5. ```pip install -r requirements.txt```
を実行する

## VS Code上のpythonファイルの実行方法
1. pythonフォルダに移動
```
cd python
```
2. 実行
```
python <ファイル名>
```

### Pythonファイル実行時注意事項 
・Qidに0未満を指定してはいけない
・パスは相対パス指定
