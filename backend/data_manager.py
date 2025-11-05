import json
import os
from typing import Dict, Any

# Define the file where data will be saved
DATA_FILE = 'media_data.json'
# Define the allowed categories
CATEGORIES = ["Book", "Film", "Magazine"]

class DataManager:
    """Manages loading, saving, and CRUD operations on media data."""

    def __init__(self):
        self.media: Dict[str, Dict[str, Any]] = {}
        self.next_id = 1
        self._load_data()
        
    def _load_data(self):
        """Loads media data from the JSON file."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    # Load data. Keys (IDs) must be converted back to integers if using next_id logic.
                    data = json.load(f)
                    self.media = {k: v for k, v in data.items()}
                    
                    # Determine the next available ID
                    if self.media:
                        # Find the max ID used and set next_id one higher
                        max_id = max([int(k) for k in self.media.keys()])
                        self.next_id = max_id + 1
                    
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading data file {DATA_FILE}: {e}. Starting with empty data.")
                self.media = {}
        
    def _save_data(self):
        """Saves current media data to the JSON file."""
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.media, f, indent=4)
        except IOError as e:
            print(f"Error saving data file {DATA_FILE}: {e}")

    def create_media(self, data: Dict[str, str]) -> Dict[str, Any]:
        """Creates a new media item, assigns an ID, and saves data."""
        
        # 1. Validation (Best Practice)
        required_fields = ["Name", "Publication date", "Author", "Category"]
        if not all(field in data for field in required_fields):
            raise ValueError("Missing required field(s).")
        if data["Category"] not in CATEGORIES:
             raise ValueError(f"Invalid category. Must be one of: {', '.join(CATEGORIES)}")

        # 2. Assignment
        new_id = str(self.next_id)
        new_media = {
            "id": new_id,
            "Name": data["Name"],
            "Publication date": data["Publication date"],
            "Author": data["Author"],
            "Category": data["Category"],
        }
        
        # 3. Persistence
        self.media[new_id] = new_media
        self.next_id += 1
        self._save_data()
        
        return new_media

    def get_all_media(self) -> list:
        """Returns a list of all media items."""
        return list(self.media.values())

    def get_media_by_id(self, media_id: str) -> Dict[str, Any]:
        """Returns a single media item by its ID."""
        if media_id not in self.media:
            raise KeyError(f"Media item with ID {media_id} not found.")
        return self.media[media_id]

    def get_media_by_category(self, category: str) -> list:
        """Returns a list of media items in a specific category."""
        if category not in CATEGORIES:
            # For robustness, handle invalid categories gracefully
            return []
            
        return [item for item in self.media.values() if item["Category"] == category]

    def search_media_by_name(self, name: str) -> list:
        """Searches for media items with an exact name match."""
        return [item for item in self.media.values() if item["Name"].lower() == name.lower()]

    def delete_media(self, media_id: str) -> bool:
        """Deletes a media item by its ID."""
        if media_id not in self.media:
            raise KeyError(f"Media item with ID {media_id} not found.")
        
        del self.media[media_id]
        self._save_data()
        return True

# Initialize data manager upon module load (best practice)
data_manager = DataManager()

# Add initial data if the file was empty
if not data_manager.media:
    data_manager.create_media({"Name": "The Martian", "Publication date": "2011", "Author": "Andy Weir", "Category": "Book"})
    data_manager.create_media({"Name": "Dune", "Publication date": "2021", "Author": "Denis Villeneuve", "Category": "Film"})
    data_manager.create_media({"Name": "Time Magazine", "Publication date": "2023", "Author": "Various", "Category": "Magazine"})