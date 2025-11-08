import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS # Used for local development to allow the GUI to connect

# --- Persistence Configuration ---
DATA_FILE = 'media_data.json'
MEDIA = {}
NEXT_ID = 1
CATEGORIES = ["Book", "Film", "Magazine"]

def load_media_data():
    """Loads media data from the JSON file."""
    global MEDIA, NEXT_ID
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                # Ensure keys are integers
                MEDIA = {int(k): v for k, v in data.get('media', {}).items()}
                NEXT_ID = data.get('next_id', 1)
        except json.JSONDecodeError:
            print(f"Error reading {DATA_FILE}. Starting with empty data.")
            MEDIA = {}
            NEXT_ID = 1
    else:
        # Initial dummy data if file does not exist
        print(f"File {DATA_FILE} not found. Creating initial dummy data.")
        MEDIA.update({
            1: {"id": 1, "name": "The Lord of the Rings", "publication_date": "1954-07-29", "author": "J.R.R. Tolkien", "category": "Book"},
            2: {"id": 2, "name": "Inception", "publication_date": "2010-07-16", "author": "Christopher Nolan", "category": "Film"},
            3: {"id": 3, "name": "National Geographic", "publication_date": "2023-10-01", "author": "Various", "category": "Magazine"}
        })
        NEXT_ID = 4
        save_media_data()

def save_media_data():
    """Saves media data to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        # Use str(k) to serialize integer keys for JSON
        serializable_media = {str(k): v for k, v in MEDIA.items()}
        json.dump({'media': serializable_media, 'next_id': NEXT_ID}, f, indent=4)

load_media_data() # Load data when the server starts

app = Flask(__name__)
CORS(app) # Enable CORS for frontend communication

# --- HTTP Endpoints ---

# 1. List of all available media items
@app.route('/media', methods=['GET'])
def list_all_media():
    return jsonify(list(MEDIA.values()))

# 2. List of all available media items that can be borrowed in a specific category.
@app.route('/media/category/<category>', methods=['GET'])
def list_media_by_category(category):
    if category not in CATEGORIES:
        return jsonify({"message": f"Category '{category}' is invalid. Must be one of: {', '.join(CATEGORIES)}"}), 400
    
    filtered_media = [item for item in MEDIA.values() if item['category'] == category]
    return jsonify(filtered_media)

# 3. Search for media items with a specific name (exact match).
@app.route('/media/search', methods=['GET'])
def search_media_by_name():
    name = request.args.get('name')
    if not name:
        return jsonify({"message": "Query parameter 'name' is required for search."}), 400
    
    # Exact match search
    found_media = [item for item in MEDIA.values() if item['name'].lower() == name.lower()]
    
    if found_media:
        return jsonify(found_media)
    else:
        return jsonify({"message": f"No media found with the exact name: '{name}'"}), 404

# 4. Display the metadata of a specific media item.
@app.route('/media/<int:media_id>', methods=['GET'])
def display_media_metadata(media_id):
    media_item = MEDIA.get(media_id)
    if media_item:
        return jsonify(media_item)
    return jsonify({"message": f"Media with ID {media_id} not found."}), 404

# 5. Create a new media item.
@app.route('/media', methods=['POST'])
def create_new_media():
    global NEXT_ID
    data = request.get_json()
    
    # Validation
    required_fields = ['name', 'publication_date', 'author', 'category']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required field(s). Required: name, publication_date, author, category"}), 400
    
    if data['category'] not in CATEGORIES:
        return jsonify({"message": f"Invalid category. Must be one of: {', '.join(CATEGORIES)}"}), 400
    
    new_media = {
        "id": NEXT_ID,
        "name": data['name'],
        "publication_date": data['publication_date'],
        "author": data['author'],
        "category": data['category']
    }
    
    MEDIA[NEXT_ID] = new_media
    NEXT_ID += 1
    save_media_data()
    
    return jsonify(new_media), 201

# 6. Delete a specific media item.
@app.route('/media/<int:media_id>', methods=['DELETE'])
def delete_specific_media(media_id):
    if media_id in MEDIA:
        del MEDIA[media_id]
        save_media_data()
        return jsonify({"message": f"Media with ID {media_id} successfully deleted."}), 200
    return jsonify({"message": f"Media with ID {media_id} not found."}), 404

if __name__ == '__main__':
    # You need to install flask and flask-cors: pip install flask flask-cors
    app.run(debug=True, port=5000)