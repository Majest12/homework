import unittest
import requests_mock
import os
import sys
import requests # <--- ADD THIS LINE

# --- Path Fix ---
# This line adds the project root to the Python path so imports like 'from frontend.api_client import ...' work.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ----------------

from frontend.api_client import ApiClient

class TestFrontendApiClient(unittest.TestCase):
    
    def setUp(self):
        """Set up the client and mock data before each test."""
        self.client = ApiClient()
        self.base_url = 'http://127.0.0.1:5000/media'
        self.mock_media_list = [
            {"id": "1", "Name": "Moby Dick", "Category": "Book", "Author": "H. Melville", "Publication date": "1851"}
        ]
        self.mock_create_data = {
            "Name": "New Film", "Publication date": "2025", "Author": "Z", "Category": "Film"
        }
        self.mock_created_response = {
             "id": "2", "Name": "New Film", "Publication date": "2025", "Author": "Z", "Category": "Film"
        }

    # --- Test 2.1: Successful List All (Endpoint 1) ---
    def test_1_get_all_media_success(self):
        """Tests successful retrieval of all media."""
        with requests_mock.Mocker() as m:
            # Mock a successful GET request to the base URL
            m.get(self.base_url, json=self.mock_media_list, status_code=200)
            
            result = self.client.get_all_media()
            
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['Name'], "Moby Dick")

    # --- Test 2.2: Successful Creation (Endpoint 5) ---
    def test_2_create_media_success(self):
        """Tests successful creation of new media item."""
        with requests_mock.Mocker() as m:
            # Mock a successful POST request with 201 Created status
            m.post(self.base_url, json=self.mock_created_response, status_code=201)
            
            result = self.client.create_media(self.mock_create_data)
            
            self.assertEqual(result['Name'], "New Film")
            self.assertEqual(result['id'], "2")

    # --- Test 2.3: Connection Error Handling ---
    def test_3_connection_failure_handling(self):
        """Tests connection failure returns an error dictionary."""
        with requests_mock.Mocker() as m:
            # Simulate an inability to connect (Network/ConnectionError)
            m.get(self.base_url, exc=requests.exceptions.ConnectionError) 
            
            result = self.client.get_all_media()
            
            # The client is designed to return a dictionary with an 'error' key on failure
            self.assertIsInstance(result, dict)
            self.assertIn('error', result)
            self.assertIn("Connection Failed", result['error'])