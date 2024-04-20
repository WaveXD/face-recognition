import React, { useEffect, useState } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import { getStorage, ref, listAll, getDownloadURL } from 'firebase/storage';
import Navbar from './Navbar';
import firebaseApp from '../firebase';
import '../styles/History.css';

const localizer = momentLocalizer(moment);

function History() {
  const [folders, setFolders] = useState([]);
  const [selectedFolder, setSelectedFolder] = useState(null);
  const [images, setImages] = useState([]);
  const [events, setEvents] = useState([]);
  const [selectedDate, setSelectedDate] = useState(new Date());

  const parseFilename = (filename) => {
    const parts = filename.replace('.jpg', '').split('_');
    const user = parts[0];
    const date = parts[1];
    const time = parts[2].replace(/-/g, ':'); // Time format might be like '114211PM' which needs to be converted to '11:42:11 PM'
    const timestamp = new Date(`${date}T${time}`);
    return { user, timestamp };
  };

  const listFolders = async () => {
    const storage = getStorage(firebaseApp);
    const rootRef = ref(storage, ''); // Adjust if your structure has a different root

    listAll(rootRef).then((res) => {
      let folderNames = new Set();
      res.prefixes.forEach((folderRef) => {
        folderNames.add(folderRef.name);
      });
      setFolders([...folderNames]);
    }).catch((error) => {
      console.error("Error listing folders:", error);
    });
  };

  const fetchImages = async (folder) => {
    const storage = getStorage(firebaseApp);
    const folderRef = ref(storage, folder);

    listAll(folderRef).then(async (res) => {
      const imagesData = await Promise.all(
        res.items.map((itemRef) => {
          return getDownloadURL(itemRef).then((url) => {
            const { user, timestamp } = parseFilename(itemRef.name);
            return { url, user, timestamp, start: timestamp, end: timestamp, title: user };
          });
        })
      );
      setImages(imagesData);
      setEvents(imagesData.filter(Boolean)); // Create calendar events
    }).catch((error) => {
      console.error("Error fetching images:", error);
    });
  };

  useEffect(() => {
    listFolders();
  }, []);

  useEffect(() => {
    if (selectedFolder) {
      fetchImages(selectedFolder);
    }
  }, [selectedFolder]);

  return (
    <div>
      <Navbar />
      <div className="history-container">
        <center><h1>History</h1></center>
        <Calendar
          localizer={localizer}
          events={events}
          startAccessor="start"
          endAccessor="end"
          style={{ height: 500 }}
          onSelectEvent={event => setSelectedDate(event.start)}
          onNavigate={date => setSelectedDate(date)}
        /><br/>
        <div className="folders-list">
          {folders.map((folder, index) => {
            if (folder !== "Users") {
              return <button key={index} onClick={() => setSelectedFolder(folder)}>{folder}</button>;
            }
            return null;
          })}
        </div>
        <div className="images-grid">
          {images.filter(img => moment(img.timestamp).isSame(selectedDate, 'day')).map((image, index) => (
            <div key={index} className="image-container">
              <img src={image.url} alt={`Captured by ${image.user}`} />
              <div className="image-info">
                <p className="timestamp">{image.user} : {moment(image.timestamp).format('L, LTS')}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default History;