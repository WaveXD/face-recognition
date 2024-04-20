// firebase.js

import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "AIzaSyCmtbAz4yMUCoEHtkY_FToLbKV4p67CtUs",
  authDomain: "database-8b747.firebaseapp.com",
  databaseURL: "https://database-8b747-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "database-8b747",
  storageBucket: "database-8b747.appspot.com",
  messagingSenderId: "189847911941",
  appId: "1:189847911941:web:3aacac3e0a0ecb1b76266c",
  measurementId: "G-KVMQ2TKVLX"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth();
export default app;