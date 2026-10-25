import json
import os

from .constants import DATA_DIR


def load_metadata(filepath):
    """Прочитать схемы таблиц или вернуть пустой словарь при первом запуске."""
    try:
        with open(filepath, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """Записать схемы таблиц в JSON-файл."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_table_data(table_name):
    """Прочитать записи таблицы или вернуть пустой список, если файла нет."""
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")

    try:
        with open(filepath, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    """Создать папку данных при необходимости и сохранить записи таблицы."""
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def remove_table_data(table_name):
    """Удалить файл таблицы; у новой пустой таблицы его может ещё не быть."""
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")
    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass
