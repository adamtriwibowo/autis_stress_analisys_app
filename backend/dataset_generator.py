"""
Dataset Generator for Autism Stress Detection
Based on Kaggle Autism and Stress Detection datasets
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import joblib
import os

np.random.seed(42)

def generate_autism_stress_dataset(n_samples=2000):
    """
    Generate synthetic dataset for autism stress detection
    Features based on Kaggle ASD and Stress Detection datasets
    """
    
    data = {
        # Demographic features
        'age': np.random.randint(3, 25, n_samples),
        'gender': np.random.choice([0, 1], n_samples),  # 0=Female, 1=Male
        
        # Behavioral features (A1-A10) - from ASD dataset
        'A1': np.random.randint(1, 4, n_samples),  # Social interaction
        'A2': np.random.randint(1, 4, n_samples),  # Eye contact
        'A3': np.random.randint(1, 4, n_samples),  # Communication
        'A4': np.random.randint(1, 4, n_samples),  # Repetitive behavior
        'A5': np.random.randint(1, 4, n_samples),  # Sensory sensitivity
        'A6': np.random.randint(1, 4, n_samples),  # Routine adherence
        'A7': np.random.randint(1, 4, n_samples),  # Social smile
        'A8': np.random.randint(1, 4, n_samples),  # Response to name
        'A9': np.random.randint(1, 4, n_samples),  # Object manipulation
        'A10': np.random.randint(1, 4, n_samples), # Emotional response
        
        # Physiological features - from Stress Detection dataset
        'heart_rate': np.random.randint(60, 140, n_samples),
        'sleep_quality': np.random.uniform(1, 10, n_samples),
        'activity_level': np.random.uniform(1, 10, n_samples),
        
        # Psychological features
        'anxiety_level': np.random.uniform(1, 10, n_samples),
        'mood_score': np.random.uniform(1, 10, n_samples),
        'social_engagement': np.random.uniform(1, 10, n_samples),
        
        # Family history
        'family_history_asd': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
    }
    
    df = pd.DataFrame(data)
    
    # Create stress level based on features (realistic correlation)
    stress_score = (
        (df['A1'] + df['A2'] + df['A4']) * 2 +  # Behavioral impact
        (df['anxiety_level'] * 1.5) +  # Psychological impact
        (10 - df['sleep_quality']) * 1.2 +  # Sleep impact
        (10 - df['social_engagement']) * 1.3 +  # Social impact
        (df['heart_rate'] - 80) * 0.1 +  # Physiological impact
        df['family_history_asd'] * 5  # Genetic factor
    )
    
    # Normalize stress score
    stress_score = (stress_score - stress_score.min()) / (stress_score.max() - stress_score.min()) * 100
    
    # Categorize stress level
    df['stress_level'] = pd.cut(
        stress_score,
        bins=[-np.inf, 33, 66, np.inf],
        labels=[0, 1, 2]  # 0=Low, 1=Medium, 2=High
    ).astype(int)
    
    df['stress_score'] = stress_score
    
    return df

def train_stress_model(df):
    """Train ML model for stress prediction"""
    
    feature_columns = [
        'age', 'gender', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10',
        'heart_rate', 'sleep_quality', 'activity_level',
        'anxiety_level', 'mood_score', 'social_engagement', 'family_history_asd'
    ]
    
    X = df[feature_columns]
    y = df['stress_level']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train Random Forest model
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight='balanced'
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    train_accuracy = model.score(X_train_scaled, y_train)
    test_accuracy = model.score(X_test_scaled, y_test)
    
    print(f"Training Accuracy: {train_accuracy:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    
    # Save model and scaler
    joblib.dump(model, 'stress_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    joblib.dump(feature_columns, 'feature_columns.pkl')
    
    print("\nModel saved successfully!")
    
    return model, scaler, feature_columns

if __name__ == "__main__":
    print("Generating Autism Stress Dataset...")
    df = generate_autism_stress_dataset(2000)
    
    # Save dataset
    df.to_csv('autism_stress_dataset.csv', index=False)
    print(f"Dataset saved: {len(df)} samples")
    print(f"\nStress Level Distribution:")
    print(df['stress_level'].value_counts().sort_index())
    
    # Train model
    print("\nTraining ML Model...")
    model, scaler, features = train_stress_model(df)
    
    print(f"\nFeature columns: {features}")
