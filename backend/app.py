
import os
import sys

# Add project root to sys.path to enable absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)