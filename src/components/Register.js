import React, { useState } from 'react'; // นำเข้า React และ Hook useState สำหรับจัดการ state
import { Link } from 'react-router-dom'; // นำเข้า Link จาก react-router-dom สำหรับการนำทาง
import { createUserWithEmailAndPassword } from "firebase/auth"; // นำเข้าฟังก์ชันสำหรับสร้างบัญชีผู้ใช้ด้วยอีเมลและรหัสผ่าน
import { auth } from '../firebase'; // นำเข้าอ็อบเจกต์ auth จากไฟล์ตั้งค่า firebase
import '../styles/register.css';

const Register = () => {
    const [email, setEmail] = useState(''); // สร้าง state สำหรับจัดเก็บอีเมลและฟังก์ชันเพื่ออัพเดท
    const [password, setPassword] = useState(''); // สร้าง state สำหรับจัดเก็บรหัสผ่านและฟังก์ชันเพื่ออัพเดท

    const handleEmailChange = (event) => {
        setEmail(event.target.value); // อัพเดทอีเมลใน state เมื่อมีการเปลี่ยนแปลงใน input
    };

    const handlePasswordChange = (event) => {
        setPassword(event.target.value); // อัพเดทรหัสผ่านใน state เมื่อมีการเปลี่ยนแปลงใน input
    };

    const handleSubmit = async (event) => {
        event.preventDefault(); // ป้องกันการทำงานของฟอร์มแบบปกติ (การรีเฟรชหน้า)
        try {
            const userCredential = await createUserWithEmailAndPassword(auth, email, password); // สร้างบัญชีผู้ใช้ใหม่ด้วยอีเมลและรหัสผ่านใน Firebase Authentication
            console.log('User registered:', userCredential.user); // บันทึกข้อความว่าผู้ใช้ได้รับการลงทะเบียน
            alert('User successfully registered.');  // แสดงข้อความแจ้งเตือน
            // ทำสิ่งที่คุณต้องการเมื่อลงทะเบียนสำเร็จ เช่น นำไปยังหน้าลงทะเบียนสำเร็จหรือให้ผู้ใช้เข้าสู่ระบบโดยอัตโนมัติ
        } catch (error) {
            console.error('Error registering user:', error.message); // บันทึกข้อผิดพลาดเมื่อการลงทะเบียนไม่สำเร็จ
            alert('Error registering user: ' + error.message); // แสดงข้อความแจ้งเตือนข้อผิดพลาด
            // ประมวลผลข้อผิดพลาดที่เกิดขึ้นในการลงทะเบียน
        }
    };

    return (
        <div>
            <br /><br /><br />
            <div className="register-container">
                <h2>Register</h2>
                <form onSubmit={handleSubmit}>
                    <div>
                        <label htmlFor="email">Email:</label><br />
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={handleEmailChange}
                        />
                    </div>
                    <div>
                        <label htmlFor="password">Password:</label><br />
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={handlePasswordChange}
                        />
                    </div>
                    <button type="submit">Register</button>
                </form>
                <p>
                    Already have an account? <Link to="/login">Login</Link>
                </p>
            </div>
        </div>
    );
};

export default Register; // ส่งออกคอมโพเนนต์ Register เพื่อใช้งานในส่วนอื่นๆ ของแอป
