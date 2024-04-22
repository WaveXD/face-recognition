import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAuth, signOut } from "firebase/auth";
import { getFirestore, collection, getDocs, deleteDoc, doc, getDoc } from 'firebase/firestore';
import { getStorage, ref, deleteObject } from 'firebase/storage';
import './admin-dashboard.css'; // Ensure CSS file path is correct

const AdminDashboard = () => {
    const logoStyle = {
        width: '50px',
        height: '50px',
        marginRight: '10px',
        filter: 'invert(1)', // Make the logo white
        verticalAlign: 'middle', // Align vertically to the middle
    };
    const navigate = useNavigate();
    const auth = getAuth();
    const firestore = getFirestore();
    const storage = getStorage();
    const [users, setUsers] = useState([]);

    useEffect(() => {
        const fetchUsers = async () => {
            const usersCollection = collection(firestore, "users");
            const userData = await getDocs(usersCollection);
            setUsers(userData.docs.map(doc => ({ ...doc.data(), id: doc.id })));
        };

        fetchUsers();
    }, [firestore]);

    const handleLogout = () => {
        signOut(auth).then(() => {
            localStorage.clear(); // เก็บสถานะล็อกอินไว้ใน localStorage
            navigate('/login');
        }).catch((error) => {
            console.error('Logout Error:', error);
        });
    };

    const handleDeleteUser = async (userId) => {
        const userRef = doc(firestore, "users", userId);
        try {
            const userData = await getDoc(userRef);
            if (!userData.exists()) {
                throw new Error('User does not exist');
            }
            const user = userData.data();
            if (!user.fileName) {
                throw new Error('File name is undefined');
            }
            const imageRef = ref(storage, `Users/${user.fileName}`);

            await deleteObject(imageRef); // Delete the image from Firebase Storage
            await deleteDoc(userRef); // Delete the user document from Firestore
            setUsers(users.filter(user => user.id !== userId)); // Update local state
            alert("User and image deleted successfully!");
        } catch (error) {
            console.error("Error deleting user:", error);
            alert(`Failed to delete user. ${error.message}`);
        }
    };

    return (
        <div className="admin-dashboard">
            <div className="navbar">
                <div className="logo-and-title">
                    <img src="/face-logo.png" alt="Face Logo" style={logoStyle} />
                    <span className="navbar-title">Face Recognition</span>
                </div>
                <div className="navbar-items">
                    <button onClick={() => navigate('/admin-history')} className="nav-button">Admin History Management</button>
                    <button onClick={handleLogout} className="logout-button">Logout</button>
                </div>
            </div>
            <main>
                <br/><center><h1>Admin Users Management</h1></center>
                <center><div className="user-list" style={{ padding: 20, width:210 }}>
                    {users.map(user => (
                        <div key={user.id} className="user-item">
                            <img src={user.photoURL} alt={user.name} style={{ width: 50, height: 50, borderRadius: '50%' }} />
                            <div className="user-info">
                                <span>{user.name}</span>
                                <button onClick={() => handleDeleteUser(user.id)}>Delete</button>
                            </div>
                        </div>
                    ))}
                </div></center>
            </main>
        </div>
    );
};

export default AdminDashboard;