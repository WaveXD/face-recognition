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
url1 = 'rtsp://admin:wave15042544.@192.168.1.64/Streaming/Channels/101' # กำหนด URL สำหรับสตรีมวิดีโอจากกล้องวงจรปิด
camera1 = cv2.VideoCapture(url1)
camera2 = cv2.VideoCapture(0)  # กำหนดกล้องเป็น webcam ในเครื่อง

cred = credentials.Certificate("C:/Users/Wave/Desktop/finalproject/backend/database-8b747-firebase-adminsdk-5gshe-eea9fb1dcc.json")
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
        photo_url = user['photoURL'] # ดึง URL รูปภาพ
        response = requests.get(photo_url) # ทำ HTTP request ไปยัง URL
        img = Image.open(BytesIO(response.content)) # เปิดรูปภาพจากข้อมูลไบนารี
        img_np = np.array(img) # แปลงรูปภาพเป็นอาร์เรย์ numpy
        face_encodings = face_recognition.face_encodings(img_np) # หา encoding ใบหน้า
        if face_encodings:
            known_face_encodings.append(face_encodings[0]) # เพิ่ม encoding ลงในรายการ
            known_face_names.append(user['name']) # เพิ่มชื่อลงในรายการ

fetch_user_data() # เรียกฟังก์ชันเพื่อดึงข้อมูลผู้ใช้

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

@app.route('/video_feed') # กำหนดเส้นทางสำหรับวิดีโอสตรีม
def video_feed():
    return Response(generate_frames(camera1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed2') # กำหนดเส้นทางสำหรับวิดีโอสตรีมอีกตัว
def video_feed2():
    return Response(generate_frames(camera2), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__': # เริ่มรันแอปพลิเคชัน
    app.run(debug=True)
