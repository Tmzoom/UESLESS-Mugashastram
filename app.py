from flask import Flask, render_template, request
import threading
from face import start_face_scan  # make sure this file exists

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start-scan', methods=['POST'])
def scan():
    threading.Thread(target=start_face_scan, daemon=True).start()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

