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
import time
import json

app = Flask(__name__)  # สร้างอินสแตนซ์ของ Flask
url1 = 'rtsp://admin:wave15042544.@192.168.1.64/Streaming/Channels/101' # กำหนด URL สำหรับสตรีมวิดีโอจากกล้องวงจรปิด
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
    """Fetch user data from Firestore and update known face encodings and names."""
    global known_face_encodings, known_face_names
    known_face_encodings.clear() # ล้างรายการ encoding
    known_face_names.clear() # ล้างรายการชื่อ
    users_ref = db.collection(u'users') # อ้างอิงคอลเล็กชันผู้ใช้
    docs = users_ref.stream()  # ดึงข้อมูลผู้ใช้
    for doc in docs:
        user = doc.to_dict() # แปลงเอกสารเป็นดิกชันนารี
        if user['name'] in known_face_names: # ถ้าชื่อผู้ใช้มีอยู่แล้วให้ข้ามไป
            continue
        else:
            face_encodings = [np.array(json.loads(encoding)) for encoding in user['face_encodings']] # แปลง encoding จาก string เป็นอาร์เรย์ numpy
            known_face_names.append(user['name'])
            known_face_encodings.append(face_encodings[0]) # เพิ่ม encoding ลงในรายการ
          



face_last_seen = {name: False for name in known_face_names} # สร้างดิกชันนารีเพื่อติดตามใบหน้าที่เห็นล่าสุด

def generate_frames(camera): # ฟังก์ชันสร้างเฟรมภาพสำหรับการสตรีม
    global face_last_seen

    fetch_user_data() # ดึงข้อมูลผู้ใช้อัพเดตล่าสุด

    while True:
        success, frame = camera.read() # อ่านเฟรมจากกล้อง
        if not success:
            break

        # ปรับแต่งรูปภาพเพื่อให้เหมาะสมกับการจดจำใบหน้า
        rgb_small_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # แปลงสีภาพ
        rgb_small_frame = cv2.resize(rgb_small_frame, (0, 0), fx=0.25, fy=0.25) # ปรับขนาดภาพ

        # หาตำแหน่งและ encoding ของใบหน้าในเฟรม
        face_locations = face_recognition.face_locations(rgb_small_frame) 
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)  

        current_time = datetime.datetime.now(local_tz) # ดึงเวลาปัจจุบัน
        faces_currently_seen = {name: False for name in known_face_names}
        
        face_names = []
        for face_encoding in face_encodings:
            # ตรวจสอบว่าใบหน้าตรงกับใบหน้าที่รู้จักหรือไม่
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown" # ตั้งชื่อเริ่มต้นเป็น "Unknown"

            # ใช้ใบหน้าที่มีระยะห่างน้อยที่สุด
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index] # กำหนดชื่อใบหน้า

            face_names.append(name) # เพิ่มชื่อใบหน้าในรายการ

            # ถ้ามีใบหน้าใหม่หรือเห็นใบหน้าเดิมอีกครั้ง บันทึกภาพ
            if not face_last_seen.get(name, False):
                timestamp_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")
                user_folder = f"{name}/{name}_{timestamp_str}.jpg"
                all_folder = f"All/{name}_{timestamp_str}.jpg"
                _, img_encoded = cv2.imencode('.jpg', frame)
                img_bytes = img_encoded.tobytes()
                # อัพโหลดไปยังโฟลเดอร์ผู้ใช้
                user_blob = bucket.blob(user_folder)
                user_blob.upload_from_string(img_bytes, content_type='image/jpeg')
                # อัพโหลดไปยังโฟลเดอร์ทั้งหมด
                all_blob = bucket.blob(all_folder)
                all_blob.upload_from_string(img_bytes, content_type='image/jpeg')
                face_last_seen[name] = True

            faces_currently_seen[name] = True

        # อัพเดทดิกชันนารีเพื่อสะท้อนใบหน้าที่เห็นในเฟรมปัจจุบัน
        for name in face_last_seen.keys():
            face_last_seen[name] = faces_currently_seen.get(name, False)

        # แสดงผลภาพบนเฟรม (เลือกใช้ได้)
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # ขยายขนาดตำแหน่งใบหน้าเพราะเฟรมที่ตรวจจับเป็นขนาด 1/4
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # วาดกรอบรอบใบหน้า
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # วาดป้ายชื่อมีชื่อด้านล่างใบหน้า
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # เพิ่มวันที่และเวลาในแต่ละเฟรม (เลือกใช้ได้)
        timestamp_text = current_time.strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, timestamp_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # แปลงภาพเป็นไบต์และส่งเซฟ
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.2)





def extract_face_encodings(image_url):
    """Extract face encodings from an image URL."""
    response = requests.get(image_url)
    image = face_recognition.load_image_file(BytesIO(response.content))
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    return face_encodings

def save_encodings_to_firestore(user_name, encodings):
    """Save face encodings to Firestore."""
    db = firestore.client()
    db.collection('users').document(user_name).set({
        'face_encodings': [json.dumps(encoding.tolist()) for encoding in encodings],
        'processed': True
    }, merge=True)
   

def check_if_processed(user_name):
    """Check if the user's image has already been processed."""
    db = firestore.client()
    doc_ref = db.collection('users').document(user_name)
    doc = doc_ref.get()
    if doc.exists:
        if doc.to_dict().get('processed'):
            return True
    return False

def list_and_process_images():
    """get images from photoURL and process them."""
    db = firestore.client()
    docs = db.collection('users').stream()
    for doc in docs:
        user_name = doc.id
        photoURL = doc.to_dict().get('photoURL')
        if not check_if_processed(user_name):
            encodings = extract_face_encodings(photoURL)
            save_encodings_to_firestore(user_name, encodings)
            print(f'{user_name} processed.')
        else:
            print(f'{user_name} already processed.')



        

@app.route('/video_feed') # กำหนดเส้นทางสำหรับวิดีโอสตรีม
def video_feed():
    return Response(generate_frames(camera1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed2') # กำหนดเส้นทางสำหรับวิดีโอสตรีมอีกตัว
def video_feed2():
    return Response(generate_frames(camera2), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/update_encode')
def update_encode():
    list_and_process_images()
    fetch_user_data()
    return Response("complete")
    







if __name__ == '__main__': 
    fetch_user_data() # เรียกฟังก์ชันเพื่อดึงข้อมูลผู้ใช้# เริ่มรันแอปพลิเคชัน
    app.run(debug=True)
