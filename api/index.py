import os
import sys

# Ensure the api directory is in Python module search path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from .app import app
except ImportError:
    from app import app

# Local development entrypoint
if __name__ == "__main__":
    app.run(debug=True)
