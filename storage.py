# storage.py
# Simple JSON-backed storage for media items.

import json
import uuid
from pathlib import Path
from typing import List, Dict, Optional

DATA_FILE = Path("media_store.json")


def _ensure_file():
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")


def load_all() -> List[Dict]:
    _ensure_file()
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_all(items: List[Dict]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)


def find_by_id(item_id: str) -> Optional[Dict]:
    items = load_all()
    for it in items:
        if it.get("id") == item_id:
            return it
    return None


def find_by_name_exact(name: str) -> Optional[Dict]:
    items = load_all()
    for it in items:
        if it.get("name") == name:
            return it
    return None


def find_by_category(category: str) -> List[Dict]:
    items = load_all()
    return [it for it in items if it.get("category", "").lower() == category.lower()]


def add_media(data: Dict) -> Dict:
    items = load_all()
    new_item = {
        "id": str(uuid.uuid4()),
        "name": data["name"],
        "publication_date": data["publication_date"],
        "author": data["author"],
        "category": data["category"],
    }
    items.append(new_item)
    save_all(items)
    return new_item


def delete_media(item_id: str) -> bool:
    items = load_all()
    new_items = [it for it in items if it.get("id") != item_id]
    if len(new_items) == len(items):
        return False
    save_all(new_items)
    return True
