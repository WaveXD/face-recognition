import React, { useState } from 'react';

const Main = () => {
  const [cameraUrl, setCameraUrl] = useState('https://localhost:5000/video_feed');  // กำหนด state สำหรับจัดเก็บ URL ของการถ่ายทอดสดจากกล้อง

  const mainStyle = {
    textAlign: 'center',
    padding: '20px',
  };

  const liveStreamStyle = {
    fontSize: '24px',
    fontWeight: 'bold',
    margin: '20px 0',
  };

  const videoContainerStyle = {
    maxWidth: '320px',
    margin: '0 auto',
    overflow: 'hidden',
  };

  const videoStyle = {
    width: '320px', 
    height: 'auto', 
    objectFit: 'contain' 
  };

  const iconStyle = {
    cursor: 'pointer',
    margin: '0 10px',
    fontSize: '20px',
  };

  const handleCameraChange = (cameraNumber) => { // กำหนดฟังก์ชันสำหรับเปลี่ยนกล้อง
    switch (cameraNumber) {
      case 1:
        setCameraUrl('http://database-8b747.web.app/video_feed'); // กำหนด URL สำหรับกล้องที่ 1
        break;
      case 2:
        setCameraUrl('http://database-8b747.web.app/video_feed2'); // กำหนด URL สำหรับกล้องที่ 2
        break;
      default:
        setCameraUrl('http://database-8b747.web.app/video_feed'); // กำหนด URL ค่าเริ่มต้น
    }
  };

  return (
    <main style={mainStyle}>
      <div>
        <div style={liveStreamStyle}>
          Live Streaming <br/>
          <img src="http://192.168.1.64:80/Streaming/channels/102/httpPreview" alt="Camera Stream"></img>
          <span style={iconStyle} onClick={() => handleCameraChange(1)} role="img" aria-label="Camera 1">📷 1</span>
          <span style={iconStyle} onClick={() => handleCameraChange(2)} role="img" aria-label="Camera 2">📷 2</span>        
        </div>
        <div style={videoContainerStyle}>
          <img
            src={cameraUrl}
            alt="Live Camera Feed"
            style={videoStyle}
          />
        </div>
      </div>
    </main>
  );
}

export default Main;