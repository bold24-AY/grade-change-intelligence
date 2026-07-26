# API Specification (v1)

This document details the REST API endpoints available in the Grade Change Intelligence backend.

## Base URL
`/api/v1`

---

## 1. Prediction Endpoints

### `POST /prediction/predict`
Executes real-time inference on a frame of paper machine sensor telemetry to determine if a grade transition is occurring.

#### Request Body
```json
{
  "timestamp": "2026-07-26T12:03:00Z",
  "pulp_flow_m3h": 420.0,
  "consistency_pct": 3.10,
  "steam_pressure_bar": 3.80,
  "machine_speed_mpm": 820.0
}
```

#### Response Body (200 OK)
```json
{
  "timestamp": "2026-07-26T12:03:00Z",
  "is_transitioning": true,
  "confidence_score": 0.87,
  "predicted_target_grade": "GRADE_B",
  "anomaly_detected": false
}
```

---

## 2. Monitoring Endpoints

### `GET /monitoring/health`
Checks backend and pipeline services health.

#### Response Body (200 OK)
```json
{
  "status": "healthy",
  "timestamp": "2026-07-26T15:20:00Z",
  "model_version": "1.0.0",
  "uptime_seconds": 12450
}
```

### `GET /monitoring/specs`
Retrieves current target specifications for all paper grades.

#### Response Body (200 OK)
```json
{
  "GRADE_A": {
    "name": "Standard Copier Paper 80gsm",
    "target_basis_weight_gsm": 80.0,
    "target_moisture_pct": 5.5
  },
  "GRADE_B": {
    "name": "Premium Heavyweight Cardstock 120gsm",
    "target_basis_weight_gsm": 120.0,
    "target_moisture_pct": 6.2
  }
}
```
