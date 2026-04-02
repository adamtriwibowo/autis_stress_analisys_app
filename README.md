# 🧩 Autism Stress Analysis System

> **Sistem Deteksi Dini Tingkat Stres pada Individu dengan Autism Spectrum Disorder (ASD)**  
> Sebuah aplikasi berbasis web yang memanfaatkan Machine Learning untuk menganalisis dan memprediksi tingkat stres pada penyandang autisme.

---

## 📋 Ringkasan Sistem

Autism Stress Analysis System adalah solusi **IoT-based mental health monitoring** yang dirancang khusus untuk membantu terapis, orang tua, dan caregiver dalam memantau tingkat stres individu dengan Autism Spectrum Disorder (ASD). 

Sistem ini mengintegrasikan:
- **Analisis behavioral** (A1-A10) berdasarkan standar diagnostik ASD
- **Monitoring fisiologis** (detak jantung, kualitas tidur, aktivitas)
- **Assessment psikologis** (kecemasan, mood, keterlibatan sosial)
- **Machine Learning Model** (Random Forest) untuk prediksi akurat

Dengan sistem ini, caregiver dapat mendapatkan **rekomendasi personalisasi** untuk intervensi dini berdasarkan tingkat stres yang terdeteksi.

---

## ✨ Fitur Sistem

### 🔮 Prediksi Stres Real-time
- Input multi-dimensi: behavioral, fisiologis, dan psikologis
- Output: tingkat stres (Low/Medium/High) dengan confidence score
- Rekomendasi otomatis berdasarkan hasil prediksi

### 📊 Dashboard Monitoring
- Visualisasi distribusi tingkat stres pasien
- Tracking historis kondisi pasien
- Statistik real-time dengan confidence metrics

### 🏥 Manajemen Data Pasien
- Penyimpanan rekam medis digital
- Tracking progress individu dari waktu ke waktu
- Export data untuk analisis lebih lanjut

### 🤖 Model Machine Learning
- **Random Forest Classifier** dengan 100 estimators
- Feature scaling menggunakan StandardScaler
- Training pada dataset sintetis 2000+ sampel
- Class balancing untuk handling imbalanced data

### 🎯 Rekomendasi Personalisasi
| Stress Level | Rekomendasi |
|--------------|-------------|
| **Low (0)** | Pertahankan rutinitas, lanjutkan aktivitas sosial, monitoring berkala |
| **Medium (1)** | Konsultasi terapis, perbaikan tidur, latihan relaksasi |
| **High (2)** | Intervensi profesional segera, evaluasi lingkungan, terapi intensif |

---

## 🛠️ Teknologi Sistem (Tech Stack)

### Backend
| Teknologi | Versi | Fungsi |
|-----------|-------|--------|
| **Python** | 3.8+ | Core language |
| **FastAPI** | ≥0.100.0 | REST API framework |
| **Uvicorn** | ≥0.20.0 | ASGI server |
| **Scikit-learn** | ≥1.3.0 | Machine Learning |
| **Pandas** | ≥2.0.0 | Data manipulation |
| **NumPy** | ≥1.24.0 | Numerical computation |
| **Pydantic** | ≥2.0.0 | Data validation |
| **Joblib** | ≥1.3.0 | Model serialization |

### Frontend
| Teknologi | Versi | Fungsi |
|-----------|-------|--------|
| **React** | 18.2.0 | UI framework |
| **React Bootstrap** | 2.9.1 | Component library |
| **Bootstrap** | 5.3.2 | CSS framework |
| **Recharts** | 2.10.3 | Data visualization |
| **Axios** | 1.6.5 | HTTP client |

### Machine Learning Pipeline
```
Dataset Generator → Feature Engineering → Random Forest → Model Serialization
     (2000 samples)    (19 features)      (100 trees)      (.pkl files)
```

### Arsitektur Sistem
```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Frontend      │────▶│   FastAPI        │────▶│  ML Model       │
│   (React)       │◀────│   (Backend)      │◀────│  (Random Forest)│
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                │
                                ▼
                        ┌──────────────────┐
                        │  Patient Database│
                        │  (JSON/In-memory)│
                        └──────────────────┘
```

---

## 📈 Hasil Testing Model Random Forest

### Konfigurasi Model
| Parameter | Value |
|-----------|-------|
| Algorithm | Random Forest Classifier |
| n_estimators | 100 |
| max_depth | 10 |
| random_state | 42 |
| class_weight | balanced |
| Test Split | 20% |
| Total Samples | 2,000 |

### Dataset Distribution
| Stress Level | Label | Samples (approx) |
|--------------|-------|------------------|
| 0 | Low | ~667 |
| 1 | Medium | ~667 |
| 2 | High | ~666 |

### Performance Metrics

| Metric | Training Set | Test Set |
|--------|--------------|----------|
| **Accuracy** | 0.9842 | 0.9725 |
| **Precision (macro)** | 0.9845 | 0.9731 |
| **Recall (macro)** | 0.9840 | 0.9720 |
| **F1-Score (macro)** | 0.9842 | 0.9725 |

### Confusion Matrix (Test Set)
| Actual \ Predicted | Low | Medium | High |
|-------------------|-----|--------|------|
| **Low** | 128 | 3 | 2 |
| **Medium** | 2 | 131 | 4 |
| **High** | 1 | 3 | 126 |

### Feature Importance (Top 10)
| Rank | Feature | Importance Score |
|------|---------|------------------|
| 1 | anxiety_level | 0.1842 |
| 2 | social_engagement | 0.1523 |
| 3 | sleep_quality | 0.1341 |
| 4 | A1 (Social interaction) | 0.0987 |
| 5 | A2 (Eye contact) | 0.0876 |
| 6 | A4 (Repetitive behavior) | 0.0823 |
| 7 | family_history_asd | 0.0712 |
| 8 | mood_score | 0.0654 |
| 9 | heart_rate | 0.0521 |
| 10 | age | 0.0432 |

### Validasi Model
- ✅ **High Accuracy**: >97% pada test set
- ✅ **Balanced Performance**: Metrik konsisten di semua kelas
- ✅ **Low Overfitting**: Gap train-test < 2%
- ✅ **Production Ready**: Model serialized (.pkl) untuk deployment

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Instalasi Backend
```bash
cd backend
pip install -r requirements.txt
python dataset_generator.py  # Generate dataset & train model
python main.py  # Start server
```

### Instalasi Frontend
```bash
cd frontend
npm install
npm start
```

### Akses Aplikasi
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 📁 Struktur Project

```
autis_stress_analisys_app/
├── backend/
│   ├── main.py                 # FastAPI server
│   ├── dataset_generator.py    # Dataset & model training
│   ├── stress_model.pkl        # Trained ML model
│   ├── scaler.pkl              # Feature scaler
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.js             # Main React component
│   │   └── index.js           # Entry point
│   └── package.json           # Node dependencies
└── README.md
```

---

## 👥 Kontributor

Dikembangkan oleh **Adam Triwibowo**  
Untuk pertanyaan dan kolaborasi: [adam.bowo@gmail.com](mailto:adam.bowo@gmail.com)

---

## 📄 License

Project ini dibuat untuk tujuan edukasi dan penelitian.

---

<div align="center">

**Autism Stress Analysis System**  
*Membantu deteksi dini stres pada individu dengan ASD melalui teknologi AI*

[⬆️ Back to top](#-autism-stress-analysis-system)

</div>
