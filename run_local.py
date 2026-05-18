"""Standalone script to run the WarmaStats Flask app locally."""

from web_app import app

if __name__ == "__main__":
    print("Starting WarmaStats locally at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)

