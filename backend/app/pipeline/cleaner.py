import pandas as pd
import numpy as np
from typing import List

class DataCleaner:
    """
    Cleans raw industrial telemetry data by imputing missing values
    and handling outliers.
    """
    
    def __init__(self, target_cols: List[str] = None):
        self.target_cols = target_cols or ["pulp_flow_m3h", "consistency_pct", "steam_pressure_bar", "machine_speed_mpm"]
        
    def impute_missing(self, df: pd.DataFrame, method: str = "ffill") -> pd.DataFrame:
        """
        Imputes missing values.
        Suitable for time-series streams: forward-fill values from last valid state,
        then backward-fill any remaining NaNs at the beginning.
        """
        cleaned_df = df.copy()
        if method == "ffill":
            cleaned_df[self.target_cols] = cleaned_df[self.target_cols].ffill().bfill()
        elif method == "median":
            for col in self.target_cols:
                median_val = cleaned_df[col].median()
                cleaned_df[col] = cleaned_df[col].fillna(median_val)
        else:
            raise ValueError(f"Imputation method not supported: {method}")
            
        return cleaned_df
        
    def handle_outliers_zscore(self, df: pd.DataFrame, threshold: float = 3.0, action: str = "clip") -> pd.DataFrame:
        """
        Detects outliers using standard Z-score (deviation from column mean).
        Actions:
          - 'clip': replace outliers with boundary limits (mean +/- threshold*std)
          - 'nan': replace outliers with NaN (to be filled by cleaner imputation)
        """
        cleaned_df = df.copy()
        for col in self.target_cols:
            if col not in cleaned_df.columns:
                continue
                
            mean = cleaned_df[col].mean()
            std = cleaned_df[col].std()
            
            # Avoid division by zero
            if std == 0:
                continue
                
            z_scores = (cleaned_df[col] - mean) / std
            
            if action == "clip":
                lower_limit = mean - threshold * std
                upper_limit = mean + threshold * std
                cleaned_df[col] = np.clip(cleaned_df[col], lower_limit, upper_limit)
            elif action == "nan":
                cleaned_df.loc[np.abs(z_scores) > threshold, col] = np.nan
            else:
                raise ValueError(f"Outlier action not supported: {action}")
                
        return cleaned_df

    def handle_outliers_iqr(self, df: pd.DataFrame, factor: float = 1.5, action: str = "clip") -> pd.DataFrame:
        """
        Detects outliers using Interquartile Range (IQR).
        """
        cleaned_df = df.copy()
        for col in self.target_cols:
            if col not in cleaned_df.columns:
                continue
                
            q25 = cleaned_df[col].quantile(0.25)
            q75 = cleaned_df[col].quantile(0.75)
            iqr = q75 - q25
            
            lower_limit = q25 - factor * iqr
            upper_limit = q75 + factor * iqr
            
            if action == "clip":
                cleaned_df[col] = np.clip(cleaned_df[col], lower_limit, upper_limit)
            elif action == "nan":
                outliers = (cleaned_df[col] < lower_limit) | (cleaned_df[col] > upper_limit)
                cleaned_df.loc[outliers, col] = np.nan
            else:
                raise ValueError(f"Outlier action not supported: {action}")
                
        return cleaned_df
