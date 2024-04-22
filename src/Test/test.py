import streamlink
from flask import Flask, Response
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

app = Flask(__name__)  # สร้างอินสแตนซ์ของ Flask
url1 = 'https://www.youtube.com/embed/5Lj0UIxmOhk?si=mI_mC478IHat7Fxm' # กำหนด URL สำหรับสตรีมวิดีโอจากกล้องวงจรปิด
camera1 = cv2.VideoCapture(url1)
camera2 = cv2.VideoCapture(0)  # กำหนดกล้องเป็น webcam ในเครื่อง

cred_data = {
  "type": "service_account",
  "project_id": "database-8b747",
  "private_key_id": "eea9fb1dcc71d374722fba2562ef51a93f7090fb",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCvDf2NC55lZOJA\n/jxlIq5v1my1JDJUMnYZT7/sMPwdYLRzOxIlWhGZzRA42+M5srrHCSi0sVQsIkRw\nXetUYUfVc6qksK/EHbvWoF+sYjf15TbylOyscmdz5JBhE2438IPfDwEBgrOrC/H1\nRxReqPjQLX7ZiJ88XRpMs79s0RXvNMfROJMqHQ0lKAPHB3bQYeEyY/maqWVEdKFc\nF7Knl4WV+oGCwmJ9FlECxBkxKzB1tujr+Wx7r1Na2Te+CY9v8Rdgl0U4AI4r0v7s\nUnoYNGcK1znO623Ou0Sk7WkudOiLpof+gEfyQHJumnAzDK/vziaIpEhw+jc8rb9/\nkLP6jYcjAgMBAAECggEAFiA7EYZL7X3sWRGpWZEiIjGkiNq738eHBNj/JZ/lZeMw\nu7XWK9FwExQHvmAQntzX3ctrETeur2tfYiKE2aP4G+MkSO+qL6wgb1bS8OtzLknc\nAZpQNdW5/LyBgTue/UQRrvJrCqFWC0MVwI5M5VAPLuTpOR6bHdqYteQsSFk/H/5C\n0mPLejsOKfACjZzA+7Yona/5VpNFQ7MK/hShatoEkinOtNsrEiKZ1GB1lRvaDtSi\niisa4XDrxx0qXVpND4hVz4OqiKE+gFfwjTzLqJV/IXTcafhJLpwJw9fMIyT3dATR\nBSLPG9/rHK8EMTHmn8IpScZFoFd/y2p3nxiEzh63vQKBgQDYV2g+2eYexUe/d45L\nnr9csaT7cYPkcsmk8lRXWUTqIHFUGdad6DNyg+JRHGMqB/+Ex/k9vVvkp+rCiuPm\n0m4eHMtfPpQZ/CMPGCV2dbE3hr4RdAQu7VE+gj1hpDrr2o/a6JLUEasTWtMnpICJ\nCvNaO2ciKlTHzO2juhcXtNUa/wKBgQDPJQ3BuyTqulwmKLWNxA60iKOz/NdRqMGC\neXGJRwQEyuYQ2Ud+4cGxo1ND6iZzGYaUvpj5dk7xx9cgFl6eb/IYxuU5LSZTqABi\nonxRtD88GIDg0NB+t7d9ofOiY+qyoPqVGuCqevuqrscOM7chcyWl54tzLddbmSef\nfFmUpmfH3QKBgGFkH/LDZzwM9bq1GKLkSSNyeWIUfRqXrj0KNnvIHSUFC9+fbiVS\nBe8Ufgqjq+SdCyN8XrCzkS3DhgSkP+qGaro1njw3ULbN8f52kU7dtrTXfLMgtk1l\n2oA4Y2eUZk4M61vR/V9owMoKxin/fTm0a08AlPIlelsj3wso2AJ9Dr6DAoGAHaHA\nUQlTY5ybF/5U0l3MeLjfKh0uNAk+/UogGrIk+gaIWLqsRpNG4QFrJNj2/RoWrWqC\neZUZ/+5FcNqiWGnNKQwyuDYkOG1c+L8jp5BwR0l+Dirw2F+xiPBE6OMALONoVTIO\nF3UWUTlFUlvFg6x0I0J3KVfSadED4QWpzuDrEaUCgYAyvhpGL6QXVr/4+/+DJGlT\nJqomJA5Y6yB7n7aBSyZDKW/FubvJx26VwE1F18pSbwGiczFWl0TKkLHXfHH0e3GC\nHqm4nALEcnsjflg+UqX2KzH9ZA0KNB2k9EWVB847a2645yUYdNUd1ZCzndfYPU9h\nSCWPvHaZszOd1iXeV+Zd8g==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-5gshe@database-8b747.iam.gserviceaccount.com",
  "client_id": "115368915921602947861",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-5gshe%40database-8b747.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# สร้าง object credentials จาก dictionary
cred = credentials.Certificate(cred_data)

# เริ่มต้นใช้งาน Firebase app ด้วย credentials ที่ได้
firebase_admin.initialize_app(cred, {
    'storageBucket': 'database-8b747.appspot.com'
})

db = firestore.client() # สร้างอินสแตนซ์สำหรับการติดต่อกับ Firestore
bucket = storage.bucket() # สร้างอินสแตนซ์สำหรับการติดต่อกับ Firebase Storage

local_tz = timezone('Asia/Bangkok') # กำหนดโซนเวลา

known_face_encodings = [] # รายการสำหรับเก็บ encoding ของใบหน้าที่รู้จัก
known_face_names = [] # รายการสำหรับเก็บชื่อของใบหน้าที่รู้จัก

# ฟังก์ชันเพื่อดึงข้อมูลผู้ใช้จาก Firestore และอัพเดตรายการใบหน้าที่รู้จัก
def fetch_user_data():
    global known_face_encodings, known_face_names
    known_face_encodings.clear()
    known_face_names.clear()
    users_ref = db.collection(u'users')
    docs = users_ref.stream()
    for doc in docs:
        user = doc.to_dict()
        response = requests.get(user['photoURL'])
        img = Image.open(BytesIO(response.content))
        img_np = np.array(img)
        face_encodings = face_recognition.face_encodings(img_np)
        if face_encodings:
            known_face_encodings.append(face_encodings[0])
            known_face_names.append(user['name'])

fetch_user_data()

def generate_frames(camera):
    while True:
        success, frame = camera.read()
        if not success:
            break
        yield process_frame(frame)

def process_frame(frame):
    rgb_small_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgb_small_frame = cv2.resize(rgb_small_frame, (0, 0), fx=0.25, fy=0.25)
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    current_time = datetime.datetime.now(local_tz)
    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        face_names.append(name)
        # Assuming direct upload for simplicity
    _, buffer = cv2.imencode('.jpg', frame)
    frame_bytes = buffer.tobytes()
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def setup_camera(url):
    streams = streamlink.streams(url)
    if 'best' in streams:
        best_stream = streams['best']
        return cv2.VideoCapture(best_stream.url)
    else:
        print("No available streams.")
        return None

@app.route('/video_feed')
def video_feed():
    global camera1
    return Response(generate_frames(camera1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed2')
def video_feed2():
    global camera2
    return Response(generate_frames(camera2), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    camera1 = setup_camera('https://www.youtube.com/watch?v=5Lj0UIxmOhk')
    camera2 = cv2.VideoCapture(0)
    app.run(debug=True, host='0.0.0.0', port=5000)