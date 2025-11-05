import requests
from typing import List, Dict, Any, Optional

# The base URL where your Flask backend is running
BASE_URL = 'http://127.0.0.1:5000/media'

class ApiClient:
    """Client to communicate with the Flask Media API."""

    def _request(self, method: str, url: str, json_data: Optional[Dict] = None, params: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """Generic request handler with basic error checking."""
        try:
            # Send the request
            response = requests.request(method, url, json=json_data, params=params, timeout=5)
            
            # Check for success status codes (2xx)
            if 200 <= response.status_code < 300:
                # 204 No Content (for DELETE) returns no JSON
                if response.status_code == 204:
                    return {"success": True, "message": "Operation successful"}
                
                # Return JSON data for other successful codes (200, 201)
                return response.json()
            
            # Handle client/server errors
            # Attempt to get error message from JSON body
            try:
                error_message = response.json().get("error", f"Unknown API Error (Status: {response.status_code})")
            except requests.JSONDecodeError:
                error_message = f"API Error (Status: {response.status_code}). Response was not JSON."
                
            return {"error": error_message}

        except requests.exceptions.ConnectionError:
            return {"error": "Connection Failed. Ensure the Flask backend is running on 127.0.0.1:5000."}
        except requests.exceptions.Timeout:
            return {"error": "Request timed out."}
        except Exception as e:
            return {"error": f"An unexpected network error occurred: {e}"}

    def get_all_media(self) -> List[Dict[str, Any]]:
        """Endpoint 1: List all available media."""
        result = self._request('GET', BASE_URL)
        return result if isinstance(result, list) else result

    def get_media_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Endpoint 2: List media by category."""
        url = f"{BASE_URL}/category/{category}"
        result = self._request('GET', url)
        return result if isinstance(result, list) else result

    def search_media_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Endpoint 3: Search for media items by exact name."""
        url = f"{BASE_URL}/search"
        params = {'name': name}
        result = self._request('GET', url, params=params)
        return result if isinstance(result, list) else result

    def get_media_details(self, media_id: str) -> Optional[Dict[str, Any]]:
        """Endpoint 4: Display the metadata of a specific media item."""
        url = f"{BASE_URL}/{media_id}"
        return self._request('GET', url)

    def create_media(self, data: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """Endpoint 5: Create a new media item."""
        return self._request('POST', BASE_URL, json_data=data)

    def delete_media(self, media_id: str) -> Optional[Dict[str, Any]]:
        """Endpoint 6: Delete a specific media item."""
        url = f"{BASE_URL}/{media_id}"
        return self._request('DELETE', url)