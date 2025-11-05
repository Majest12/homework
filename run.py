# run.py
# This file imports the app instance from api.py and runs it.

from backend.api import app 

if __name__ == '__main__':
    # Run the app on the default host and port
    app.run(debug=True)