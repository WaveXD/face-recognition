import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Home from './components/home';
import History from './components/History';
import Setup from './components/Setup';
import Login from './components/Login';
import Register from './components/Register';
import Logout from './components/Logout';
import AdminLogin from './admin/admin-login'; // ตรวจสอบว่าไฟล์และเส้นทางการนำเข้านี้ถูกต้อง
import AdminDashboard from './admin/admin-dashboard';
import AdminHistory from './admin/admin-history';

function App() {
  // Initial check for existing logged in state in local storage
  const [isLoggedIn, setLoggedIn] = useState(localStorage.getItem('isLoggedIn') === 'true');

  useEffect(() => {
    // Update local storage when isLoggedIn changes
    localStorage.setItem('isLoggedIn', isLoggedIn);
  }, [isLoggedIn]);

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={<Login setLoggedIn={setLoggedIn} />} />
          <Route path="/" element={isLoggedIn ? <Home /> : <Navigate to="/login" />} />
          <Route path="/history" element={isLoggedIn ? <History /> : <Navigate to="/login" />} />
          <Route path="/setup" element={isLoggedIn ? <Setup /> : <Navigate to="/login" />} />
          <Route path="/register" element={<Register />} />
          <Route path="/logout" element={<Logout setLoggedIn={setLoggedIn} />} />
          <Route path="/admin-login" element={<AdminLogin />} />
          <Route path="/admin-dashboard" element={<AdminDashboard />} />
          <Route path="/admin-history" element={<AdminHistory />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
