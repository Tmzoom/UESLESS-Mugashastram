import cv2
import random
import time
from gtts import gTTS
import os
from playsound import playsound  # Ensure this line is not causing conflict

comments = [
    "ഇത് മുഖമോ, മുഖച്ചുമ്മാ!",  
    "പറയാനുണ്ടെങ്കിലും പറയില്ല!", 
    "ഈ മുഖം കണ്ടിട്ട് ഞാനും ഷോക്!", 
    "പുതിയ റെക്കോർഡ് — ഏറ്റവും ക്ഷാമമുള്ള മുഖം!",
    "ഹേയ്, മുഖം പോലെ project useless അല്ലേ!",
    "വണ്ടിക്ക് മുമ്പിൽ പുള്ളിപ്പുലി!", 
    "മലയാള സിനിമാ വില്ലൻ വിൽപനയ്ക്ക്!"
    "മുഖം നല്ല പ്രകാശമുള്ളതായിരിക്കുന്നു!",
    "കണ്ണ് നല്ല ഭംഗിയുണ്ട്!"
]

# Load face detector
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)
if face_cascade.empty():
    print("Failed to load face cascade:", cascade_path)
    exit()

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Webcam not accessible.")
    exit()

last_spoken_time = 0
cooldown = 5  # seconds
last_comment = "മുഖശാസ്ത്രം"  # Default text

while True:
    ret, frame = cap.read()
    if not ret:
        print("Webcam read error!")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(60, 60)  # Detect faces at least 60x60
)

    print("Faces detected:", len(faces))  # DEBUG LINE

    current_time = time.time()

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        if current_time - last_spoken_time > cooldown:
            last_comment = random.choice(comments)

            # Speak the comment
            try:
                tts = gTTS(text=last_comment, lang='ml')
                tts.save("comment.mp3")
                playsound("comment.mp3")
                os.remove("comment.mp3")
            except Exception as e:
                print("Voice error:", e)

            last_spoken_time = current_time

        # Display the comment on screen
        cv2.putText(frame, last_comment, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    title = f'മുഖശാസ്ത്രം | Faces Detected: {len(faces)}'
    cv2.imshow(title, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/file')
def file_page():
    return render_template('index.html')  # This serves index.html

if __name__ == '__main__':
    app.run(debug=True)
