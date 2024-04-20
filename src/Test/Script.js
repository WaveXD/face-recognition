import React, { useState } from 'react';
import { getFirestore, collection, addDoc } from 'firebase/firestore';
import { getStorage, ref, uploadBytes, getDownloadURL } from 'firebase/storage';
import app from '../firebase'; // ตรวจสอบเส้นทางการเชื่อมต่อ Firebase
import Navbar from '../components/Navbar.js'; // ตรวจสอบเส้นทางการเชื่อมต่อ
import '../styles/Setup.css';
import { faceapi } from '@vladmandic/face-api'; // นำเข้าไลบรารี face-api

function Setup() {
  const [userName, setUserName] = useState('');
  const [file, setFile] = useState(null);
  const firestore = getFirestore(app);
  const storage = getStorage(app);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const addUser = async (userName, file) => {
    try {
      const storageRef = ref(storage, `Users/${file.name}`);
      const metadata = {
        contentType: file.type,
        customMetadata: {
          'processed': 'false', // ตั้งค่าเริ่มต้นเป็น 'false' เพื่อรอการประมวลผล
        }
      };
      const snapshot = await uploadBytes(storageRef, file, metadata);
      const photoURL = await getDownloadURL(snapshot.ref);

      // โหลดโมเดลการตรวจจับใบหน้า
      await faceapi.loadFaceDetectionModel('/models');

      // ตรวจจับใบหน้าในรูปภาพ
      const detections = await faceapi.detectAllFaces(file);

      // ตรวจสอบว่ามีใบหน้าในรูปภาพหรือไม่
      if (detections.length > 0) {
        // รับค่า Encoding ของใบหน้าแรก
        const encoding = detections[0].descriptor;

        // เพิ่มค่า Encoding ลงในเอกสารผู้ใช้
        await addDoc(collection(firestore, "users"), {
          name: userName,
          photoURL: photoURL,
          processed: true,
          encoding: encoding
        });
      } else {
        // แสดงข้อความแจ้งเตือนหากไม่พบใบหน้า
        alert('No face detected in the image.');
      }

      console.log("User added with ID: ", docRef.id);
      alert('User added successfully! Processing complete.');
    } catch (error) {
      console.error("Error adding user: ", error);
      alert('Failed to add user.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (file && userName) {
      await addUser(userName, file);
    } else {
      alert("Missing userName or file");
    }
  };

  return (
    <div>
      <Navbar />
      <div className="setup-container">
        <h1 className="setup-title">Setup New User</h1>
        <form onSubmit={handleSubmit} className="setup-form">
          <input
            className="setup-input"
            type="text"
            value={userName}
            onChange={(e) => setUserName(e.target.value)}
            placeholder="User Name"
            required
          />
          <input
            className="setup-file-input"
            type="file"
            onChange={handleFileChange}
            required
          />
          <button className="setup-submit-btn" type="submit">Submit</button>
        </form>
      </div>
    </div>
  );
}

export default Setup;
