import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { signOut } from "firebase/auth";
import { auth } from '../firebase';

const Logout = () => {
    const navigate = useNavigate(); // กำหนดฟังก์ชัน navigate จาก useNavigate เพื่อใช้สำหรับการนำทางผู้ใช้

    useEffect(() => {
        const logout = async () => { // กำหนดฟังก์ชัน logout แบบ asynchronous
            try {
                await signOut(auth); // พยายามออกจากระบบผู้ใช้โดยใช้อ็อบเจกต์ auth ของ Firebase
                localStorage.removeItem('isLoggedIn'); // ลบรายการ 'isLoggedIn' ออกจาก local storage เพื่อจัดการสถานะการเข้าสู่ระบบ
                alert('You have been logged out.'); // แจ้งผู้ใช้ว่าได้ทำการออกจากระบบเรียบร้อยแล้ว
                navigate('/login'); // นำทางไปยังหน้าล็อกอินหลังจากการออกจากระบบสำเร็จ
            } catch (error) {
                console.error('Error logging out:', error); // บันทึกข้อผิดพลาดไปยังคอนโซลหากการออกจากระบบล้มเหลว
                alert('Error logging out: ' + error.message); // แจ้งข้อผิดพลาดให้ผู้ใช้รู้ถ้าการออกจากระบบล้มเหลว
            }
        };

        logout(); // เรียกฟังก์ชัน logout เมื่อ component ถูกติดตั้ง
    }, [navigate]); // อาเรย์ขึ้นอยู่กับ useEffect ประกอบด้วย navigate เพื่อจัดการการเปลี่ยนแปลงในการนำทาง

    return null; // Component ไม่แสดงผลอะไรบน UI, จึงคืนค่า null
};

export default Logout; // ส่งออกคอมโพเนนต์ Logout