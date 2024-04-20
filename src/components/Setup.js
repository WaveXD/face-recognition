import React, { useState } from 'react';
import { getFirestore, collection, addDoc } from 'firebase/firestore'; // นำเข้าฟังก์ชันจัดการข้อมูล Firestore
import { getStorage, ref, uploadBytes, getDownloadURL } from 'firebase/storage'; // นำเข้าฟังก์ชันจัดการไฟล์บน Firebase Storage
import app from '../firebase'; // ตรวจสอบเส้นทางการเชื่อมต่อ Firebase
import Navbar from './Navbar'; // ตรวจสอบเส้นทางการเชื่อมต่อ
import '../styles/Setup.css';

function Setup() {
  const [userName, setUserName] = useState(''); // กำหนด state สำหรับจัดเก็บชื่อผู้ใช้
  const [file, setFile] = useState(null); // กำหนด state สำหรับจัดเก็บไฟล์
  const firestore = getFirestore(app); // รับอินสแตนซ์ของ Firestore จากแอป Firebase
  const storage = getStorage(app); // รับอินสแตนซ์ของ Storage จากแอป Firebase

  const handleFileChange = (e) => { // ฟังก์ชันจัดการเมื่อมีการเปลี่ยนแปลงไฟล์
    setFile(e.target.files[0]); // อัปเดต state ไฟล์เมื่อผู้ใช้เลือกไฟล์
  };

  const addUser = async (userName, file) => { // ฟังก์ชัน asynchronous สำหรับเพิ่มผู้ใช้
    try {
      const storageRef = ref(storage, `Users/${file.name}`); // สร้าง reference ไฟล์ใน Storage
      const metadata = { // กำหนด metadata สำหรับไฟล์
        contentType: file.type, // ชนิดของไฟล์
        customMetadata: {
          'processed': 'false', // ตั้งค่าเริ่มต้นเป็น 'false' เพื่อรอการประมวลผล
        }
      };
      const snapshot = await uploadBytes(storageRef, file, metadata); // อัปโหลดไฟล์พร้อม metadata
      const photoURL = await getDownloadURL(snapshot.ref); // รับ URL ของไฟล์ที่อัปโหลด

      const docRef = await addDoc(collection(firestore, "users"), { // เพิ่มข้อมูลผู้ใช้ใน Firestore
        name: userName,
        photoURL: photoURL,
        processed: false
      });

      console.log("User added with ID: ", docRef.id); // บันทึก ID ของผู้ใช้ใหม่ใน console
      alert('User added successfully! Processing will complete soon.'); // แจ้งผู้ใช้ว่าเพิ่มผู้ใช้สำเร็จ
    } catch (error) {
      console.error("Error adding user: ", error); // บันทึกข้อผิดพลาดใน console
      alert('Failed to add user.'); // แจ้งข้อผิดพลาดให้ผู้ใช้
    }
  };

  const handleSubmit = async (e) => { // ฟังก์ชันจัดการเมื่อส่งฟอร์ม
    e.preventDefault(); // ป้องกันการทำงานของฟอร์มแบบปกติ
    if (file && userName) { // เช็คว่าได้รับชื่อผู้ใช้และไฟล์แล้วหรือไม่
      await addUser(userName, file); // เรียกฟังก์ชันเพิ่มผู้ใช้
    } else {
      alert("Missing userName or file"); // แจ้งเตือนหากขาดข้อมูล
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
