"""
Generate Dummy Patient Dataset for Autism Stress Detection
"""
import json
from datetime import datetime, timedelta
import random

def generate_dummy_patients(n=20):
    """Generate dummy patient records"""
    
    names = [
        "Ahmad Rizki", "Siti Nurhaliza", "Budi Santoso", "Dewi Lestari",
        "Muhammad Fikri", "Ayu Pertiwi", "Andi Wijaya", "Rina Kusuma",
        "Doni Pratama", "Eka Putri", "Farhan Abdullah", "Gita Permata",
        "Hendra Gunawan", "Indah Sari", "Joko Susilo", "Kartika Dewi",
        "Lukman Hakim", "Maya Anggraini", "Nanda Saputra", "Olivia Zalianty"
    ]
    
    patients = []
    
    for i in range(n):
        age = random.randint(3, 25)
        gender = random.choice([0, 1])
        
        # Behavioral features
        a1 = random.randint(1, 3)
        a2 = random.randint(1, 3)
        a3 = random.randint(1, 3)
        a4 = random.randint(1, 3)
        a5 = random.randint(1, 3)
        a6 = random.randint(1, 3)
        a7 = random.randint(1, 3)
        a8 = random.randint(1, 3)
        a9 = random.randint(1, 3)
        a10 = random.randint(1, 3)
        
        # Physiological features
        heart_rate = random.randint(60, 140)
        sleep_quality = round(random.uniform(1, 10), 1)
        activity_level = round(random.uniform(1, 10), 1)
        
        # Psychological features
        anxiety_level = round(random.uniform(1, 10), 1)
        mood_score = round(random.uniform(1, 10), 1)
        social_engagement = round(random.uniform(1, 10), 1)
        
        family_history_asd = random.choice([0, 1])
        
        # Calculate stress score (same formula as backend)
        stress_score = (
            (a1 + a2 + a4) * 2 +
            (anxiety_level * 1.5) +
            (10 - sleep_quality) * 1.2 +
            (10 - social_engagement) * 1.3 +
            (heart_rate - 80) * 0.1 +
            family_history_asd * 5
        )
        
        # Normalize to 0-100
        stress_score = max(0, min(100, stress_score))
        
        # Determine stress level
        if stress_score <= 33:
            stress_level = 0
            stress_label = "Low"
            confidence = round(random.uniform(0.75, 0.95), 4)
        elif stress_score <= 66:
            stress_level = 1
            stress_label = "Medium"
            confidence = round(random.uniform(0.70, 0.90), 4)
        else:
            stress_level = 2
            stress_label = "High"
            confidence = round(random.uniform(0.75, 0.95), 4)
        
        # Recommendations based on stress level
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
        
        timestamp = datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        
        patient = {
            "id": i + 1,
            "timestamp": timestamp.isoformat(),
            "patient_name": names[i] if i < len(names) else f"Patient {i+1}",
            "input_data": {
                "patient_name": names[i] if i < len(names) else f"Patient {i+1}",
                "age": age,
                "gender": gender,
                "A1": a1, "A2": a2, "A3": a3, "A4": a4, "A5": a5,
                "A6": a6, "A7": a7, "A8": a8, "A9": a9, "A10": a10,
                "heart_rate": heart_rate,
                "sleep_quality": sleep_quality,
                "activity_level": activity_level,
                "anxiety_level": anxiety_level,
                "mood_score": mood_score,
                "social_engagement": social_engagement,
                "family_history_asd": family_history_asd
            },
            "prediction": {
                "stress_level": stress_level,
                "stress_level_label": stress_label,
                "stress_score": round(stress_score, 1),
                "confidence": confidence,
                "recommendations": recommendations[stress_level],
                "patient_id": i + 1
            }
        }
        
        patients.append(patient)
    
    return patients

if __name__ == "__main__":
    patients = generate_dummy_patients(20)
    
    # Save to JSON file
    with open('dummy_patients.json', 'w', encoding='utf-8') as f:
        json.dump(patients, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {len(patients)} dummy patient records")
    print("Saved to dummy_patients.json")
    
    # Print summary
    stress_dist = {0: 0, 1: 0, 2: 0}
    for p in patients:
        stress_dist[p['prediction']['stress_level']] += 1
    
    print("\nStress Distribution:")
    print(f"  Low: {stress_dist[0]}")
    print(f"  Medium: {stress_dist[1]}")
    print(f"  High: {stress_dist[2]}")
