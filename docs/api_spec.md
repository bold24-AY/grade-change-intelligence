# API Specification (v1)

This document details the REST API endpoints available in the Grade Change Intelligence backend.

## Base URL
`/api/v1`

---

## 1. Prediction & Inference Endpoints

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

## 2. Recommendation Endpoints

### `POST /prediction/recommend`
Generates real-time controller setpoint delta recommendations to stabilize deviations.

#### Request Body
```json
{
  "telemetry": {
    "pulp_flow_m3h": 450.0,
    "consistency_pct": 3.4,
    "steam_pressure_bar": 4.2,
    "machine_speed_mpm": 850.0,
    "basis_weight_gsm": 82.0,
    "active_grade_id": "GRADE_A"
  },
  "prediction": {
    "is_basis_weight_off_spec": true,
    "confidence_score": 0.88,
    "basis_weight_dev": 2.0
  }
}
```

#### Response Body (200 OK)
```json
{
  "active_grade_id": "GRADE_A",
  "adjustments": {
    "stock_flow_m3h_delta": -11.0,
    "filler_flow_lmin_delta": -4.0,
    "steam_pressure_bar_delta": 0.8,
    "machine_speed_mpm_delta": -4.2
  },
  "explanation": {
    "why": "The scanner measures a basis weight deviation of +2.00 gsm. To correct this, we recommend to reduce stock flow by -11.00 m3/h.",
    "confidence": 0.92,
    "historical_evidence": [
      {
        "timestamp": "2026-07-25T14:32:00Z",
        "pulp_flow_m3h": 448.0,
        "machine_speed_mpm": 845.0,
        "similarity_score": 0.9412
      }
    ],
    "operator_notes": "For standard 80gsm copy paper, prioritize pulp flow consistency checks. Maintain speed above 800mpm."
  }
}
```

---

## 3. Explainable AI (XAI) Endpoints

### `POST /prediction/explain`
Calculates SHAP feature attributions and operator text summaries explaining the predictions.

#### Request Body
```json
{
  "pulp_flow_m3h": 480.0,
  "machine_speed_mpm": 850.0
}
```

#### Response Body (200 OK)
```json
{
  "risk_percentage": 85.0,
  "why_nlp": "The system indicates a HIGH off-spec deviation risk (85.0% probability). The primary driver is Thick Stock Pulp Flow (measured at 480.0), contributing to 88.0% of the model's decision path.",
  "influential_variables": [
    {
      "variable_name": "Thick Stock Pulp Flow",
      "value": 480.0,
      "shap_value": 2.5,
      "percentage_impact": 88.0,
      "direction": "INCREASE"
    }
  ],
  "historical_references": [
    {
      "timestamp": "2026-07-25T14:32:00Z",
      "description": "Similar high pulp flow event resolved by stock valve step change (-8 m³/h).",
      "similarity": 0.9412
    }
  ],
  "confidence_score": 0.85
}
```

---

## 4. Monitoring Endpoints

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
Standard JSON responses are structured using FastAPI models.
