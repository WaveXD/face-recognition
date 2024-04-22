import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAuth, signOut } from "firebase/auth";
import { getStorage, ref, listAll, getDownloadURL, deleteObject } from 'firebase/storage';
import firebaseApp from '../firebase';
import './admin-history.css';

function AdminHistory() {
  const logoStyle = {
    width: '50px',
    height: '50px',
    marginRight: '10px',
    filter: 'invert(1)', // Make the logo white
    verticalAlign: 'middle', // Align vertically to the middle
  };
  const [folders, setFolders] = useState([]);
  const [selectedFolder, setSelectedFolder] = useState(null);
  const [images, setImages] = useState([]);
  const navigate = useNavigate();
  const auth = getAuth();

  useEffect(() => {
    listFolders();
  }, []);

  const listFolders = async () => {
    const storage = getStorage(firebaseApp);
    const rootRef = ref(storage, '');
    listAll(rootRef).then((res) => {
      let folderNames = new Set();
      res.prefixes.forEach((folderRef) => {
        if (folderRef.name !== "Users") {
          folderNames.add(folderRef.name);
        }
      });
      setFolders([...folderNames]);
    }).catch((error) => {
      console.error("Error listing folders:", error);
    });
  };

  const fetchImages = async (folder) => {
    setSelectedFolder(folder);
    const storage = getStorage(firebaseApp);
    const folderRef = ref(storage, folder);
    listAll(folderRef).then(async (res) => {
      const imagesData = await Promise.all(
        res.items.map((itemRef) => {
          return getDownloadURL(itemRef).then((url) => {
            const updated = new Date(itemRef.updated);
            let nameWithoutExtension = itemRef.name.replace(/\.jpg$/, ''); // Remove .jpg from the filename
            let displayText = nameWithoutExtension; // Use the name without .jpg as the default display text
            if (!isNaN(updated.getTime())) {
              const dateStr = `${updated.toLocaleDateString('en-US', {
                month: '2-digit',
                day: '2-digit',
                year: 'numeric'
              })}, ${updated.toLocaleTimeString('en-US', {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: true
              })}`;
              displayText = `${nameWithoutExtension} - wave : ${dateStr}`;
            }
            return { url, name: displayText, fullPath: itemRef.fullPath };
          });
        })
      );
      setImages(imagesData);
    }).catch((error) => {
      console.error("Error fetching images:", error);
    });
  };


  const deleteImage = async (fullPath) => {
    const storage = getStorage(firebaseApp);
    const imageRef = ref(storage, fullPath);
    deleteObject(imageRef).then(() => {
      setImages(images.filter(image => image.fullPath !== fullPath));
      alert("Image deleted successfully!");
    }).catch((error) => {
      console.error("Error deleting image:", error);
      alert("Failed to delete image.");
    });
  };

  const deleteAllImagesInFolder = async () => {
    if (selectedFolder) {
      const storage = getStorage(firebaseApp);
      const folderRef = ref(storage, selectedFolder);
      listAll(folderRef).then(async (res) => {
        Promise.all(res.items.map(itemRef => deleteObject(itemRef))).then(() => {
          alert(`All images in ${selectedFolder} deleted successfully!`);
          setImages([]);
        }).catch(error => {
          console.error("Error deleting all images in folder:", error);
          alert("Failed to delete images.");
        });
      });
    } else {
      alert("No folder selected!");
    }
  };

  const handleLogout = () => {
    signOut(auth).then(() => {
      localStorage.clear(); // เก็บสถานะล็อกอินไว้ใน localStorage
      navigate('/login');
    }).catch((error) => {
      console.error('Logout Error:', error);
    });
  };

  return (
    <div className="admin-history">
      <div className="navbar">
        <div className="logo-and-title">
          <img src="/face-logo.png" alt="Face Logo" style={logoStyle} />
          <span className="navbar-title">Face Recognition</span>
        </div>
        <div className="navbar-items">
          <button onClick={() => navigate('/admin-dashboard')} className="nav-button">Admin Users Management</button>
          <button onClick={handleLogout} className="logout-button">Logout</button>
        </div>
      </div>
      <div className="history-container">
        <center><h1>Admin History Management</h1></center>
        <div className="folders-list">
          {folders.map((folder, index) => (
            <button key={index} onClick={() => fetchImages(folder)}>{folder}</button>
          ))}
        </div>
        {selectedFolder && (
          <button onClick={deleteAllImagesInFolder}>Delete All Images in Folder</button>
        )}
        <center><div className="images-grid">
          {images.map((image, index) => (
            <div key={index} className="image-container">
              <img src={image.url} alt={image.name} style={{ width: '100px', height: '100px' }} /><br/>
              <p>{image.name}</p>
              <button onClick={() => deleteImage(image.fullPath)}>Delete</button>
            </div>
          ))}
        </div></center>
      </div>
    </div>
  );
}

export default AdminHistory;
