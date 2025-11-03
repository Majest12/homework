# app.py
from flask import Flask, jsonify, request, abort
from storage import (
    load_all,
    find_by_category,
    find_by_name_exact,
    find_by_id,
    add_media,
    delete_media,
)

app = Flask(__name__)

VALID_CATEGORIES = {"Book", "Film", "Magazine"}


@app.route("/media", methods=["GET"])
def list_media():
    """1. List all available media items."""
    return jsonify(load_all()), 200


@app.route("/media/category/<category>", methods=["GET"])
def list_by_category(category):
    """2. List media in a specific category."""
    if category.capitalize() not in VALID_CATEGORIES:
        return jsonify({"error": "Invalid category"}), 400
    return jsonify(find_by_category(category)), 200


@app.route("/media/search", methods=["GET"])
def search_by_name():
    """3. Search for media by exact name (query param ?name=...)."""
    name = request.args.get("name", "")
    if not name:
        return jsonify({"error": "Please provide name query parameter"}), 400
    found = find_by_name_exact(name)
    if not found:
        return jsonify({}), 404
    return jsonify(found), 200


@app.route("/media/<item_id>", methods=["GET"])
def get_metadata(item_id):
    """4. Display metadata of a specific media item by id."""
    found = find_by_id(item_id)
    if not found:
        return jsonify({"error": "Not found"}), 404
    return jsonify(found), 200


@app.route("/media", methods=["POST"])
def create_media():
    """5. Create a new media item."""
    data = request.get_json() or {}
    required = {"name", "publication_date", "author", "category"}
    if not required.issubset(data.keys()):
        return jsonify({"error": "Missing fields, required: name, publication_date, author, category"}), 400
    if data["category"].capitalize() not in VALID_CATEGORIES:
        return jsonify({"error": f"Category must be one of {list(VALID_CATEGORIES)}"}), 400
    created = add_media(data)
    return jsonify(created), 201


@app.route("/media/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    """6. Delete a specific media item."""
    ok = delete_media(item_id)
    if not ok:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"deleted": item_id}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
