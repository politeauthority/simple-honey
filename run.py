"""
Python runner script

"""

from app import app

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=80,
        debug=True
    )

# End File: simple-honey/run.py
