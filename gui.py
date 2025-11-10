# gui.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests

BACKEND_URL = "http://127.0.0.1:5000"


class LibraryGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Online Library (Client)")
        self.geometry("700x420")
        self.create_widgets()
        self.refresh_all()

    def create_widgets(self):
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=8, pady=6)

        ttk.Label(top_frame, text="Category:").pack(side=tk.LEFT)
        self.category_var = tk.StringVar(value="All")
        categories = ["All", "Book", "Film", "Magazine"]
        self.category_menu = ttk.OptionMenu(top_frame, self.category_var, "All", *categories, command=self.on_category_change)
        self.category_menu.pack(side=tk.LEFT, padx=6)

        ttk.Label(top_frame, text="Search (exact name):").pack(side=tk.LEFT, padx=(12, 4))
        self.search_entry = ttk.Entry(top_frame, width=30)
        self.search_entry.pack(side=tk.LEFT)
        ttk.Button(top_frame, text="Search", command=self.on_search).pack(side=tk.LEFT, padx=6)
        ttk.Button(top_frame, text="Refresh", command=self.refresh_all).pack(side=tk.LEFT, padx=6)

        mid_frame = ttk.Frame(self)
        mid_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

        # Listbox of media
        left_frame = ttk.Frame(mid_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ttk.Label(left_frame, text="Media items:").pack(anchor=tk.W)
        self.listbox = tk.Listbox(left_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        right_frame = ttk.Frame(mid_frame, width=300)
        right_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(8,0))
        ttk.Label(right_frame, text="Metadata:").pack(anchor=tk.W)
        self.meta_text = tk.Text(right_frame, height=12, width=40)
        self.meta_text.pack()

        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill=tk.X, pady=(8,0))
        ttk.Button(btn_frame, text="Create new", command=self.on_create).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Delete selected", command=self.on_delete).pack(side=tk.LEFT, padx=4)

        # status
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self, textvariable=self.status_var).pack(fill=tk.X, padx=8, pady=(4,8))

        # internal mapping id -> item
        self.items_map = []

    def set_status(self, txt):
        self.status_var.set(txt)

    def refresh_all(self):
        self.set_status("Loading all media...")
        try:
            r = requests.get(f"{BACKEND_URL}/media")
            r.raise_for_status()
            items = r.json()
            self.populate_list(items)
            self.set_status(f"Loaded {len(items)} items.")
            
            # FIX 1a: Clear metadata panel on full refresh
            self.meta_text.delete("1.0", tk.END) 
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load media: {e}")
            self.set_status("Error loading media")

    def populate_list(self, items):
        self.items_map = items
        self.listbox.delete(0, tk.END)
        for it in items:
            self.listbox.insert(tk.END, f"{it['name']} ({it['category']})")

    def on_category_change(self, _value=None):
        cat = self.category_var.get()
        if cat == "All":
            self.refresh_all()
            return
        self.set_status(f"Loading category {cat}...")
        try:
            r = requests.get(f"{BACKEND_URL}/media/category/{cat}")
            r.raise_for_status()
            items = r.json()
            self.populate_list(items)
            self.set_status(f"Loaded {len(items)} items in {cat}.")
            
            # FIX 1b: Clear metadata panel on category change
            self.meta_text.delete("1.0", tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load category: {e}")
            self.set_status("Error loading category")

    def on_search(self):
        name = self.search_entry.get().strip()
        if not name:
            messagebox.showinfo("Search", "Enter a name to search for (exact match).")
            return
        
        self.set_status(f"Searching for '{name}'...")
        try:
            r = requests.get(f"{BACKEND_URL}/media/search", params={"name": name})
            
            # 🚨 Clear metadata panel before showing result or error
            self.meta_text.delete("1.0", tk.END) 
            
            if r.status_code == 404:
                messagebox.showinfo("Not found", "No media found with that exact name.")
                self.set_status("Search: no results")
                return
            
            r.raise_for_status()
            item = r.json()
            self.populate_list([item])
            self.set_status("Search completed")
            
            # FIX 2: Manually select and show the metadata for the single found item
            if self.items_map:
                # Select the item in the listbox (optional, but good UX)
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(0)
                # Show the metadata for the first (and only) item found
                self.show_metadata(self.items_map[0])
                
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")
            self.set_status("Search error")

    def on_select(self, evt=None):
        sel = self.listbox.curselection()
        if not sel:
            # FIX 3: Clear panel if selection is removed (e.g., when populating a new list)
            self.meta_text.delete("1.0", tk.END) 
            return
        idx = sel[0]
        item = self.items_map[idx]
        self.show_metadata(item)

    def show_metadata(self, item):
        # Already clears the panel, so no need to add here again.
        self.meta_text.delete("1.0", tk.END) 
        text = (
            f"ID: {item['id']}\n"
            f"Name: {item['name']}\n"
            f"Author: {item['author']}\n"
            f"Publication date: {item['publication_date']}\n"
            f"Category: {item['category']}\n"
        )
        self.meta_text.insert(tk.END, text)

    def on_create(self):
        # ... (on_create logic remains the same) ...
        name = simpledialog.askstring("Create", "Name:")
        if not name:
            return
        author = simpledialog.askstring("Create", "Author:")
        if author is None:
            return
        pub_date = simpledialog.askstring("Create", "Publication date (e.g., 2020-01-01):")
        if pub_date is None:
            return
        category = simpledialog.askstring("Create", "Category (Book/Film/Magazine):")
        if category is None:
            return
        payload = {
            "name": name,
            "author": author,
            "publication_date": pub_date,
            "category": category,
        }
        try:
            r = requests.post(f"{BACKEND_URL}/media", json=payload)
            if r.status_code == 201:
                messagebox.showinfo("Success", "Media created.")
                self.refresh_all()
            else:
                messagebox.showerror("Failed", f"Create failed: {r.status_code} {r.text}")
        except Exception as e:
            messagebox.showerror("Error", f"Create error: {e}")

    def on_delete(self):
        # ... (on_delete logic remains the same) ...
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Delete", "Select an item first.")
            return
        idx = sel[0]
        item = self.items_map[idx]
        if not messagebox.askyesno("Confirm delete", f"Delete '{item['name']}'?"):
            return
        try:
            r = requests.delete(f"{BACKEND_URL}/media/{item['id']}")
            if r.status_code == 200:
                messagebox.showinfo("Deleted", "Item deleted.")
                self.refresh_all()
            else:
                messagebox.showerror("Error", f"Delete failed: {r.status_code} {r.text}")
        except Exception as e:
            messagebox.showerror("Error", f"Delete error: {e}")


if __name__ == "__main__":
    app = LibraryGUI()
    app.mainloop()