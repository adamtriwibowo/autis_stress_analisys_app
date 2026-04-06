"""
Simple HTTP Server untuk test backend tanpa uvicorn
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import joblib
import numpy as np
from datetime import datetime
import os

# Load model dan data
print("Loading model and data...")
model = joblib.load('stress_model.pkl')
scaler = joblib.load('scaler.pkl')
feature_columns = joblib.load('feature_columns.pkl')

with open('dummy_patients.json', 'r', encoding='utf-8') as f:
    patients_db = json.load(f)

print(f"✓ Model loaded")
print(f"✓ {len(patients_db)} patients loaded")

def get_recommendations(stress_level):
    recommendations = {
        0: ["Pertahankan rutinitas harian", "Monitor perilaku berkala"],
        1: ["Konsultasikan dengan terapis", "Tingkatkan kualitas tidur"],
        2: ["Segera konsultasikan profesional", "Evaluasi lingkungan"]
    }
    return recommendations.get(stress_level, [])

class MyHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        if self.path == '/health':
            response = {'status': 'healthy', 'model_loaded': True, 'patients_count': len(patients_db)}
        elif self.path == '/patients':
            response = patients_db
        elif self.path == '/statistics':
            stress_levels = [p['prediction']['stress_level_label'] for p in patients_db]
            response = {
                'total_patients': len(patients_db),
                'stress_distribution': {
                    'Low': stress_levels.count('Low'),
                    'Medium': stress_levels.count('Medium'),
                    'High': stress_levels.count('High')
                },
                'average_confidence': 0.85
            }
        else:
            response = {'message': 'Autism Stress Detection API', 'version': '1.0.0'}
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        if self.path == '/predict':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            # Extract features
            X = np.array([[data[col] for col in feature_columns]])
            X_scaled = scaler.transform(X)
            
            prediction = int(model.predict(X_scaled)[0])
            probabilities = model.predict_proba(X_scaled)[0]
            stress_score = float(np.sum(probabilities * [0, 50, 100]))
            
            # Override prediction based on explicit threshold rules
            # Low: 0-33, Medium: 34-66, High: 67-100
            if stress_score <= 33:
                prediction = 0  # Low
            elif stress_score <= 66:
                prediction = 1  # Medium
            else:
                prediction = 2  # High
            
            confidence = float(np.max(probabilities))
            
            response = {
                'stress_level': prediction,
                'stress_level_label': ['Low', 'Medium', 'High'][prediction],
                'stress_score': stress_score,
                'confidence': confidence,
                'recommendations': get_recommendations(prediction)
            }
            
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
            # Save to patients
            new_patient = {
                'id': len(patients_db) + 1,
                'timestamp': datetime.now().isoformat(),
                'patient_name': data.get('patient_name', ''),
                'input_data': data,
                'prediction': response
            }
            patients_db.append(new_patient)
            print(f"✓ New prediction saved: ID {new_patient['id']}")
        
        elif self.path == '/save-patient':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            response = {'message': 'Saved', 'patient_id': len(patients_db) + 1}
            
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 8000), MyHandler)
    print("\n" + "="*50)
    print("  BACKEND SERVER RUNNING")
    print("="*50)
    print(f"  URL: http://127.0.0.1:8000")
    print(f"  API Docs: http://127.0.0.1:8000/docs (not available)")
    print(f"  Health: http://127.0.0.1:8000/health")
    print("="*50)
    print("\nPress Ctrl+C to stop\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        server.shutdown()
