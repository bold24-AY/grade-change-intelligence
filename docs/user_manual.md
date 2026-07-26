# Operator User Manual - Grade Change Intelligence

This manual explains how control room operators use the Grade Change Command Center to monitor paper machine grade transitions, review ML anomaly forecasts, and apply setpoint adjustments.

---

## 🖥 Dashboard Interface Sections

The Streamlit dashboard interface is split into 7 primary pages:

### 1. Overview Page
- **Machinery Cards**: Monitor current Pulp Flow, Slurry Consistency, Steam Pressure, and Reel Speed.
- **Specification Banner**: Indicates whether the measured basis weight falls within the grade's tolerance band.
- **Alarm Status**: If the basis weight deviates outside limits, a red `🚨 ALARM: OFF SPEC` badge flashes. If within limits, a green `🟢 ON SPECIFICATION` badge is shown.

### 2. Prediction Page
- **Risk Meter**: Shows the model-forecasted probability (%) of an upcoming or current off-spec deviation.
- **Causal Justification (SHAP)**: Explains the exact mechanical reasoning (the "Why") behind the prediction.
- **Drivers Chart**: Visualizes the top 5 process variables influencing the risk probability.

### 3. Analytics Page
- **Telemetry Trends**: View interactive line charts of any sensor over the last 10 minutes.
- **Cross-Correlations Heatmap**: Highlights which sensors are moving together to help identify root causes.

### 4. Recommendations Page
- **Setpoint Recommendations**: Displays suggested controller changes (e.g., `-11.0 m³/h` stock flow change).
- **Operator Notes**: Presets loaded from specifications with operator advice.
- **Control Interface**: Operators can click **Accept** or **Reject** to log actions.

### 5. Historical Cases Page
- **Nearest Neighbors**: Lists historical run timestamps that closely match the current machine state, along with the action deltas that resolved those deviations.

### 6. Reports Page
- **PDF Exporter**: Compile and download a formal PDF process report listing telemetry, predictions, and logged operator decisions.

### 7. Settings Page
- **Simulator**: Move sliders to adjust simulated telemetry readings (pulp flow, speed, consistency, steam, and weight) to see how the recommendations and XAI model respond.

---

## 🚨 Operator Action Protocols

When an `OFF-SPEC ALARM` triggers:
1.  Navigate to the **Prediction Page** to evaluate the risk probability and the SHAP drivers.
2.  Review the **Recommendations Page** to see the suggested actuator changes (e.g., reducing thick stock pulp flow).
3.  Cross-reference the **Historical Cases Page** to confirm if similar adjustments resolved similar past events.
4.  Apply recommendations on the DCS control panel and click **Accept** on the dashboard.
5.  At the end of the shift, navigate to the **Reports Page** and export the action log as a PDF report.
