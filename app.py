from flask import Flask, render_template, render_template_string
import subprocess
import sys
import os

# 🟢 Define app FIRST
app = Flask(__name__)

# 🟢 Route for home page
@app.route("/")
def index():
    return render_template("index.html")

# 🟢 Route for starting the face scan
@app.route("/start-scan", methods=["POST"])
def start_scan():
    try:
        # Open face scanner in new terminal window (Windows-specific)
        subprocess.Popen(
            [sys.executable, "face.py"],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        return render_template_string("<h1>🔍 Scanning started in new window!<br><a href='/'>Back</a></h1>")
    except Exception as e:
        return f"Error running scanner: {e}"

# 🟢 Run app
if __name__ == "__main__":
    app.run(debug=True)


