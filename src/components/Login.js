import React, { useState, useEffect } from 'react'; // นำเข้า React และ Hooks useState, useEffect สำหรับจัดการ state และ lifecycle
import { Link, useNavigate } from 'react-router-dom'; // นำเข้า Link และ Hook useNavigate สำหรับการนำทางและลิงก์ภายในเว็บแอป
import { signInWithEmailAndPassword } from "firebase/auth"; // นำเข้าฟังก์ชันสำหรับล็อกอินด้วยอีเมลและรหัสผ่านจาก Firebase
import { auth } from '../firebase'; // นำเข้าอ็อบเจกต์ auth จากไฟล์ตั้งค่า Firebase
import '../styles/login.css';

const Login = () => {
    const [email, setEmail] = useState(''); // สร้าง state สำหรับจัดเก็บอีเมล
    const [password, setPassword] = useState(''); // สร้าง state สำหรับจัดเก็บรหัสผ่าน
    const [loading, setLoading] = useState(false); // สร้าง state สำหรับติดตามสถานะการโหลดของการล็อกอิน
    const navigate = useNavigate(); // Hook สำหรับการนำทางไปยังหน้าอื่น

    // Hook useEffect สำหรับเช็คว่าผู้ใช้ล็อกอินอยู่แล้วหรือไม่
    useEffect(() => {
        const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
        if (isLoggedIn) {
            navigate('/history'); // นำทางไปหน้าหลักถ้าผู้ใช้ล็อกอินอยู่แล้ว
        }
    }, [navigate]); // ขึ้นอยู่กับการเปลี่ยนแปลงของ navigate

    const handleEmailChange = (event) => {
        setEmail(event.target.value); // อัพเดต state อีเมลเมื่อมีการเปลี่ยนแปลงใน input
    };

    const handlePasswordChange = (event) => {
        setPassword(event.target.value); // อัพเดต state รหัสผ่านเมื่อมีการเปลี่ยนแปลงใน input
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true); // ตั้งค่า loading เป็น true เพื่อแสดงการโหลด
        try {
            await signInWithEmailAndPassword(auth, email, password); // ล็อกอินด้วยอีเมลและรหัสผ่าน
            localStorage.setItem('isLoggedIn', 'true'); // เก็บสถานะล็อกอินไว้ใน localStorage
            alert('Login successful!'); // แสดงข้อความแจ้งเตือนว่าล็อกอินสำเร็จ
            navigate('/history'); // นำทางไปหน้า history หลังจากล็อกอินสำเร็จ
        } catch (error) {
            console.error('Error logging in:', error.message); // บันทึกข้อผิดพลาดการล็อกอินใน console
            alert('Error logging in: ' + error.message); // แสดงข้อความแจ้งเตือนข้อผิดพลาดการล็อกอิน
        }
        setLoading(false); // ตั้งค่า loading เป็น false เมื่อล็อกอินเสร็จสิ้น
    };

    return (
        <div>
            <br /><br /><br />
            <div className="formlogin-container">
                <h2>Login</h2>
                <form onSubmit={handleSubmit}>
                    <div>
                        <label htmlFor="email">Email:</label><br />
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={handleEmailChange}
                            disabled={loading}
                        />
                    </div>
                    <div>
                        <label htmlFor="password">Password:</label><br />
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={handlePasswordChange}
                            disabled={loading}
                        />
                    </div>
                    <button type="submit" disabled={loading}>
                        {loading ? 'Logging in...' : 'Login'}
                    </button>
                </form>
                <p>Don't have an account? <Link to="/register">Register</Link></p>
            </div>
        </div>
    );
};

export default Login; // ส่งออกคอมโพเนนต์ Login เพื่อใช้งานในส่วนอื่นๆ ของแอป
