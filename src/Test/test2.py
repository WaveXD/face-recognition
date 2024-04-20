from flask import Flask, Response
from flask_cors import CORS  # Import CORS
import cv2
import face_recognition
import numpy as np
import datetime
from pytz import timezone
import firebase_admin
from firebase_admin import credentials, firestore, storage
import requests
from PIL import Image
from io import BytesIO

app = Flask(__name__)
CORS(app)  # Enable CORS

url1 = 'rtsp://admin:wave15042544.@192.168.1.64/Streaming/Channels/101'
camera1 = cv2.VideoCapture(url1)
camera2 = cv2.VideoCapture(0)  # Assuming this is the index for your webcam

cred = credentials.Certificate("C:/Users/Wave/Desktop/finalproject/backend/database-8b747-firebase-adminsdk-5gshe-eea9fb1dcc.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'database-8b747.appspot.com'
})

db = firestore.client()
bucket = storage.bucket()

local_tz = timezone('Asia/Bangkok')

known_face_encodings = []
known_face_names = []

def fetch_user_data():
    global known_face_encodings, known_face_names
    known_face_encodings.clear()
    known_face_names.clear()
    users_ref = db.collection(u'users')
    docs = users_ref.stream()
    for doc in docs:
        user = doc.to_dict()
        photo_url = user['photoURL']
        response = requests.get(photo_url)
        img = Image.open(BytesIO(response.content))
        img_np = np.array(img)
        face_encodings = face_recognition.face_encodings(img_np)
        if face_encodings:
            known_face_encodings.append(face_encodings[0])
            known_face_names.append(user['name'])

def generate_frames(camera):
    global face_last_seen

    fetch_user_data()

    while True:
        success, frame = camera.read()
        if not success:
            continue  # Skip the rest of the code in this iteration

        rgb_small_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_small_frame = cv2.resize(rgb_small_frame, (0, 0), fx=0.5, fy=0.5)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        current_time = datetime.datetime.now(local_tz)
        faces_currently_seen = {name: False for name in known_face_names}

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            if len(face_encodings) > 0:
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                if len(face_distances) > 0:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
            face_names.append(name)

            if not face_last_seen.get(name, False):
                timestamp_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")
                user_folder = f"{name}/{name}_{timestamp_str}.jpg"
                all_folder = f"All/{name}_{timestamp_str}.jpg"
                _, img_encoded = cv2.imencode('.jpg', frame)
                img_bytes = img_encoded.tobytes()
                user_blob = bucket.blob(user_folder)
                user_blob.upload_from_string(img_bytes, content_type='image/jpeg')
                all_blob = bucket.blob(all_folder)
                all_blob.upload_from_string(img_bytes, content_type='image/jpeg')
                face_last_seen[name] = True

            faces_currently_seen[name] = True

        for name in face_last_seen.keys():
            face_last_seen[name] = faces_currently_seen.get(name, False)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        timestamp_text = current_time.strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, timestamp_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(camera1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed2')
def video_feed2():
    return Response(generate_frames(camera2), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
