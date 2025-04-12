from flask import Flask, Response, jsonify, send_from_directory
from flask import request
from flask_cors import CORS
import cv2
import numpy as np
from datetime import datetime
import random
from collections import deque
import threading
import time

app = Flask(__name__, static_folder='.')
CORS(app)

class TrafficSystem:
    def __init__(self):
        self.traffic_data = {
            'junction1': {
                'density': 'Medium',
                'signal': 'yellow',
                'wait_time': '45 seconds',
                'vehicles': 23,
                'location': [51.505, -0.09]
            },
            'junction2': {
                'density': 'Low',
                'signal': 'red',
                'wait_time': '30 seconds',
                'vehicles': 15,
                'location': [51.507, -0.1]
            }
        }
        self.violations = deque(maxlen=10)
        self.camera = None
        self.initialize_camera()
        self.start_violation_detection()

    def initialize_camera(self):
        try:
            self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not self.camera.isOpened():
                print("Warning: Could not open camera")
                self.camera = None
            else:
                self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        except Exception as e:
            print(f"Camera initialization error: {e}")
            self.camera = None

    def get_frame(self):
        if self.camera is None or not self.camera.isOpened():
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, 'Camera Not Available', (160, 240),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            return frame
        
        ret, frame = self.camera.read()
        if not ret:
            return np.zeros((480, 640, 3), dtype=np.uint8)
        return frame

    def start_violation_detection(self):
        def detect():
            while True:
                if random.random() < 0.3:
                    violation = {
                        'type': random.choice(['Speed', 'Red Light', 'Wrong Way']),
                        'location': random.choice(['Junction 1', 'Junction 2']),
                        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    self.violations.append(violation)
                time.sleep(10)

        thread = threading.Thread(target=detect, daemon=True)
        thread.start()

traffic_system = TrafficSystem()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            frame = traffic_system.get_frame()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)

    return Response(generate(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/update_traffic', methods=['POST'])
def update_traffic():
    try:
        for junction in traffic_system.traffic_data:
            traffic_system.traffic_data[junction]['vehicles'] = random.randint(10, 100)
            vehicles = traffic_system.traffic_data[junction]['vehicles']
            
            if vehicles > 70:
                density = 'High'
                signal = 'green'
                wait_time = '90 seconds'
            elif vehicles > 40:
                density = 'Medium'
                signal = 'yellow'
                wait_time = '45 seconds'
            else:
                density = 'Low'
                signal = 'red'
                wait_time = '30 seconds'
            
            traffic_system.traffic_data[junction].update({
                'density': density,
                'signal': signal,
                'wait_time': wait_time
            })

        return jsonify({
            'status': 'success',
            'junction1': traffic_system.traffic_data['junction1'],
            'junction2': traffic_system.traffic_data['junction2']
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/optimize_signals', methods=['POST'])
def optimize_signals():
    try:
        for junction in traffic_system.traffic_data:
            traffic_system.traffic_data[junction]['signal'] = 'green'
            traffic_system.traffic_data[junction]['wait_time'] = '60 seconds'

        return jsonify({
            'status': 'success',
            'junction1': traffic_system.traffic_data['junction1'],
            'junction2': traffic_system.traffic_data['junction2']
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/emergency_override', methods=['POST'])
def emergency_override():
    try:
        for junction in traffic_system.traffic_data:
            traffic_system.traffic_data[junction]['signal'] = 'green'
            traffic_system.traffic_data[junction]['wait_time'] = '0 seconds'

        return jsonify({
            'status': 'success',
            'junction1': traffic_system.traffic_data['junction1'],
            'junction2': traffic_system.traffic_data['junction2']
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/violations')
def get_violations():
    return jsonify({
        'status': 'success',
        'violations': list(traffic_system.violations)
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower()
        
        # Simple response logic
        if 'traffic' in user_message and 'status' in user_message:
            response = "The current traffic status is being monitored. You can check the real-time status on the dashboard."
        elif 'emergency' in user_message:
            response = "For emergencies, use the Emergency Override button. This will set all signals to green."
        elif 'violation' in user_message:
            response = "Traffic violations are monitored in real-time. Check the violations panel for recent incidents."
        elif 'help' in user_message:
            response = "I can help you with:\n- Traffic status\n- Emergency procedures\n- Violations\n- Signal optimization"
        else:
            response = "I understand you're asking about traffic management. Could you be more specific? You can ask about traffic status, violations, or emergency procedures."

        return jsonify({
            'status': 'success',
            'response': response
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)