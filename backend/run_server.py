"""
Script to run the backend server with dummy data loaded
"""
import json
import os

# Load dummy data first
dummy_path = os.path.join(os.path.dirname(__file__), 'dummy_patients.json')
if os.path.exists(dummy_path):
    with open(dummy_path, 'r', encoding='utf-8') as f:
        patients_data = json.load(f)
    print(f"Loaded {len(patients_data)} dummy patient records")
else:
    patients_data = []
    print("No dummy data found")

# Set environment variable with patient data
import os
os.environ['DUMMY_PATIENTS'] = json.dumps(patients_data)

# Now run uvicorn
import uvicorn
uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
