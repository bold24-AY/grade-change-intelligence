# Smart India Hackathon (SIH) - Presentation Assets Catalog

This document catalog contains every diagram required for the Grade Change Intelligence presentation slides, rendered using **Mermaid** and standalone vector **SVG** wireframes.

---

## 1. System Architecture Diagram
Depicts the decoupled clean architecture layers from operator interactions to backend services.

```mermaid
graph TB
    subgraph Presentation Layer
        StreamlitApp[Streamlit Dashboard Client]
    end

    subgraph API Gateway Layer
        FastAPIApp[FastAPI Web Server]
        Auth[Authentication & CORS]
    end

    subgraph Business Logic Services
        PredictionSvc[PredictionService]
        RecommendationSvc[RecommendationEngine]
        ExplanationSvc[ShapExplanationService]
        NLPComp[NlpExplanationService]
    end

    subgraph Data Pipeline Service
        DataLoader[DataLoader]
        Cleaner[DataCleaner]
        FeatureEng[FeatureEngineer]
        Scaler[DataProcessor]
        Validator[DataValidator]
        Versioner[DataVersioner]
    end

    subgraph Data & Checkpoint Registries
        RawDB[(Raw Telemetry Logs)]
        FeatureStore[(Processed CSV Feature Store)]
        ModelRegistry[(Model Checkpoint Registry)]
    end

    StreamlitApp -->|HTTP POST Requests| FastAPIApp
    FastAPIApp --> Auth
    Auth --> PredictionSvc
    Auth --> RecommendationSvc
    Auth --> ExplanationSvc
    
    PredictionSvc -->|Load Model| ModelRegistry
    ExplanationSvc -->|SHAP attributions| NLPComp
    RecommendationSvc -->|Historical Nearest Neighbor Search| FeatureStore
    
    DataLoader --> RawDB
    Cleaner --> Loader
    FeatureEng --> Cleaner
    Scaler --> FeatureEng
    Validator --> Scaler
    Versioner --> Validator
    Versioner --> FeatureStore
```

---

## 2. Operator Flowchart
Step-by-step control room operator workflow during off-specification basis weight anomalies.

```mermaid
flowchart TD
    Start([1. Real-time Telemetry Stream]) --> CheckAlarm{2. Deviation Exceeds Spec?}
    CheckAlarm -- No --> KeepMonitoring[3. Maintain Current Controls]
    KeepMonitoring --> Start
    
    CheckAlarm -- Yes --> TriggerAlarm[4. Flash Alarm: OFF-SPEC]
    TriggerAlarm --> ViewPrediction[5. Open Dashboard: Review Risk Probability]
    ViewPrediction --> ViewXAI[6. Inspect Drivers: SHAP Causal Analysis]
    ViewXAI --> ViewRecommendations[7. Review AI Setpoint Recommendations]
    ViewRecommendations --> ViewHistory[8. Compare Similar Historical Cases]
    ViewHistory --> OperatorDecision{9. Operator Decision?}
    
    OperatorDecision -- Reject --> LogRejection[10. Click Reject: Log Feedback]
    LogRejection --> MaintainState[11. Manually Override Controls]
    MaintainState --> Start
    
    OperatorDecision -- Accept --> LogAcceptance[12. Click Accept: Log Action]
    LogAcceptance --> PushControls[13. Deploy Deltas to Machinery Valves]
    PushControls --> StabilizeProcess[14. Basis Weight Returns to Spec]
    StabilizeProcess --> Start
```

---

## 3. Use Case Diagram
Maps actor roles to specific machine interactions.

