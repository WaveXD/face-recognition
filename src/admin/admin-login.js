import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { signInWithEmailAndPassword, getAuth } from "firebase/auth";
import '../styles/login.css';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    const auth = getAuth();

    useEffect(() => {
        if (auth.currentUser) {
            // Redirect users directly if they are already logged in
            navigate('/admin-dashboard');
        }
    }, [navigate, auth]);

    const handleEmailChange = (event) => setEmail(event.target.value);
    const handlePasswordChange = (event) => setPassword(event.target.value);

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);

        if (email !== 'admin@test.com') {
            alert('Access Denied: Only admin@test.com is allowed to login here.');
            setLoading(false);
            return;
        }

        try {
            const userCredential = await signInWithEmailAndPassword(auth, email, password);
            // Directly set local storage and navigate if the correct admin email is used
            localStorage.setItem('isLoggedIn', 'true');
            localStorage.setItem('isAdmin', 'true'); // Additional flag to indicate admin privileges
            navigate('/admin-dashboard');
        } catch (error) {
            console.error('Error logging in:', error);
            alert('Error logging in: ' + error.message);
            setLoading(false);
        }
    };

    return (
        <div>
            <br /><br /><br />
            <div className="formlogin-container">
                <h2>Admin Login</h2>
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
                <p>Don't have an admin account? <Link to="/login">Login as user</Link></p>
            </div>
        </div>
    );
};

export default Login;
