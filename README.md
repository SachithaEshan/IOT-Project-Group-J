# Driver Drowsiness Monitoring System (DMS)

## Overview
The **Driver Drowsiness Monitoring System (DMS)** is an **IoT-based solution** designed to enhance road safety by detecting driver drowsiness in **real-time**. The system integrates **ESP32**, **ESP32-CAM**, and **GPS-NEO-6M** modules with cloud platforms like **Firebase** and **ThingSpeak** for data storage and visualization.  

It captures **driver face images** and **vehicle location** to detect drowsiness and provides real-time monitoring through a **web dashboard**.  

> 📌 This project was completed as part of the **PUSL2022 - Introduction to IoT** module at the **University of Plymouth**.

---

## Key Components

### **Hardware**
- **ESP32 Microcontroller** – Central control unit for coordinating modules.
- **ESP32-CAM Module** – Captures driver face images for drowsiness detection.
- **GPS-NEO-6M Module** – Tracks vehicle **location** and **speed**.

### **Software**
- **Firebase Realtime Database** – Logs vehicle data and drowsiness events.
- **ThingSpeak** – Cloud platform for real-time data visualization.
- **Web Interface** – Dashboard for visualizing real-time data.

---

## System Architecture

### **Data Flow**
1. **Sensors capture data** (GPS, Camera) via the **ESP32**.
2. **Drowsiness detection** is performed locally on the **ESP32-CAM** images.
3. Data is logged to **Firebase** and visualized in **ThingSpeak**.

### **Database Design**
#### **Schema**
- **drowsiness_events** (Stores event details)
  - `latitude` – Vehicle’s latitude.
  - `longitude` – Vehicle’s longitude.
  - `speed` – Vehicle’s speed.
  - `timestamp` – Event time.

---

## **Deployment**
- **Hybrid Hosting:** Uses **on-premises servers** + **cloud services (Firebase, ThingSpeak)** for real-time data storage & visualization.
- **Infrastructure:** Includes **servers, virtualization** for resource optimization & seamless networking.

---

## **Testing**
- ✅ **Unit Testing** – Validates individual components (**ESP32, sensors, backend**).  
- ✅ **Integration Testing** – Verifies interactions between **hardware, cloud services, and dashboard**.  
- ✅ **System Testing** – Ensures **end-to-end functionality**.

---

## **Dependencies**
### **Libraries**
- **OpenCV, dlib** – Facial detection & drowsiness monitoring.
- **Firebase Admin SDK, ThingSpeak API** – Cloud interaction.
- **Arduino libraries** – Wi-Fi, HTTPClient, and sensor control.

### **External Files**
- **Model files**
- **Alarm sounds**
- **HTML for the dashboard**
- **Firebase credentials**

---

## **Communication Protocols**
- **Wi-Fi & HTTP** – Enables communication between hardware & cloud.  
- **Real-time Data Streaming** – Streams sensor data for immediate action.  

---

## **Contributors**
- **Sinel Nemsara**
- **Thejan Rajapaksha**
- **Yohan Nanayakkara**
- **Sachitha Eshan**
- **Charith Bandara**
- **Devin Fernando**

---

## **Conclusion**
The **Driver Drowsiness Monitoring System (DMS)** effectively integrates **hardware and cloud technologies** to:
✔ Monitor driver behavior  
✔ Detect drowsiness in real-time  
✔ Improve road safety through **real-time monitoring & data visualization**  

🚀 **This project showcases the power of IoT in enhancing road safety!**