```mermaid
leftToRightDirection
graph TD
    subgraph Users
        Operator((Plant Operator))
        DataScientist((Data Scientist))
        Admin((System Admin))
    end

    subgraph Use Cases
        UC1[Monitor Real-time Telemetry]
        UC2[Inspect Off-Spec Predictions]
        UC3[Apply Recommendation Deltas]
        UC4[Export PDF Quality Reports]
        UC5[Trigger Model Retraining]
        UC6[Verify Pipeline Manifests]
        UC7[Configure Gains & Safety Limits]
        UC8[Rotate Application Logs]
    end

    Operator --> UC1
    Operator --> UC2
    Operator --> UC3
    Operator --> UC4

    DataScientist --> UC5
    DataScientist --> UC6
    
    Admin --> UC7
    Admin --> UC8
```

---

## 4. Data Flow Diagram (DFD Level 1)
Details the flow of telemetry data from machines, through ML inferences, to operator displays.

```mermaid
graph LR
    subgraph Data Sources
        RawLogs[(Raw Telemetry Logs)]
    end

    subgraph Data Pipeline
        Loader[Loader]
        Clean[Cleaner]
        Feature[Feature Engineer]
        Scale[Processor Scaler]
    end

    subgraph Core ML & Decision Services
        MLInference[ML Predictor Classifier]
        XAIModel[SHAP Explainer]
        RecEngine[Recommendation Engine]
    end

    subgraph Sinks & Presentation
        FeatureCSV[(Processed CSV Store)]
        RegistryJSON[(Model Registry Manifest)]
        DashboardUI[Streamlit Operator UI]
    end

    RawLogs -->|1. Ingest| Loader
    Loader -->|2. Impute| Clean
    Clean -->|3. Rolling Stats| Feature
    Feature -->|4. Normalize| Scale
    Scale -->|5. Hashed Features| FeatureCSV
    
    FeatureCSV -->|6. Feed Vector| MLInference
    RegistryJSON -->|7. Model Parameters| MLInference
    
    MLInference -->|8. Predicted Risk| XAIModel
    MLInference -->|9. Deviation Value| RecEngine
    
    XAIModel -->|10. Driver Importances| DashboardUI
    RecEngine -->|11. Adjustments Cards| DashboardUI
```

---

## 5. Pipeline Diagram
Details the execution sequence of cleaning, feature engineering, and manifest version registration.

```mermaid
graph TD
    Step1[1. Load CSV/Excel Files] --> Step2[2. Chronological Log Sorting]
    Step2 --> Step3[3. Forward & Backward Fill Imputation]
    Step3 --> Step4[4. Rolling Z-Score Outlier Clipping]
    Step4 --> Step5[5. Calculate Rolling Means & Std Devs]
    Step5 --> Step6[6. Calculate Difference Derivatives]
    Step6 --> Step7[7. Calculate Shifted Lags]
    Step7 --> Step8[8. Exclude Targets & Standard Scale Features]
    Step8 --> Step9[9. Categorical Label Mappings]
    Step9 --> Step10[10. Compute Dataset SHA-256 Hash]
    Step10 --> Step11[11. Save Version Manifest log]
```

---

## 6. Sequence Diagram
Timeline of user interactions, REST backend services, and serialization registries.

```mermaid
sequenceDiagram
    autonumber
    actor Operator as Plant Operator
    participant UI as Streamlit UI Client
    participant API as FastAPI REST Gateway
    participant Pipeline as Data Processor Pipeline
    participant MLs as ML Prediction Model
    participant XAIs as SHAP Explainer
    participant Recs as Recommendation Engine

    Operator->>UI: Slide simulated telemetry parameters
    UI->>API: HTTP POST /prediction/predict (telemetry)
    API->>Pipeline: Clean & scale input vector
    Pipeline-->>API: Standardized features
    API->>MLs: Evaluate probability (X_instance)
    MLs-->>API: Risk probability (prob=0.88)
    
    API->>XAIs: compute_shap_attributions(X_instance)
    XAIs-->>API: Attribution values & expected base
    
    API->>Recs: generate_recommendation(telemetry, prediction)
    Recs-->>API: Recommended Setpoint Deltas & Matches
    
    API-->>UI: Return merged recommendations & XAI cards
    UI-->>Operator: Render Dark Mode Alarms & Plotly charts
```

