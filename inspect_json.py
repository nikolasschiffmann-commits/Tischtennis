import json

with open("remix.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def search(obj, path=""):
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_path = f"{path}.{key}" if path else key

            if key == "meetings":
                print("\nFOUND:")
                print(new_path)

            search(value, new_path)

    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            search(item, f"{path}[{idx}]")

search(data)
