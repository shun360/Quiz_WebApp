path = input("パス：")
with open(path, encoding="utf-8") as file:
    print(file.read())