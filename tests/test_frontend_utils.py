# tests/test_frontend_utils.py
# small test for a simple formatting helper (keeps GUI testable)
def format_meta_for_display(item: dict) -> str:
    return f"{item['name']} - {item['category']} by {item['author']}"

def test_format_meta_for_display():
    obj = {"name": "A", "category": "Book", "author": "B"}
    assert format_meta_for_display(obj) == "A - Book by B"
