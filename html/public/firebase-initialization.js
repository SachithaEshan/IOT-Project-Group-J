// firebase-initialization.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDsQ6BWZ_5t7fBQz7cx6VjSHownQujrlC0",
  authDomain: "iot-groupj.firebaseapp.com",
  databaseURL: "https://iot-groupj-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "iot-groupj",
  storageBucket: "iot-groupj.appspot.com",
  messagingSenderId: "95119028407",
  appId: "1:95119028407:web:9add91735de2e39326dd32",
  measurementId: "G-VTN7GPCLXJ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

export { app };