---

## 7. Dashboard Wireframe (SVG View)
Vector schematic diagram illustrating the industrial command center user interface layout.

```xml
<svg width="800" height="500" viewBox="0 0 800 500" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- General Background -->
  <rect width="800" height="500" fill="#0b0f19" rx="8" />
  
  <!-- Sidebar Navigator -->
  <rect width="180" height="500" fill="#0f172a" />
  <line x1="180" y1="0" x2="180" y2="500" stroke="#1e293b" />
  
  <!-- Sidebar Branding -->
  <circle cx="90" cy="50" r="24" fill="#1e3d59" />
  <text x="90" y="54" fill="#ffffff" font-family="Helvetica" font-size="11" text-anchor="middle">GRADE CHANGE</text>
  <text x="90" y="100" fill="#94a3b8" font-family="Helvetica" font-size="10" text-anchor="middle">Operator Terminal</text>
  
  <!-- Sidebar Menu Buttons -->
  <rect x="10" y="130" width="160" height="30" rx="4" fill="#1e293b" />
  <text x="25" y="149" fill="#f1f5f9" font-family="Helvetica" font-size="11">Overview</text>
  <text x="25" y="189" fill="#94a3b8" font-family="Helvetica" font-size="11">Predictions</text>
  <text x="25" y="229" fill="#94a3b8" font-family="Helvetica" font-size="11">Analytics</text>
  <text x="25" y="269" fill="#94a3b8" font-family="Helvetica" font-size="11">Recommendations</text>
  
  <!-- Header Block -->
  <text x="200" y="40" fill="#ffffff" font-family="Helvetica" font-size="18" font-weight="bold">Machinery Overview Control Room</text>
  <rect x="200" y="60" width="580" height="35" rx="4" fill="#7f1d1d" stroke="#f87171" />
  <text x="215" y="81" fill="#f87171" font-family="Helvetica" font-size="11" font-weight="bold">🚨 ALARM: OFF-SPEC DEVIATION | Basis Weight exceeds target by +2.00 gsm</text>
  
  <!-- Telemetry Sensor Cards -->
  <rect x="200" y="110" width="135" height="70" rx="6" fill="#1e293b" stroke="#334155" />
  <text x="215" y="130" fill="#94a3b8" font-family="Helvetica" font-size="10">Pulp Stock Flow</text>
  <text x="215" y="155" fill="#f1f5f9" font-family="Helvetica" font-size="16" font-weight="bold">450.0 m³/h</text>
  
  <rect x="345" y="110" width="135" height="70" rx="6" fill="#1e293b" stroke="#334155" />
  <text x="360" y="130" fill="#94a3b8" font-family="Helvetica" font-size="10">Dryer Steam</text>
  <text x="360" y="155" fill="#f1f5f9" font-family="Helvetica" font-size="16" font-weight="bold">4.20 bar</text>

  <rect x="490" y="110" width="135" height="70" rx="6" fill="#1e293b" stroke="#334155" />
  <text x="505" y="130" fill="#94a3b8" font-family="Helvetica" font-size="10">Machine Speed</text>
  <text x="505" y="155" fill="#f1f5f9" font-family="Helvetica" font-size="16" font-weight="bold">850.0 mpm</text>

  <rect x="635" y="110" width="145" height="70" rx="6" fill="#1e293b" stroke="#334155" />
  <text x="650" y="130" fill="#94a3b8" font-family="Helvetica" font-size="10">Scanner Weight</text>
  <text x="650" y="155" fill="#f87171" font-family="Helvetica" font-size="16" font-weight="bold">82.00 gsm</text>
  
  <!-- Left Side: Recommendation Card -->
  <rect x="200" y="200" width="370" height="180" rx="6" fill="#1e1b4b" stroke="#6366f1" />
  <text x="215" y="225" fill="#f1f5f9" font-family="Helvetica" font-size="12" font-weight="bold">💡 AI Controller Setpoint Advice</text>
  <text x="215" y="255" fill="#e2e8f0" font-family="Helvetica" font-size="10">Suggested Adjustments to regain specifications:</text>
  <text x="215" y="280" fill="#f87171" font-family="Helvetica" font-size="11" font-weight="bold">Pulp Flow: -11.0 m³/h  |  Speed: -4.2 mpm  |  Steam: +0.8 bar</text>
  
  <!-- Action Buttons -->
  <rect x="215" y="325" width="120" height="30" rx="4" fill="#064e3b" />
  <text x="275" y="344" fill="#34d399" font-family="Helvetica" font-size="11" text-anchor="middle">✔ Accept</text>
  
  <rect x="345" y="325" width="120" height="30" rx="4" fill="#7f1d1d" />
  <text x="405" y="344" fill="#f87171" font-family="Helvetica" font-size="11" text-anchor="middle">❌ Reject</text>
  
  <!-- Right Side: Risk Meter Gauge -->
  <rect x="585" y="200" width="195" height="180" rx="6" fill="#1e293b" stroke="#334155" />
  <text x="682" y="225" fill="#f1f5f9" font-family="Helvetica" font-size="12" font-weight="bold" text-anchor="middle">Deviation Risk</text>
  <path d="M 610,320 A 70,70 0 0,1 750,320" fill="none" stroke="#7f1d1d" stroke-width="20" />
  <path d="M 610,320 A 70,70 0 0,1 680,250" fill="none" stroke="#064e3b" stroke-width="20" />
  <text x="682" y="315" fill="#f87171" font-family="Helvetica" font-size="28" font-weight="bold" text-anchor="middle">88.0%</text>
  
  <!-- Lower Section: Operator Logs -->
  <rect x="200" y="395" width="580" height="85" rx="6" fill="#1e293b" stroke="#334155" />
  <text x="215" y="415" fill="#94a3b8" font-family="Helvetica" font-size="11" font-weight="bold">Action Decision Log</text>
  <text x="215" y="440" fill="#f1f5f9" font-family="Helvetica" font-size="10">15:43:29 | GRADE_A | Flow Delta: -11.0 | Action: ACCEPTED (Valves optimized)</text>
  <text x="215" y="460" fill="#f1f5f9" font-family="Helvetica" font-size="10">15:35:10 | GRADE_B | Flow Delta: +14.2 | Action: REJECTED (Speed tear limit overrides)</text>
</svg>
```

