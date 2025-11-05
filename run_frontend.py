# run_frontend.py
# This file runs the GUI application by correctly importing the module.

import sys
from PyQt6.QtWidgets import QApplication
# The correct way to import the application when running from the root
from frontend.gui import LibraryApp 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec())