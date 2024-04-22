import React, { useState } from 'react';
import { getFirestore, collection, addDoc } from 'firebase/firestore';
import { getStorage, ref, uploadBytes, getDownloadURL } from 'firebase/storage';
import app from '../firebase';
import Navbar from './Navbar';
import '../styles/Setup.css';

function Setup() {
  const [userName, setUserName] = useState('');
  const [file, setFile] = useState(null);
  const firestore = getFirestore(app);
  const storage = getStorage(app);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const addUser = async (userName, file) => {
    try {
      const storageRef = ref(storage, `Users/${file.name}`);
      const metadata = {
        contentType: file.type,
        customMetadata: {
          'processed': 'false',
        }
      };
      const snapshot = await uploadBytes(storageRef, file, metadata);
      const photoURL = await getDownloadURL(snapshot.ref);

      const docRef = await addDoc(collection(firestore, "users"), {
        name: userName,
        photoURL: photoURL,
        processed: false,
        fileName: file.name
      });

      console.log("User added with ID: ", docRef.id);
      alert('User added successfully! Processing will complete soon.');
    } catch (error) {
      console.error("Error adding user: ", error);
      alert('Failed to add user.');
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (file && userName) {
      addUser(userName, file);
    } else {
      alert("Missing userName or file");
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
