import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Form, Alert, Spinner, Badge, Tabs, Tab, Table } from 'react-bootstrap';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const API_URL = 'http://127.0.0.1:8000';

const COLORS = ['#28a745', '#ffc107', '#dc3545'];

function App() {
  const [activeTab, setActiveTab] = useState('prediction');
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState('');
  const [patients, setPatients] = useState([]);
  const [statistics, setStatistics] = useState(null);
  
  const [formData, setFormData] = useState({
    patient_name: '',
    age: 10,
    gender: 1,
    A1: 2, A2: 2, A3: 2, A4: 2, A5: 2, A6: 2, A7: 2, A8: 2, A9: 2, A10: 2,
    heart_rate: 80,
    sleep_quality: 5.0,
    activity_level: 5.0,
    anxiety_level: 5.0,
    mood_score: 5.0,
    social_engagement: 5.0,
    family_history_asd: 0
  });

  const handleInputChange = (e) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' || type === 'range' ? parseFloat(value) : value
    }));
  };

  const loadPreset = (level) => {
    const presets = {
      low: {
        patient_name: '',
        age: 10,
        gender: 1,
        A1: 1, A2: 1, A3: 1, A4: 1, A5: 1, A6: 1, A7: 1, A8: 1, A9: 1, A10: 1,
        heart_rate: 70,
        sleep_quality: 8.0,
        activity_level: 8.0,
        anxiety_level: 2.0,
        mood_score: 8.0,
        social_engagement: 8.0,
        family_history_asd: 0
      },
      medium: {
        patient_name: '',
        age: 12,
        gender: 1,
        A1: 2, A2: 2, A3: 2, A4: 2, A5: 2, A6: 2, A7: 2, A8: 2, A9: 2, A10: 2,
        heart_rate: 100,
        sleep_quality: 5.0,
        activity_level: 5.0,
        anxiety_level: 5.0,
        mood_score: 5.0,
        social_engagement: 5.0,
        family_history_asd: 0
      },
      high: {
        patient_name: '',
        age: 15,
        gender: 1,
        A1: 3, A2: 3, A3: 3, A4: 3, A5: 3, A6: 3, A7: 3, A8: 3, A9: 3, A10: 3,
        heart_rate: 135,
        sleep_quality: 1.5,
        activity_level: 2.0,
        anxiety_level: 9.5,
        mood_score: 1.5,
        social_engagement: 1.5,
        family_history_asd: 1
      }
    };
    setFormData(presets[level]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setPrediction(null);

    try {
      const predictResponse = await axios.post(`${API_URL}/predict`, formData);
      const predictionData = predictResponse.data;

      const saveResponse = await axios.post(`${API_URL}/save-patient`, {
        ...formData,
        prediction: predictionData
      });

      predictionData.patient_id = saveResponse.data.patient_id;
      setPrediction(predictionData);
      
      fetchPatients();
      fetchStatistics();
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Terjadi kesalahan. Pastikan backend sudah berjalan.';
      setError(typeof errorMsg === 'string' ? errorMsg : 'Terjadi kesalahan pada sistem');
    } finally {
      setLoading(false);
    }
  };

  const fetchPatients = async () => {
    try {
      const response = await axios.get(`${API_URL}/patients`);
      setPatients(Array.isArray(response.data) ? response.data : []);
    } catch (err) {
      console.error('Error fetching patients:', err);
      setPatients([]);
    }
  };

  const fetchStatistics = async () => {
    try {
      const response = await axios.get(`${API_URL}/statistics`);
      setStatistics(response.data);
    } catch (err) {
      console.error('Error fetching statistics:', err);
    }
  };

  useEffect(() => {
    fetchPatients();
    fetchStatistics();
  }, []);

  const getStressBadge = (level) => {
    const variants = { 0: 'success', 1: 'warning', 2: 'danger' };
    return variants[level] || 'secondary';
  };

  const stressDistributionData = statistics && statistics.stress_distribution ? [
    { name: 'Low', value: Number(statistics.stress_distribution.Low) || 0 },
    { name: 'Medium', value: Number(statistics.stress_distribution.Medium) || 0 },
    { name: 'High', value: Number(statistics.stress_distribution.High) || 0 }
  ] : [];

  const totalPatients = statistics ? Number(statistics.total_patients) || 0 : 0;
  const avgConfidence = statistics && statistics.average_confidence 
    ? (Number(statistics.average_confidence) * 100).toFixed(1) 
    : '0';

  return (
    <Container fluid className="py-4">
      <Row className="mb-4">
        <Col>
          <h1 className="text-primary">Autism Stress Detection System</h1>
          <p className="text-muted">Sistem Analisis Stres untuk Pasien Autisme Berbasis Machine Learning</p>
        </Col>
      </Row>

      <Tabs activeKey={activeTab} onSelect={setActiveTab} className="mb-4">
        <Tab eventKey="prediction" title="Prediksi Stres">
          <Row>
            <Col lg={8}>
              <Card>
                <Card.Header>
                  <h5>Input Data Pasien</h5>
                </Card.Header>
                <Card.Body>
                  {/* Preset Buttons */}
                  <div className="mb-3">
                    <label className="form-label fw-bold">Preset Cepat (untuk testing):</label>
                    <div className="d-flex gap-2 flex-wrap">
                      <Button variant="outline-success" size="sm" onClick={() => loadPreset('low')}>
                        ✅ Low Stress (0-33)
                      </Button>
                      <Button variant="outline-warning" size="sm" onClick={() => loadPreset('medium')}>
                        ⚠️ Medium Stress (34-66)
                      </Button>
                      <Button variant="outline-danger" size="sm" onClick={() => loadPreset('high')}>
                        🚨 High Stress (67-100)
                      </Button>
                    </div>
                  </div>

                  <Form onSubmit={handleSubmit}>
                    <Row>
                      <Col md={6}>
                        <Form.Group className="mb-3">
                          <Form.Label>Nama Pasien (Opsional)</Form.Label>
                          <Form.Control
                            type="text"
                            name="patient_name"
                            value={formData.patient_name}
                            onChange={handleInputChange}
                            placeholder="Masukkan nama pasien"
                          />
                        </Form.Group>
                      </Col>
                      <Col md={6}>
                        <Form.Group className="mb-3">
                          <Form.Label>Usia (tahun)</Form.Label>
                          <Form.Control
                            type="number"
                            name="age"
                            value={formData.age}
                            onChange={handleInputChange}
                            min={3}
                            max={25}
                          />
                        </Form.Group>
                      </Col>
                    </Row>

                    <Form.Group className="mb-3">
                      <Form.Label>Gender</Form.Label>
                      <div>
                        <Form.Check
                          inline
                          type="radio"
                          name="gender"
                          id="gender-female"
                          label="Perempuan"
                          value={0}
                          checked={formData.gender === 0}
                          onChange={handleInputChange}
                        />
                        <Form.Check
                          inline
                          type="radio"
                          name="gender"
                          id="gender-male"
                          label="Laki-laki"
                          value={1}
                          checked={formData.gender === 1}
                          onChange={handleInputChange}
                        />
                      </div>
                    </Form.Group>

                    <hr />
                    <h6 className="text-primary mb-3">Fitur Behavioral (A1-A10)</h6>
                    <Row>
                      {[
                        { id: 'A1', label: 'Interaksi Sosial' },
                        { id: 'A2', label: 'Kontak Mata' },
                        { id: 'A3', label: 'Komunikasi' },
                        { id: 'A4', label: 'Perilaku Repetitif' },
                        { id: 'A5', label: 'Sensitivitas Sensorik' },
                        { id: 'A6', label: 'Kepatuhan Rutinitas' },
                        { id: 'A7', label: 'Senyum Sosial' },
                        { id: 'A8', label: 'Respon Nama' },
                        { id: 'A9', label: 'Manipulasi Objek' },
                        { id: 'A10', label: 'Respon Emosional' }
                      ].map((feature) => (
                        <Col md={4} key={feature.id}>
                          <Form.Group className="mb-3">
                            <Form.Label>{feature.label} ({feature.id})</Form.Label>
                            <Form.Range
                              name={feature.id}
                              value={formData[feature.id]}
                              onChange={handleInputChange}
                              min={1}
                              max={3}
                              step={1}
                            />
                            <div className="d-flex justify-content-between">
                              <small>1</small>
                              <small className="fw-bold">{formData[feature.id]}</small>
                              <small>3</small>
                            </div>
                          </Form.Group>
                        </Col>
                      ))}
                    </Row>

                    <hr />
                    <h6 className="text-primary mb-3">Fitur Fisiologis & Psikologis</h6>
                    <Row>
                      <Col md={4}>
                        <Form.Group className="mb-3">
                          <Form.Label>Detak Jantung (bpm)</Form.Label>
                          <Form.Control
                            type="number"
                            name="heart_rate"
                            value={formData.heart_rate}
                            onChange={handleInputChange}
                            min={60}
                            max={140}
                          />
                        </Form.Group>
                      </Col>
                      <Col md={4}>
                        <Form.Group className="mb-3">
                          <Form.Label>Kualitas Tidur (1-10)</Form.Label>
                          <Form.Range
                            name="sleep_quality"
                            value={formData.sleep_quality}
                            onChange={handleInputChange}
                            min={1}
                            max={10}
                            step={0.5}
                          />
                          <div className="text-center">{Number(formData.sleep_quality).toFixed(1)}</div>
                        </Form.Group>
                      </Col>
                      <Col md={4}>
                        <Form.Group className="mb-3">
                          <Form.Label>Level Aktivitas (1-10)</Form.Label>
                          <Form.Range
                            name="activity_level"
                            value={formData.activity_level}
                            onChange={handleInputChange}
                            min={1}
                            max={10}
                            step={0.5}
                          />
                          <div className="text-center">{Number(formData.activity_level).toFixed(1)}</div>
                        </Form.Group>
                      </Col>
                      <Col md={4}>
                        <Form.Group className="mb-3">
                          <Form.Label>Level Kecemasan (1-10)</Form.Label>
                          <Form.Range
                            name="anxiety_level"
                            value={formData.anxiety_level}
                            onChange={handleInputChange}
                            min={1}
                            max={10}
                            step={0.5}
                          />
                          <div className="text-center">{Number(formData.anxiety_level).toFixed(1)}</div>
                        </Form.Group>
                      </Col>
                      <Col md={4}>
                        <Form.Group className="mb-3">
                          <Form.Label>Skor Mood (1-10)</Form.Label>
                          <Form.Range
                            name="mood_score"
                            value={formData.mood_score}
                            onChange={handleInputChange}
                            min={1}
                            max={10}
                            step={0.5}
                          />
                          <div className="text-center">{Number(formData.mood_score).toFixed(1)}</div>
                        </Form.Group>
                      </Col>
                      <Col md={4}>
                        <Form.Group className="mb-3">
                          <Form.Label>Engagement Sosial (1-10)</Form.Label>
                          <Form.Range
                            name="social_engagement"
                            value={formData.social_engagement}
                            onChange={handleInputChange}
                            min={1}
                            max={10}
                            step={0.5}
                          />
                          <div className="text-center">{Number(formData.social_engagement).toFixed(1)}</div>
                        </Form.Group>
                      </Col>
                    </Row>

                    <Form.Group className="mb-3">
                      <Form.Label>Riwayat Keluarga ASD</Form.Label>
                      <div>
                        <Form.Check
                          inline
                          type="radio"
                          name="family_history_asd"
                          id="family-no"
                          label="Tidak"
                          value={0}
                          checked={formData.family_history_asd === 0}
                          onChange={handleInputChange}
                        />
                        <Form.Check
                          inline
                          type="radio"
                          name="family_history_asd"
                          id="family-yes"
                          label="Ya"
                          value={1}
                          checked={formData.family_history_asd === 1}
                          onChange={handleInputChange}
                        />
                      </div>
                    </Form.Group>

                    <Button variant="primary" type="submit" disabled={loading} className="w-100">
                      {loading ? (
                        <span><Spinner animation="border" size="sm" /> Menganalisis...</span>
                      ) : 'Prediksi Tingkat Stres'}
                    </Button>
                  </Form>
                </Card.Body>
              </Card>
            </Col>

            <Col lg={4}>
              {prediction && (
                <Card className="mb-3">
                  <Card.Header className={'bg-' + getStressBadge(prediction.stress_level) + ' text-white'}>
                    <h5>Hasil Prediksi</h5>
                  </Card.Header>
                  <Card.Body>
                    <div className="text-center mb-3">
                      <Badge bg={getStressBadge(prediction.stress_level)} pill className="fs-4">
                        {String(prediction.stress_level_label)}
                      </Badge>
                    </div>
                    <div className="mb-3">
                      <label>Stress Score: {Number(prediction.stress_score).toFixed(1)}/100</label>
                      <div className="progress">
                        <div
                          className={'progress-bar bg-' + getStressBadge(prediction.stress_level)}
                          style={{ width: String(Number(prediction.stress_score)) + '%' }}
                        />
                      </div>
                    </div>
                    <div className="mb-3">
                      <label>Confidence: {(Number(prediction.confidence) * 100).toFixed(1)}%</label>
                      <div className="progress">
                        <div
                          className="progress-bar bg-info"
                          style={{ width: String(Number(prediction.confidence) * 100) + '%' }}
                        />
                      </div>
                    </div>
                    <hr />
                    <h6>Rekomendasi:</h6>
                    <ul className="small">
                      {Array.isArray(prediction.recommendations) && prediction.recommendations.map((rec, idx) => (
                        <li key={idx}>{String(rec)}</li>
                      ))}
                    </ul>
                    {prediction.patient_id && (
                      <Badge bg="secondary">Patient ID: #{prediction.patient_id}</Badge>
                    )}
                  </Card.Body>
                </Card>
              )}

              {error && (
                <Alert variant="danger">
                  <Alert.Heading>Error</Alert.Heading>
                  <p>{String(error)}</p>
                </Alert>
              )}

              <Card>
                <Card.Header>
                  <h6>Panduan Skor</h6>
                </Card.Header>
                <Card.Body>
                  <ul className="small mb-0">
                    <li><Badge bg="success">Low</Badge>: 0-33 (Stres rendah, kondisi stabil)</li>
                    <li><Badge bg="warning">Medium</Badge>: 34-66 (Perlu perhatian)</li>
                    <li><Badge bg="danger">High</Badge>: 67-100 (Memerlukan intervensi)</li>
                  </ul>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Tab>

        <Tab eventKey="patients" title="Data Pasien">
          <Card>
            <Card.Header>
              <h5>Riwayat Pasien</h5>
            </Card.Header>
            <Card.Body>
              {patients.length === 0 ? (
                <p className="text-muted text-center">Belum ada data pasien</p>
              ) : (
                <div className="table-responsive">
                  <Table striped hover>
                    <thead>
                      <tr>
                        <th>ID</th>
                        <th>Waktu</th>
                        <th>Nama</th>
                        <th>Usia</th>
                        <th>Gender</th>
                        <th>Stress Level</th>
                        <th>Score</th>
                        <th>Confidence</th>
                      </tr>
                    </thead>
                    <tbody>
                      {patients.map((patient) => (
                        <tr key={String(patient.id)}>
                          <td>#{patient.id}</td>
                          <td>{new Date(patient.timestamp).toLocaleString('id-ID')}</td>
                          <td>{patient.patient_name || '-'}</td>
                          <td>{patient.input_data.age}</td>
                          <td>{patient.input_data.gender === 0 ? 'P' : 'L'}</td>
                          <td>
                            <Badge bg={getStressBadge(patient.prediction.stress_level)}>
                              {String(patient.prediction.stress_level_label)}
                            </Badge>
                          </td>
                          <td>{Number(patient.prediction.stress_score).toFixed(1)}</td>
                          <td>{(Number(patient.prediction.confidence) * 100).toFixed(1)}%</td>
                        </tr>
                      ))}
                    </tbody>
                  </Table>
                </div>
              )}
            </Card.Body>
          </Card>
        </Tab>

        <Tab eventKey="statistics" title="Statistik">
          <Row>
            <Col md={6}>
              <Card className="mb-3">
                <Card.Header>
                  <h5>Distribusi Tingkat Stres</h5>
                </Card.Header>
                <Card.Body>
                  {totalPatients > 0 && stressDistributionData.length > 0 ? (
                    <ResponsiveContainer width="100%" height={300}>
                      <PieChart>
                        <Pie
                          data={stressDistributionData}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          label={({ name, value }) => String(name) + ': ' + String(value)}
                          outerRadius={100}
                          fill="#8884d8"
                          dataKey="value"
                        >
                          {stressDistributionData.map((entry, index) => (
                            <Cell key={'cell-' + index} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  ) : (
                    <p className="text-muted text-center">Belum ada data</p>
                  )}
                </Card.Body>
              </Card>
            </Col>
            <Col md={6}>
              <Card className="mb-3">
                <Card.Header>
                  <h5>Ringkasan</h5>
                </Card.Header>
                <Card.Body>
                  <div>
                    <h3 className="text-primary">{totalPatients}</h3>
                    <p>Total Pasien</p>
                    <hr />
                    <div className="row">
                      <div className="col-4 text-center">
                        <Badge bg="success" className="fs-6">
                          {statistics ? (Number(statistics.stress_distribution?.Low) || 0) : 0}
                        </Badge>
                        <div className="small">Low</div>
                      </div>
                      <div className="col-4 text-center">
                        <Badge bg="warning" className="fs-6">
                          {statistics ? (Number(statistics.stress_distribution?.Medium) || 0) : 0}
                        </Badge>
                        <div className="small">Medium</div>
                      </div>
                      <div className="col-4 text-center">
                        <Badge bg="danger" className="fs-6">
                          {statistics ? (Number(statistics.stress_distribution?.High) || 0) : 0}
                        </Badge>
                        <div className="small">High</div>
                      </div>
                    </div>
                    <hr />
                    <p>Average Confidence: <strong>{avgConfidence}%</strong></p>
                  </div>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Tab>
      </Tabs>
    </Container>
  );
}

export default App;
