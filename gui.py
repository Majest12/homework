import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests
import json

# --- Configuration ---
API_BASE_URL = "http://127.0.0.1:5000"
CATEGORIES = ["All", "Book", "Film", "Magazine"] # "All" is for the initial list

class LibraryGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Online Library GUI")
        self.geometry("800x600")

        # Configure requests (requires: pip install requests)
        try:
            requests.get(f"{API_BASE_URL}/media") # Test connection
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Connection Error", 
                                 f"Could not connect to the backend at {API_BASE_URL}.\n"
                                 "Please ensure 'backend.py' is running.")
            self.destroy()
            return
        
        self.create_widgets()
        self.load_media("All")

    def create_widgets(self):
        # --- Controls Frame (Top) ---
        controls_frame = ttk.Frame(self, padding="10")
        controls_frame.pack(fill='x')

        # 1. Category Dropdown
        ttk.Label(controls_frame, text="Filter by Category:").pack(side='left', padx=(0, 5))
        self.category_var = tk.StringVar(self)
        self.category_var.set(CATEGORIES[0])
        category_menu = ttk.OptionMenu(controls_frame, self.category_var, CATEGORIES[0], *CATEGORIES, command=self.on_category_select)
        category_menu.pack(side='left', padx=(0, 20))
        
        # 3. Name Search Field
        ttk.Label(controls_frame, text="Search Name (Exact):").pack(side='left', padx=(0, 5))
        self.search_entry = ttk.Entry(controls_frame, width=20)
        self.search_entry.pack(side='left', padx=(0, 5))
        ttk.Button(controls_frame, text="Search", command=self.search_media).pack(side='left', padx=(0, 20))

        # 5. Create New Button
        ttk.Button(controls_frame, text="➕ Create New Media", command=self.create_media).pack(side='right')

        # --- List Frame (Middle) ---
        list_frame = ttk.Frame(self, padding="10")
        list_frame.pack(fill='both', expand=True)

        self.media_listbox = tk.Listbox(list_frame, height=20, font=('TkDefaultFont', 10))
        self.media_listbox.pack(side='left', fill='both', expand=True)
        self.media_listbox.bind('<<ListboxSelect>>', self.on_media_select) # 4. Display metadata on click

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.media_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.media_listbox.config(yscrollcommand=scrollbar.set)

        # --- Details Frame (Bottom) ---
        details_frame = ttk.Frame(self, padding="10")
        details_frame.pack(fill='x')
        self.details_label = ttk.Label(details_frame, text="Select an item to view details.", justify='left', wraplength=780)
        self.details_label.pack(fill='x')

        # 6. Delete Button (Placed next to details for easy access after selection)
        ttk.Button(details_frame, text="🗑️ Delete Selected Media", command=self.delete_media).pack(pady=5)
        
        self.current_media_data = []

    # --- API Communication & Frontend Logic ---

    def load_media(self, category):
        """1 & 2. Loads and displays media from the backend."""
        self.media_listbox.delete(0, tk.END)
        self.details_label.config(text="Select an item to view details.")
        self.current_media_data = []

        try:
            if category == "All":
                response = requests.get(f"{API_BASE_URL}/media")
            else:
                response = requests.get(f"{API_BASE_URL}/media/category/{category}")

            response.raise_for_status() # Raise exception for bad status codes
            
            self.current_media_data = response.json()
            if not self.current_media_data:
                self.media_listbox.insert(tk.END, f"--- No media found in category: {category} ---")
                return

            for item in self.current_media_data:
                display_text = f"[{item['category']}] ID: {item['id']} | Name: {item['name']} | Author: {item['author']}"
                self.media_listbox.insert(tk.END, display_text)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("API Error", f"Could not load media: {e}")

    def on_category_select(self, category):
        """2. Event handler for category selection."""
        if category:
            self.load_media(category)

    def search_media(self):
        """3. Searches for media by name (exact match)."""
        name = self.search_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Required", "Please enter a name to search.")
            return

        self.media_listbox.delete(0, tk.END)
        self.details_label.config(text="Select an item to view details.")
        self.current_media_data = []
        self.category_var.set("Search Results") # Change dropdown to reflect search
        
        try:
            response = requests.get(f"{API_BASE_URL}/media/search?name={name}")
            
            if response.status_code == 404:
                self.media_listbox.insert(tk.END, f"--- No exact match found for '{name}' ---")
                return
            
            response.raise_for_status()
            
            self.current_media_data = response.json()
            for item in self.current_media_data:
                display_text = f"[{item['category']}] ID: {item['id']} | Name: {item['name']} | Author: {item['author']}"
                self.media_listbox.insert(tk.END, display_text)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("API Error", f"Could not search media: {e}")

    def on_media_select(self, event):
        """4. Displays the full metadata of the selected item."""
        try:
            selection = self.media_listbox.curselection()
            if not selection:
                return

            # Get the selected media item's data from the list we loaded
            selected_item_data = self.current_media_data[selection[0]]
            
            # Fetch full metadata from the API (Endpoint 4)
            response = requests.get(f"{API_BASE_URL}/media/{selected_item_data['id']}")
            response.raise_for_status()
            metadata = response.json()
            
            details_text = (
                f"ID: {metadata['id']}\n"
                f"Name: {metadata['name']}\n"
                f"Category: {metadata['category']}\n"
                f"Author: {metadata['author']}\n"
                f"Publication Date: {metadata['publication_date']}"
            )
            self.details_label.config(text=details_text)

        except (IndexError, requests.exceptions.RequestException) as e:
            self.details_label.config(text=f"Error displaying details: {e}")

    def create_media(self):
        """5. Opens a dialog to create a new media item."""
        new_media_data = CreateMediaDialog(self).result
        if new_media_data:
            try:
                # API Endpoint 5 (POST)
                response = requests.post(f"{API_BASE_URL}/media", json=new_media_data)
                response.raise_for_status()
                messagebox.showinfo("Success", f"Media '{new_media_data['name']}' created successfully!")
                self.load_media(self.category_var.get()) # Reload the current view

            except requests.exceptions.RequestException as e:
                error_message = f"Failed to create media. {e}"
                try:
                    error_data = response.json()
                    error_message = error_data.get('message', error_message)
                except:
                    pass
                messagebox.showerror("Creation Error", error_message)

    def delete_media(self):
        """6. Deletes the currently selected media item."""
        try:
            selection = self.media_listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a media item to delete.")
                return

            selected_item_data = self.current_media_data[selection[0]]
            media_id = selected_item_data['id']
            media_name = selected_item_data['name']

            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{media_name}' (ID: {media_id})?"):
                # API Endpoint 6 (DELETE)
                response = requests.delete(f"{API_BASE_URL}/media/{media_id}")
                response.raise_for_status()
                
                messagebox.showinfo("Success", f"Media '{media_name}' deleted.")
                self.load_media(self.category_var.get()) # Reload the current view
                
        except (IndexError, requests.exceptions.RequestException) as e:
            messagebox.showerror("Deletion Error", f"Failed to delete media: {e}")


