import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTableWidget, QTableWidgetItem, QComboBox, QLineEdit, QPushButton, 
    QLabel, QGridLayout, QMessageBox, QInputDialog, QHeaderView
)
from PyQt6.QtCore import Qt

# Ensure this import matches the file name 'api_client.py' in the same directory
from .api_client import ApiClient

# --- Constants and Setup ---
CATEGORIES = ["All", "Book", "Film", "Magazine"]
METADATA_FIELDS = ["id", "Name", "Author", "Publication date", "Category"]
# Headers for the table display
TABLE_HEADERS = ["ID", "Name", "Author", "Publication Date", "Category"] 

class LibraryApp(QMainWindow):
    """Main application window for the Online Library GUI."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Online Library Management (PyQt6)")
        self.setGeometry(100, 100, 1200, 700)
        
        self.api_client = ApiClient()
        
        # Central Widget and Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Left Panel: List and Controls
        self.list_panel = QWidget()
        list_layout = QVBoxLayout(self.list_panel)
        main_layout.addWidget(self.list_panel, 2) 

        self._init_controls(list_layout)
        self._init_table(list_layout)

        # Right Panel: Details and Actions
        self.detail_panel = QWidget()
        self.detail_panel.setFixedWidth(400)
        detail_layout = QVBoxLayout(self.detail_panel)
        main_layout.addWidget(self.detail_panel, 1) 
        
        self._init_details_view(detail_layout)
        
        # Initial load attempt
        self.load_media()

    # --- Initialization Methods ---
        
    def _init_controls(self, layout):
        """Initializes filter and search controls."""
        control_group = QWidget()
        control_layout = QGridLayout(control_group)

        # Category Filter (Endpoint 2)
        control_layout.addWidget(QLabel("Filter by Category:"), 0, 0)
        self.category_combo = QComboBox()
        self.category_combo.addItems(CATEGORIES)
        self.category_combo.currentTextChanged.connect(self.filter_media)
        control_layout.addWidget(self.category_combo, 0, 1)

        # Search by Name (Endpoint 3)
        control_layout.addWidget(QLabel("Search by Name:"), 1, 0)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter exact name...")
        control_layout.addWidget(self.search_input, 1, 1)
        
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_media)
        control_layout.addWidget(self.search_button, 1, 2)

        # Allow pressing Enter in the search input to trigger the search
        self.search_input.returnPressed.connect(self.search_media)

        # Create Button (Endpoint 5)
        self.create_button = QPushButton("Create New Media")
        self.create_button.clicked.connect(self.show_create_dialog)
        control_layout.addWidget(self.create_button, 0, 2)
        
        layout.addWidget(control_group)

    def _init_table(self, layout):
        """Initializes the QTableWidget for displaying media list."""
        self.media_table = QTableWidget()
        self.media_table.setColumnCount(len(TABLE_HEADERS))
        self.media_table.setHorizontalHeaderLabels(TABLE_HEADERS)
        self.media_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.media_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # Auto-resize columns
        header = self.media_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) 

        # Connect selection event to display details (Endpoint 4)
        self.media_table.itemSelectionChanged.connect(self.display_selected_details)
        
        layout.addWidget(self.media_table)

    def _init_details_view(self, layout):
        """Initializes the panel to show metadata and the delete button."""
        layout.addWidget(QLabel("<h2>Selected Media Details</h2>"))
        
        # Grid layout for detail display
        self.detail_labels = {}
        detail_grid = QGridLayout()
        
        for i, field in enumerate(METADATA_FIELDS):
            detail_grid.addWidget(QLabel(f"<b>{field.replace('_', ' ')}:</b>"), i, 0)
            value_label = QLabel("N/A")
            self.detail_labels[field] = value_label
            detail_grid.addWidget(value_label, i, 1)

        layout.addLayout(detail_grid)
        layout.addStretch(1) 

        # Delete Button (Endpoint 6)
        self.delete_button = QPushButton("Delete Selected Media")
        self.delete_button.setStyleSheet("background-color: #f44336; color: white;")
        self.delete_button.clicked.connect(self.delete_media)
        self.delete_button.setEnabled(False)
        layout.addWidget(self.delete_button)

    # --- Data Loading and Filtering ---

    def load_media(self, media_data=None):
        """Loads data into the table, handling potential errors."""
        # Clear any previous selection so old details do not remain
        self.media_table.clearSelection()
        # Also clear detail labels immediately when loading new list
        for label in self.detail_labels.values():
            label.setText("N/A")
        self.delete_button.setEnabled(False)
        
        if media_data is None:
            # Endpoint 1: Load all media
            media_data = self.api_client.get_all_media()
            
            # Handle connection/API error
            if isinstance(media_data, dict) and "error" in media_data:
                 QMessageBox.critical(self, "Connection Error", media_data["error"])
                 self.media_table.setRowCount(0)
                 return
                 
        self.media_table.setRowCount(len(media_data))
        
        for row, item in enumerate(media_data):
            media_id = str(item.get("id", "")) 
            
            # Create the list of values to display in the table
            display_values = [media_id] + [item.get(field) for field in METADATA_FIELDS[1:]] 

            for col, value in enumerate(display_values):
                cell = QTableWidgetItem(str(value))
                self.media_table.setItem(row, col, cell)
                
        if not media_data and self.category_combo.currentText() == "All":
             self.statusBar().showMessage("No media items found.", 3000)

    def filter_media(self):
        """Called when category dropdown changes (Endpoint 2)."""
        category = self.category_combo.currentText()
        if category == "All":
            self.load_media()
        else:
            media_data = self.api_client.get_media_by_category(category)
            if isinstance(media_data, dict) and "error" in media_data:
                QMessageBox.critical(self, "API Error", media_data["error"])
            else:
                self.load_media(media_data)

    def search_media(self):
        """Called when Search button is clicked (Endpoint 3)."""
        name = self.search_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Required", "Please enter the exact name of the medium to search.")
            return

        media_data = self.api_client.search_media_by_name(name)
        if isinstance(media_data, dict) and "error" in media_data:
             QMessageBox.critical(self, "API Error", media_data["error"])
        else:
             self.load_media(media_data)
             # If results found, select the first row to trigger detail display
             if media_data and len(media_data) > 0:
                 self.media_table.selectRow(0)
             else:
                 QMessageBox.information(self, "Search Result", f"No media found with the exact name: '{name}'.")


    # --- Detail and Action Methods ---

    def display_selected_details(self):
        """Displays metadata of the selected row (Endpoint 4)."""
        # Use selection model to find selected row(s)
        selected_rows = self.media_table.selectionModel().selectedRows()
        if not selected_rows:
            # Clear details if nothing is selected
            for label in self.detail_labels.values():
                label.setText("N/A")
            self.delete_button.setEnabled(False)
            return

        row = selected_rows[0].row()
        id_item = self.media_table.item(row, 0)
        media_id = id_item.text() if id_item is not None else None

        if not media_id:
            for label in self.detail_labels.values():
                label.setText("N/A")
            self.delete_button.setEnabled(False)
            return

        # Load details from API
        details = self.api_client.get_media_details(media_id)

        if isinstance(details, dict) and "error" in details:
            QMessageBox.critical(self, "API Error", details["error"])
            self.delete_button.setEnabled(False)
            return

        # Update detail labels (ensure string conversion)
        for field in METADATA_FIELDS:
            self.detail_labels[field].setText(str(details.get(field, "N/A")))

        self.delete_button.setEnabled(True)

    def show_create_dialog(self):
        """Presents a dialog for creating a new media item (Endpoint 5)."""
        
        # Note: A custom form widget is better, but QInputDialog is used for simplicity
        
        name, ok = QInputDialog.getText(self, "Create Media", "Name:")
        if not ok or not name: return
        
        author, ok = QInputDialog.getText(self, "Create Media", "Author:")
        if not ok or not author: return

        pub_date, ok = QInputDialog.getText(self, "Create Media", "Publication Date:")
        if not ok or not pub_date: return

        # Categories list excludes "All"
        category, ok = QInputDialog.getItem(self, "Create Media", "Category:", CATEGORIES[1:], editable=False)
        if not ok or not category: return
        
        data = {
            "Name": name.strip(),
            "Author": author.strip(),
            "Publication date": pub_date.strip(),
            "Category": category,
        }
        
        result = self.api_client.create_media(data) # Endpoint 5

        if isinstance(result, dict) and "error" in result:
            QMessageBox.critical(self, "Creation Failed", result["error"])
        else:
            QMessageBox.information(self, "Success", f"Media '{name}' created successfully!")
            self.load_media() # Reload the list

    def delete_media(self):
        """Deletes the selected media item (Endpoint 6)."""
        selected_items = self.media_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Selection Required", "Please select a media item to delete.")
            return

        # Get the ID and name of the selected item
        row = selected_items[0].row()
        media_id = self.media_table.item(row, 0).text()
        media_name = self.media_table.item(row, 1).text()

        reply = QMessageBox.question(self, 'Confirm Delete',
            f"Are you sure you want to permanently delete '{media_name}' (ID: {media_id})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            result = self.api_client.delete_media(media_id) # Endpoint 6

            if isinstance(result, dict) and "error" in result:
                QMessageBox.critical(self, "Deletion Failed", result["error"])
            else:
                QMessageBox.information(self, "Success", f"Media '{media_name}' deleted successfully!")
                self.load_media() # Reload the list
                for label in self.detail_labels.values():
                    label.setText("N/A") # Clear details
                self.delete_button.setEnabled(False)

# --- Main Execution ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec())