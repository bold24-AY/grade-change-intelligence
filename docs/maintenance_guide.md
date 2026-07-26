# Maintenance Guide - Grade Change Intelligence

This guide outlines routine tasks for maintaining the Grade Change Intelligence system in production, ensuring model accuracy, clean data flows, and log rotations.

---

## 🪵 1. Log Management

Logs are recorded in two locations:
1.  **Console (stdout)**: Captured by Docker containers or system services.
2.  **Log File**: Saved at `logs/app.log` by default.

### Log Rotation & Retention
Log rotation parameters are configured in **[config.yaml](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/config.yaml)**:
- **`rotation`**: `10 MB` (automatically rolls over to a new log file when it hits 10MB).
- **`retention`**: `1 week` (purges log files older than a week to conserve disk space).

If logs are filling up too fast, update the log level in `config.yaml` from `DEBUG` to `WARNING`.

---

## 🔄 2. Model Retraining Protocol

Over time, paper machine parameters can shift due to wear, nozzle erosion, or sensor drifts. The classifier models should be retrained periodically (e.g., monthly).

### Retraining Cycle:
1.  **Ingest New Data**: Place the new historical DCS logs (CSV/Excel format) inside `data/raw/`.
2.  **Process Features**: Run the pipeline to clean values and engineer lag metrics:
    ```cmd
    venv\Scripts\python scripts/run_pipeline.py
    ```
    This updates [engineered_features_sample.csv](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/data/processed/engineered_features_sample.csv).
3.  **Run Comparative Selector**: Run the training script:
    ```cmd
    venv\Scripts\python scripts/train_pipeline.py
    ```
    The training engine will fit all candidates, compare validation F1 scores, register the new champion in `model_registry.json`, and overwrite `basis_weight_deviation_champion.joblib`.
4.  **Restart Services**: Uvicorn and Streamlit will automatically pick up the new model card from the registry.

---

## 📂 3. Data Manifest and Hashes

- The `version_manifest.json` inside `data/processed/` registers cryptographic hashes (SHA-256) of every processed dataset version.
- **Never edit this file manually.** If data is corrupted, clear the processed directory and rerun `run_pipeline.py` to re-register the manifest.

---

## 🛠 4. Troubleshooting Guide

### Issue: "Input y contains NaN" during retraining
- **Cause**: Some raw log files do not contain basis weight columns, or target columns contain empty rows.
- **Solution**: The training script automatically drops rows where target values are missing. Verify that raw logs contain columns named `basis_weight_gsm` and `is_basis_weight_off_spec`.

### Issue: "Model file not found" on startup
- **Cause**: The API started before the models were trained.
- **Solution**: Run `venv\Scripts\python scripts/train_pipeline.py` first to generate the champion binary checkpoint.