---

## 8. Recommendation Workflow
Logic loop processing control gains calculations and historical neighbor matches.

```mermaid
flowchart TD
    TelemetryIn[1. Input Current Telemetry] --> CheckDev{2. deviation == 0?}
    CheckDev -- Yes --> NoAction[3. Recommendation: No change needed]
    CheckDev -- No --> CalcStockFlow[4. Calculate Stock Flow Delta: Gain * deviation]
    
    CalcStockFlow --> ClipStockFlow[5. Clip Stock Flow to safety change limit %]
    ClipStockFlow --> CalcSpeed[6. Calculate Speed Delta: Gain * -deviation]
    CalcSpeed --> ClipSpeed[7. Clip Speed Delta to safety speed limit mpm]
    ClipSpeed --> CalcSteam[8. Calculate Dryer Steam Delta: Gain * deviation]
    CalcSteam --> ClipSteam[9. Clip Steam Delta to safety limit bar]
    
    ClipSteam --> ScanHistory[10. Run Historical Matcher: nearest neighbor search]
    ScanHistory --> GenSimilarity[11. Calculate state similarity scores]
    GenSimilarity --> CombineOutput[12. Combine recommendation adjustments + matches list]
    CombineOutput --> CompileNLP[13. Translate output to Operator explanation Card]
```
