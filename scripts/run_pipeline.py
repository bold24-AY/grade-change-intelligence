#!/usr/bin/env python
"""
Grade Change Intelligence Pipeline Runner.
Loads configuration, reads raw sensor readings, processes them, and writes engineered features.
"""

import os
import sys
import yaml
import pandas as pd
import numpy as np

# Add project root to path to resolve any backend imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_config(config_path="config.yaml"):
    """Load system configuration from YAML."""
    if not os.path.exists(config_path):
        print(f"[WARNING] Config file not found at {config_path}, using defaults.")
        return {
            "data": {
                "raw_sensor_path": "data/raw/sensor_readings_sample.csv",
                "processed_features_path": "data/processed/engineered_features_sample.csv"
            }
        }
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def run_pipeline():
    """Runs the feature engineering pipeline."""
    print("Initializing Grade Change Data Pipeline...")
    config = load_config()
    
    raw_path = config["data"]["raw_sensor_path"]
    processed_path = config["data"]["processed_features_path"]
    
    if not os.path.exists(raw_path):
        print(f"[ERROR] Raw data file not found at: {raw_path}")
        sys.exit(1)
        
    print(f"Reading raw telemetry from: {raw_path}")
    df = pd.read_csv(raw_path)
    
    # Feature engineering simulation (SRP: compute rolling metrics)
    print("Calculating rolling averages and sensor gradients...")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    
    # Pulp flow rolling mean
    df['pulp_flow_roll_mean_5m'] = df['pulp_flow_m3h'].rolling(window=3, min_periods=1).mean().round(2)
    # Consistency gradient (difference)
    df['consistency_grad_1m'] = df['consistency_pct'].diff().fillna(0.0).round(4)
    # Steam pressure variance
    df['steam_pressure_roll_var_5m'] = df['steam_pressure_bar'].rolling(window=3, min_periods=1).var().fillna(0.0).round(5)
    # Speed differential
    df['machine_speed_diff_1m'] = df['machine_speed_mpm'].diff().fillna(0.0).round(2)
    
    # Simple transition thresholding rule (For demo/mocking transitions)
    # Transitions occur when machine speed differs or active grade contains 'TRANSITION'
    df['is_transitioning'] = df['active_grade_id'].apply(
        lambda x: 1 if 'TRANSITION' in str(x) else 0
    )
    
    # Select columns to save
    output_cols = [
        'timestamp', 
        'pulp_flow_roll_mean_5m', 
        'consistency_grad_1m', 
        'steam_pressure_roll_var_5m', 
        'machine_speed_diff_1m', 
        'is_transitioning'
    ]
    processed_df = df[output_cols]
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    
    print(f"Writing engineered features to: {processed_path}")
    processed_df.to_csv(processed_path, index=False)
    print("Pipeline run completed successfully!")

if __name__ == "__main__":
    run_pipeline()
    sys.exit(0)
