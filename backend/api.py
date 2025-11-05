from flask import Flask, jsonify, request
# Import the data manager instance
from .data_manager import data_manager, CATEGORIES

# Initialize the Flask application
app = Flask(__name__)

# --- HTTP Endpoints (API Routes) ---

# 1. List of all available media items (GET /media)
@app.route('/media', methods=['GET'])
def list_all_media():
    """Returns a list of all media items."""
    try:
        media_list = data_manager.get_all_media()
        # Return HTTP 200 OK with the list of media
        return jsonify(media_list), 200
    except Exception as e:
        # Catch unexpected errors during retrieval
        return jsonify({"error": "An internal server error occurred.", "details": str(e)}), 500

# 2. List of all available media items in a specific category (GET /media/category/<category_name>)
@app.route('/media/category/<string:category_name>', methods=['GET'])
def list_media_by_category(category_name):
    """Returns a list of media items filtered by category."""
    # Ensure the category is valid (case-insensitive check for robustness)
    if category_name.capitalize() not in CATEGORIES:
        return jsonify({"error": "Invalid category provided."}), 400
    
    media_list = data_manager.get_media_by_category(category_name.capitalize())
    return jsonify(media_list), 200

# 3. Search for media items with a specific name (GET /media/search?name=...)
@app.route('/media/search', methods=['GET'])
def search_media_by_name():
    """Searches for media items with an exact name match (case-insensitive)."""
    # Get the 'name' query parameter from the URL
    name = request.args.get('name')
    
    if not name:
        return jsonify({"error": "Missing 'name' query parameter."}), 400
        
    results = data_manager.search_media_by_name(name)
    # Return 200 OK even if the list is empty
    return jsonify(results), 200

# 4. Display the metadata of a specific media item (GET /media/<id>)
@app.route('/media/<string:media_id>', methods=['GET'])
def get_media_details(media_id):
    """Returns the metadata for a single media item by ID."""
    try:
        media_item = data_manager.get_media_by_id(media_id)
        return jsonify(media_item), 200
    except KeyError:
        # Handle the specific exception when the ID is not found (KeyError from DataManager)
        return jsonify({"error": f"Media item with ID {media_id} not found."}), 404
    except Exception as e:
        return jsonify({"error": "An internal server error occurred.", "details": str(e)}), 500

# 5. Create a new media item (POST /media)
@app.route('/media', methods=['POST'])
def create_new_media():
    """Creates a new media item using data from the JSON request body."""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Request body must contain JSON data."}), 400
        
    try:
        # The DataManager handles validation and ID assignment
        new_media = data_manager.create_media(data)
        # Return 201 Created status
        return jsonify(new_media), 201
    except ValueError as e:
        # Handle validation errors (missing fields, invalid category)
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to create media item.", "details": str(e)}), 500

# 6. Delete a specific media item (DELETE /media/<id>)
@app.route('/media/<string:media_id>', methods=['DELETE'])
def delete_media_item(media_id):
    """Deletes a media item by its ID."""
    try:
        data_manager.delete_media(media_id)
        # Return 204 No Content status for successful deletion
        return '', 204 
    except KeyError:
        # Handle the specific exception when the ID is not found
        return jsonify({"error": f"Media item with ID {media_id} not found."}), 404
    except Exception as e:
        return jsonify({"error": "Failed to delete media item.", "details": str(e)}), 500

# --- Running the Server ---
if __name__ == '__main__':
    # Ensure the Flask app runs on a defined host/port (e.g., 5000)
    # In a real-world scenario, you might run this with 'flask run' or gunicorn/waitress
    # We use debug=True for development convenience
    app.run(debug=True)