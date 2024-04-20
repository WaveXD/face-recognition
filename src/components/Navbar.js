import React from 'react';
import { FaHome, FaUser, FaSignOutAlt, FaCog } from 'react-icons/fa';

const Navbar = () => {
  const navbarStyle = {
    background: '#333',
    padding: '10px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    color: 'white',
  };

  const logoStyle = {
    width: '50px',
    height: '50px',
    marginRight: '10px',
    filter: 'invert(1)', // Make the logo white
    verticalAlign: 'middle', // Align vertically to the middle
  };

  const titleStyle = {
    textDecoration: 'none',
    color: 'white',
    fontSize: '24px',
    fontWeight: 'bold',
    verticalAlign: 'middle', // Align vertically to the middle
  };

  const linkStyle = {
    textDecoration: 'none',
    color: 'white',
    margin: '0 10px',
    fontSize: '18px',
  };

  return (
    <nav style={navbarStyle}>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <img src="/face-logo.png" alt="Logo" style={logoStyle} />
        <a href="/" style={titleStyle}>Face Recognition</a>
      </div>
      <div>
        <a href="/" style={linkStyle}><FaHome /> Home</a>
        <a href="/History" style={linkStyle}><FaUser /> History</a>
        <a href="/Setup" style={linkStyle}><FaCog /> Setup</a>
        <a href="/Logout" style={linkStyle}><FaSignOutAlt /> Logout</a>

      </div>
    </nav>
  );
}

export default Navbar;
