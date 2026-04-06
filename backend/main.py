"""
FastAPI Backend for Autism Stress Detection System
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import joblib
import numpy as np
import json
import os
from datetime import datetime

# Load dummy data FIRST before anything else
patients_db = []
dummy_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dummy_patients.json')
if os.path.exists(dummy_path):
    try:
        with open(dummy_path, 'r', encoding='utf-8') as f:
            patients_db = json.load(f)
        print(f"✓ Loaded {len(patients_db)} patient records from dummy_patients.json")
    except Exception as e:
        print(f"✗ Error loading dummy data: {e}")
        patients_db = []
else:
    print(f"✗ Dummy data not found at: {dummy_path}")
    patients_db = []

app = FastAPI(
    title="Autism Stress Detection API",
    description="API untuk prediksi tingkat stres pada pasien autisme",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
try:
    model = joblib.load('stress_model.pkl')
    scaler = joblib.load('scaler.pkl')
    feature_columns = joblib.load('feature_columns.pkl')
    print("✓ Model loaded successfully!")
except Exception as e:
    model = None
    scaler = None
    feature_columns = None
    print(f"✗ Model not found: {e}")

# Pydantic models
class PatientInput(BaseModel):
    age: int
    gender: int
    A1: int
    A2: int
    A3: int
    A4: int
    A5: int
    A6: int
    A7: int
    A8: int
    A9: int
    A10: int
    heart_rate: int
    sleep_quality: float
    activity_level: float
    anxiety_level: float
    mood_score: float
    social_engagement: float
    family_history_asd: int
    patient_name: Optional[str] = None

class PredictionResponse(BaseModel):
    stress_level: int
    stress_level_label: str
    stress_score: float
    confidence: float
    recommendations: List[str]
    patient_id: Optional[int] = None

def get_recommendations(stress_level: int) -> List[str]:
    """Generate recommendations based on stress level"""
    recommendations = {
        0: [
            "Pertahankan rutinitas harian yang konsisten",
            "Lanjutkan aktivitas sosial yang positif",
            "Monitor perubahan perilaku secara berkala",
            "Berikan reinforcement positif"
        ],
        1: [
            "Konsultasikan dengan terapis untuk strategi coping",
            "Tingkatkan kualitas tidur dengan rutinitas malam",
            "Kurangi stimulus sensorik yang berlebihan",
            "Latihan relaksasi dan pernapasan",
            "Monitor pemicu stres harian"
        ],
        2: [
            "Segera konsultasikan dengan profesional kesehatan mental",
            "Evaluasi lingkungan untuk mengurangi stresor",
            "Implementasikan intervensi behavioral intensif",
            "Pertimbangkan terapi okupasi",
            "Monitor tanda-tanda meltdown",
            "Pastikan dukungan keluarga yang memadai"
        ]
    }
    return recommendations.get(stress_level, [])

@app.get("/")
def read_root():
    return {
        "message": "Autism Stress Detection API",
        "version": "1.0.0",
        "status": "running",
        "patients_loaded": len(patients_db)
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "patients_count": len(patients_db)
    }

@app.post("/predict", response_model=PredictionResponse)
def predict_stress(patient_input: PatientInput):
    """Predict stress level based on patient input"""
    if model is None or scaler is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please train the model first."
        )

    input_data = {
        'age': patient_input.age,
        'gender': patient_input.gender,
        'A1': patient_input.A1,
        'A2': patient_input.A2,
        'A3': patient_input.A3,
        'A4': patient_input.A4,
        'A5': patient_input.A5,
        'A6': patient_input.A6,
        'A7': patient_input.A7,
        'A8': patient_input.A8,
        'A9': patient_input.A9,
        'A10': patient_input.A10,
        'heart_rate': patient_input.heart_rate,
        'sleep_quality': patient_input.sleep_quality,
        'activity_level': patient_input.activity_level,
        'anxiety_level': patient_input.anxiety_level,
        'mood_score': patient_input.mood_score,
        'social_engagement': patient_input.social_engagement,
        'family_history_asd': patient_input.family_history_asd
    }

    X = np.array([[input_data[col] for col in feature_columns]])
    X_scaled = scaler.transform(X)

    prediction = int(model.predict(X_scaled)[0])
    probabilities = model.predict_proba(X_scaled)[0]

    # Calculate stress score from model probabilities
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
    recommendations = get_recommendations(prediction)

    stress_labels = {0: "Low", 1: "Medium", 2: "High"}

    return PredictionResponse(
        stress_level=prediction,
        stress_level_label=stress_labels.get(prediction, "Unknown"),
        stress_score=stress_score,
        confidence=confidence,
        recommendations=recommendations
    )

@app.post("/save-patient", response_model=dict)
def save_patient_record(patient_input: PatientInput, prediction: PredictionResponse):
    """Save patient record to database"""
    record = {
        'id': len(patients_db) + 1,
        'timestamp': datetime.now().isoformat(),
        'patient_name': patient_input.patient_name,
        'input_data': patient_input.model_dump(),
        'prediction': prediction.model_dump()
    }

    patients_db.append(record)

    return {
        "message": "Patient record saved successfully",
        "patient_id": record['id']
    }

@app.get("/patients", response_model=List[dict])
def get_all_patients():
    """Get all patient records"""
    return patients_db

@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    """Get specific patient record"""
    for patient in patients_db:
        if patient['id'] == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/statistics")
def get_statistics():
    """Get overall statistics"""
    if not patients_db:
        return {
            "total_patients": 0,
            "stress_distribution": {"Low": 0, "Medium": 0, "High": 0}
        }

    stress_levels = [p['prediction']['stress_level_label'] for p in patients_db]
    confidences = [p['prediction']['confidence'] for p in patients_db]
    avg_confidence = float(np.mean(confidences)) if confidences else 0.0

    return {
        "total_patients": len(patients_db),
        "stress_distribution": {
            "Low": stress_levels.count("Low"),
            "Medium": stress_levels.count("Medium"),
            "High": stress_levels.count("High")
        },
        "average_confidence": avg_confidence
    }

if __name__ == "__main__":
    import uvicorn
    print(f"\n🚀 Starting server with {len(patients_db)} patient records")
    print(f"📍 API Docs: http://localhost:8000/docs")
    print(f"🏥 Health Check: http://localhost:8000/health\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
