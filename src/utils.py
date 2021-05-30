import json
def load_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data

def save_json(data, file_path):
    with open(file_path, "w") as f:
        json.dump(data, f)
    print(f"SAVE {file_path} SUCCESS")