class CreateMediaDialog(simpledialog.Dialog):
    """Custom dialog for creating a new media item."""
    def __init__(self, parent):
        self.result = None
        super().__init__(parent, title="Create New Media")

    def body(self, master):
        self.entries = {}
        fields = ['Name', 'Publication Date (YYYY-MM-DD)', 'Author']
        
        for i, field in enumerate(fields):
            ttk.Label(master, text=f"{field}:").grid(row=i, column=0, sticky='w')
            entry = ttk.Entry(master, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[field.split(' ')[0].lower()] = entry
        
        # Category Dropdown
        ttk.Label(master, text="Category:").grid(row=len(fields), column=0, sticky='w')
        self.category_var = tk.StringVar(master)
        self.category_var.set(CATEGORIES[1]) # Default to Book
        category_menu = ttk.OptionMenu(master, self.category_var, CATEGORIES[1], *CATEGORIES[1:])
        category_menu.grid(row=len(fields), column=1, padx=5, pady=5, sticky='ew')

        return self.entries['name'] # initial focus

    def apply(self):
        # Gather data from fields
        data = {
            'name': self.entries['name'].get().strip(),
            'publication_date': self.entries['publication'].get().strip(),
            'author': self.entries['author'].get().strip(),
            'category': self.category_var.get()
        }
        
        # Basic validation
        if not all(data.values()):
            messagebox.showerror("Input Error", "All fields are required.")
            self.initial_focus = self.entries['name']
            return

        self.result = data


if __name__ == "__main__":
    # Ensure you have the 'requests' library installed: pip install requests
    app = LibraryGUI()
    app.mainloop()