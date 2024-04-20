import cv2

# URL สำหรับวิดีโอสตรีม MJPEG จากกล้อง IP
stream_url = 'rtsp://admin:wave15042544.@192.168.1.64/Streaming/Channels/102'

# สร้างอ็อบเจ็กต์ VideoCapture
cap = cv2.VideoCapture(stream_url)

# ตรวจสอบว่าการเชื่อมต่อสำเร็จหรือไม่
if not cap.isOpened():
    print("Error: Could not open stream.")
else:
    try:
        while True:
            # อ่านภาพจากสตรีม
            ret, frame = cap.read()
            if not ret:
                print("Error: Can't receive frame (stream end?). Exiting ...")
                break
            
            # แสดงภาพในหน้าต่าง
            cv2.imshow('MJPEG Video Stream', frame)
            
            # กด 'q' เพื่อออกจาก loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # ปิดการเชื่อมต่อและหน้าต่าง
        cap.release()
        cv2.destroyAllWindows()
