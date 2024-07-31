import webview
from threading import Thread
import subprocess

def start_flask():
    subprocess.Popen(["python", "app.py"])

# Start Flask server in a separate thread
flask_thread = Thread(target=start_flask)
flask_thread.start()

# Create a webview window with the Flask app
webview.create_window("Button Example", "http://127.0.0.1:5000/")
webview.start()
