import pandas as pd
import numpy as np
from typing import List, Dict

class DataProcessor:
    """
    Handles normalization, scaling, and categorical variable encoding.
    Utilizes stateful custom scaling methods resembling scikit-learn transformers.
    """
    
    def __init__(self, numeric_cols: List[str] = None, categorical_cols: List[str] = None):
        self.numeric_cols = numeric_cols or ["pulp_flow_m3h", "consistency_pct", "steam_pressure_bar", "machine_speed_mpm"]
        self.categorical_cols = categorical_cols or ["active_grade_id"]
        self.scaling_params: Dict[str, Dict[str, float]] = {}
        self.label_mappings: Dict[str, Dict[str, int]] = {}
        
    def fit_minmax(self, df: pd.DataFrame) -> None:
        """Saves min and max limits for normalization."""
        for col in self.numeric_cols:
            if col in df.columns:
                self.scaling_params[col] = {
                    "min": float(df[col].min()),
                    "max": float(df[col].max())
                }
                
    def transform_minmax(self, df: pd.DataFrame) -> pd.DataFrame:
        """Scales numeric values to [0, 1] range using fit parameters."""
        scaled_df = df.copy()
        for col in self.numeric_cols:
            if col not in scaled_df.columns or col not in self.scaling_params:
                continue
            params = self.scaling_params[col]
            denom = params["max"] - params["min"]
            if denom == 0:
                scaled_df[col] = 0.0
            else:
                scaled_df[col] = ((scaled_df[col] - params["min"]) / denom).round(6)
        return scaled_df

    def fit_standardize(self, df: pd.DataFrame) -> None:
        """Saves mean and standard deviation for standardization."""
        for col in self.numeric_cols:
            if col in df.columns:
                self.scaling_params[col] = {
                    "mean": float(df[col].mean()),
                    "std": float(df[col].std())
                }
                
    def transform_standardize(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardizes numeric values (Z-score scaling)."""
        scaled_df = df.copy()
        for col in self.numeric_cols:
            if col not in scaled_df.columns or col not in self.scaling_params:
                continue
            params = self.scaling_params[col]
            std = params["std"]
            if std == 0:
                scaled_df[col] = 0.0
            else:
                scaled_df[col] = ((scaled_df[col] - params["mean"]) / std).round(6)
        return scaled_df

    def fit_label_encode(self, df: pd.DataFrame) -> None:
        """Creates unique integer mapping for categorical variables."""
        for col in self.categorical_cols:
            if col in df.columns:
                # Find unique, sort them, map to integers
                unique_vals = sorted(df[col].dropna().unique())
                self.label_mappings[col] = {val: idx for idx, val in enumerate(unique_vals)}
                
    def transform_label_encode(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applies label encoding mapping. Unseen categories default to -1."""
        encoded_df = df.copy()
        for col in self.categorical_cols:
            if col not in encoded_df.columns or col not in self.label_mappings:
                continue
            mapping = self.label_mappings[col]
            encoded_df[col] = encoded_df[col].map(mapping).fillna(-1).astype(int)
        return encoded_df

    def transform_one_hot(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applies standard one-hot encoding on categorical variables."""
        # Wrap pandas get_dummies
        return pd.get_dummies(df, columns=self.categorical_cols, drop_first=True)
