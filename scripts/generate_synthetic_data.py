#!/usr/bin/env python
"""
Generate synthetic telemetry logs in CSV and Excel formats.
Used to validate the ingestion and preprocessing pipelines.
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_synthetic_dataframe(start_time, num_rows, base_grade="GRADE_A"):
    """Creates a simulated DataFrame containing continuous process readings."""
    timestamps = [start_time + timedelta(seconds=i*10) for i in range(num_rows)]
    
    # Base process parameters
    pulp_flow = 450.0 + np.random.normal(0, 5, num_rows)
    consistency = 3.4 + np.random.normal(0, 0.05, num_rows)
    steam_pressure = 4.2 + np.random.normal(0, 0.1, num_rows)
    machine_speed = 850.0 + np.random.normal(0, 2, num_rows)
    active_grade = [base_grade] * num_rows
    
    # Introduce some missing values (for testing cleaners)
    for idx in np.random.choice(num_rows, size=int(num_rows * 0.05), replace=False):
        pulp_flow[idx] = np.nan
    for idx in np.random.choice(num_rows, size=int(num_rows * 0.03), replace=False):
        consistency[idx] = np.nan
        
    # Introduce some outliers (for testing outlier cleaners)
    for idx in np.random.choice(num_rows, size=3, replace=False):
        pulp_flow[idx] = 9999.0  # Spiky outlier
    for idx in np.random.choice(num_rows, size=2, replace=False):
        machine_speed[idx] = -120.0  # Physical impossibility
        
    df = pd.DataFrame({
        "timestamp": timestamps,
        "pulp_flow_m3h": pulp_flow,
        "consistency_pct": consistency,
        "steam_pressure_bar": steam_pressure,
        "machine_speed_mpm": machine_speed,
        "active_grade_id": active_grade
    })
    
    return df

def generate_data():
    raw_dir = os.path.join("data", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    
    start_time = datetime(2026, 7, 26, 12, 0, 0)
    
    # 1. File 1: CSV dataset (GRADE_A)
    print("Generating synthetic CSV log 1...")
    df1 = create_synthetic_dataframe(start_time, 100, "GRADE_A")
    df1.to_csv(os.path.join(raw_dir, "history_log_1.csv"), index=False)
    
    # 2. File 2: Excel dataset (GRADE_B)
    print("Generating synthetic Excel log 2...")
    df2 = create_synthetic_dataframe(start_time + timedelta(seconds=1000), 100, "GRADE_B")
    excel_path = os.path.join(raw_dir, "history_log_2.xlsx")
    try:
        df2.to_excel(excel_path, index=False)
    except ModuleNotFoundError:
        print("[WARNING] openpyxl not installed. Installing dynamically to write Excel...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])
        df2.to_excel(excel_path, index=False)
        
    # 3. File 3: CSV dataset (GRADE_C)
    print("Generating synthetic CSV log 3...")
    df3 = create_synthetic_dataframe(start_time + timedelta(seconds=2000), 100, "GRADE_C")
    df3.to_csv(os.path.join(raw_dir, "history_log_3.csv"), index=False)
    
    print("Synthetic datasets generated in data/raw/")

if __name__ == "__main__":
    generate_data()
