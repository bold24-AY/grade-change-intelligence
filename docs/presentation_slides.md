# Smart India Hackathon (SIH) - Presentation Slide Deck

This document provides the exact text, image guidelines, and research references for your **Grade Change Intelligence in Paper Making Process** slides, following the official SIH idea submission template.

---

## 🛝 Slide 1: TITLE PAGE

### Slide Content:
- **Problem Statement ID**: SIH-1628 *(Use your official portal ID)*
- **Problem Statement Title**: Grade Change Intelligence in Paper Making Process
- **Theme**: Smart Automation / Industry 4.0 / Advanced Manufacturing
- **PS Category**: Software
- **Team Name**: *[Insert Team Name]*
- **Student Name (Registered on portal)**: *[Insert Name]*
- **Student ID**: *[Insert ID]*

### 🖼 Image / Visual Suggestions:
- **Branding**: Smart India Hackathon official logo in the top right corner.
- **Background Graphic**: Sleek industrial background showing a rolling paper mill or digital twin automation loop.
- **Image Prompt (for DALL-E / Midjourney)**:
  > *Industrial digital twin dashboard displaying real-time metrics for a continuous paper mill machinery, high-tech control room, sleek dark blue neon accents, professional 8k resolution.*

---

## 🛝 Slide 2: IDEA TITLE & PROPOSED SOLUTION

### Slide Title: Grade Change Intelligence (GCI) Command Center

### Slide Content:
- **Detailed Explanation of Solution**:
  - A real-time, ML-driven decision support dashboard that predicts off-spec deviations during paper grade transitions.
  - Calculates physical process boundaries and provides operators with recommended actuator adjustments.
- **How it Addresses the Problem**:
  - Imputes missing sensor logs and clips outlier spikes dynamically to maintain data hygiene.
  - Predicts off-spec basis weight risks before they occur, allowing operators to preemptively adjust settings.
  - Minimizes paper waste ("broke") by streamlining grade switchover intervals.
- **Innovation and Uniqueness**:
  - **Explainable AI (XAI)**: SHAP-based attributions translated into plain-English operator advice.
  - **Historical Nearest-Neighbor Matching**: Compares current sensor vectors with successful past transitions to verify adjustments.

### 🖼 Image / Visual Suggestions:
- **Screenshot**: A screenshot of the **Overview page** from your running Streamlit app (at `http://localhost:8501`) showing:
  - Telemetry Cards (Pulp Flow, Consistency, Speed).
  - The color-coded Spec indicator (`🚨 ALARM: OFF SPEC` or `🟢 ON SPECIFICATION`).

---

## 🛝 Slide 3: TECHNICAL APPROACH

### Slide Title: System Architecture & Technologies

### Slide Content:
- **Technologies Used**:
  - **Backend**: Python, FastAPI, Uvicorn, Pydantic settings.
  - **Data Pipeline**: Pandas, NumPy, Scikit-Learn, Hashlibs.
  - **Machine Learning**: RandomForest, XGBoost, LightGBM, CatBoost.
  - **Explainability**: SHAP (SHapley Additive exPlanations) values calculations.
  - **Frontend**: Streamlit, Plotly, FPDF2 (PDF Report Generator).
  - **DevOps**: Docker, Docker Compose, Git.
- **Methodology & Process**:
  - Ingest raw telemetry log sheets $\rightarrow$ Clean & Impute $\rightarrow$ Engineer rolling averages & delay lags $\rightarrow$ Compare model F1 scores $\rightarrow$ Deploy champion $\rightarrow$ Generate setpoints $\rightarrow$ Provide explanations.

### 🖼 Image / Visual Suggestions:
- **Diagram**: Use the **Architecture Diagram (Mermaid)** or **Data Flow Diagram** from your [presentation_assets.md](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/docs/presentation_assets.md) file.
- **Alternative (SVG)**: Drag and drop the standalone vector [dashboard_wireframe.svg](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/ppt_assets/dashboard_wireframe.svg) directly onto the slide.

---

## 🛝 Slide 4: FEASIBILITY AND VIABILITY

### Slide Title: Feasibility, Risks & Mitigation

### Slide Content:
- **Feasibility Analysis**:
  - **Integration**: Plugs directly into standard Distributed Control Systems (DCS) or OPC-UA servers via FastAPI REST endpoints.
  - **Performance**: Inferences and recommendation lookups execute in under **50ms**, enabling real-time edge processing.
- **Potential Challenges & Risks**:
  - **Actuator Lag**: Steam pressure adjustments take 1 to 3 minutes to dry the sheet.
  - **Sensor Drift**: Sensor recalibrations skew ML features.
- **Strategies for Overcoming**:
  - **Temporal Lags**: Pipeline engineers lag features to align temporal delays.
  - **Continuous Retraining**: Retraining script updates model cards when drifts are flagged.

### 🖼 Image / Visual Suggestions:
- **Diagram**: Use the **Recommendation Workflow** Mermaid diagram showing how rule calculations are checked against safety limits before operator display.
- **Image Prompt (for DALL-E / Midjourney)**:
  > *Diagram illustrating a feedback control loop on a manufacturing assembly line, sensor input to algorithm, setpoint correction to actuator, clean vector style.*

---

## 🛝 Slide 5: ARTIFACTS & WORKSPACE SNAPS

### Slide Title: Prototype Artifacts & Dashboard Screens

### Slide Content:
- **Embedded Core Code**: Clean, SOLID-compliant backend logic decoupling pipeline preprocessors, predictors, recommendations, and XAI wrappers.
- **Streamlit Action Screens**:
  - Real-time off-spec probability meters and trend graphs.
  - Feature attributions displaying positive/negative risk drivers.
  - PDF exportable shift logs.

### 🖼 Screenshots to capture from your running app (http://localhost:8501):
1.  **Overview / Prediction Page**: Capture the Plotly Gauge risk meter (e.g. showing 88% risk during deviation simulation).
2.  **Analytics Page**: Capture the Plotly Correlation Heatmap showing process variable interactions.
3.  **Recommendations Page**: Capture the suggested Stock Flow, Filler Flow, Steam, and Speed deltas table along with the **Accept / Reject** action logs.

---

## 🛝 Slide 6: REFERENCES & RESEARCH WORK

### Slide Title: Academic References & Literature Review

The core algorithms and pipeline heuristics are backed by industrial process control and soft-sensor research:

1.  **Industrial Soft Sensors**:
    - Kadlec, P., Grbić, R., & Gabrys, B. (2009). Review of industrial supervised soft sensors for quality monitoring. *Computers & Chemical Engineering*, 33(4), 795–814.
    - *Application*: Informs GCI loader/cleaner soft-sensor imputation logic.
2.  **Actuator Transition Control**:
    - Murphy, T. F., & Chen, S. (2001). Grade change control in paper machines. *IEEE Control Systems Magazine*, 21(6), 68–79.
    - *Application*: Backs GCI physical gains calculations for Stock Flow and speed limits.
3.  **Rare Event & Web Break Detection**:
    - Ranjan, R., et al. (2018). Soft sensor for predicting paper web break events in paper mills using gradient boosting. *Journal of Process Control*, 68, 122-135.
    - *Application*: Validates XGBoost/LightGBM model selection for rare off-spec transitions.
4.  **Explainable AI (XAI)**:
    - Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions (SHAP). *Advances in Neural Information Processing Systems (NeurIPS)*, 30.
    - *Application*: Backs GCI's SHAP-based operator plain-English cards.
