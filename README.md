# AI Traffic Monitoring System

An AI-based Traffic Monitoring and Management System using Flask for the backend and HTML, CSS, JavaScript for the frontend. This system simulates traffic flow, displays a live CCTV feed, provides traffic control actions, and detects violations (simulated). It also includes a basic chatbot interface.

---

## Project Structure

├── app.py # Flask backend for traffic logic, video stream, and API endpoints ├── index.html # Frontend dashboard with map, controls, video feed, and chatbot ├── yolov8n.pt # YOLOv8 model file (placeholder for future integration) └── README.md # Project documentation


---

## Features

- Real-time traffic status updates and visualization
- Simulated CCTV camera video feed using OpenCV
- Dynamic traffic signal control logic
- Emergency override functionality
- Signal optimization simulation
- Basic traffic violation detection (simulated)
- Interactive chatbot for assistance

---

## Backend (`app.py`)

### Key Functionalities

- **Traffic Data Simulation**: Maintains traffic status for multiple junctions.
- **Camera Feed**: Uses OpenCV to stream live video or a placeholder if no camera is detected.
- **Violation Detection**: Simulates violations periodically in a background thread.
- **REST Endpoints**:
  - `/`: Serves the frontend
  - `/video_feed`: Streams MJPEG video frames
  - `/update_traffic`: Updates traffic info with simulated values
  - `/optimize_signals`: Sets all signals to green with standard wait time
  - `/emergency_override`: Immediately turns all signals green
  - `/violations`: Returns recent simulated violations
  - `/chat`: Handles chatbot interactions

---

## Frontend (`index.html`)

### Key Components

- **Dashboard**:
  - Displays live signal status (density, signal color, wait time)
  - Updates every few seconds using JavaScript and fetch APIs

- **Map Integration**:
  - Uses Leaflet.js to display junction markers

- **Camera Feed**:
  - Shows real-time CCTV using the `/video_feed` endpoint

- **Violations Panel**:
  - Lists recent violations detected (simulated)

- **Chatbot**:
  - Interactive assistant responding to basic user queries about traffic

---

## Signal Control Logic

| Vehicles       | Density | Signal | Wait Time     |
|----------------|---------|--------|---------------|
| > 70           | High    | Green  | 90 seconds    |
| 41 – 70        | Medium  | Yellow | 45 seconds    |
| ≤ 40           | Low     | Red    | 30 seconds    |

---

## How to Run

1. **Install dependencies**:
   ```bash
   pip install flask flask-cors opencv-python numpy
2. **Run the application**:

   python app.py

3. **Open in browser**:
http://localhost:5000

### Notes
If no webcam is detected, a placeholder image will appear in the camera feed section.

Violations are generated randomly for demonstration purposes.

The yolov8n.pt model is included for potential future integration using YOLOv8 object detection.

### Future Scope
Integrate YOLOv8 for real-time detection (e.g., red-light jumps, vehicle tracking)

Use live data from traffic sensors or APIs

Store logs and violations in a database

Implement admin panel and user roles

