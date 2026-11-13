import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "data", "inventory.json")


def load_data() -> list:
    if not os.path.exists(FILE_PATH):
        return []

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        print("\nВнимание: файл данных поврежден или пуст. Загружен пустой список.")
        return []


def save_data(items: list) -> None:
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(items, file, ensure_ascii=False, indent=4)
