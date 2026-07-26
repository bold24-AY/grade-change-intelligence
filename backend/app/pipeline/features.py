import pandas as pd
from typing import List

class FeatureEngineer:
    """
    Constructs rolling variables, lags, and rate-of-change metrics
    from paper machine time-series telemetry.
    """
    
    def __init__(self, target_cols: List[str] = None, window_sizes: List[int] = None):
        self.target_cols = target_cols or ["pulp_flow_m3h", "consistency_pct", "steam_pressure_bar", "machine_speed_mpm"]
        self.window_sizes = window_sizes or [3, 5]
        
    def add_rolling_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculates rolling means, standard deviations, and variances."""
        featured_df = df.copy()
        
        # Ensure data is sorted by timestamp before windowing
        if "timestamp" in featured_df.columns:
            featured_df = featured_df.sort_values("timestamp")
            
        for col in self.target_cols:
            if col not in featured_df.columns:
                continue
            for window in self.window_sizes:
                # Rolling Mean
                featured_df[f"{col}_roll_mean_{window}"] = (
                    featured_df[col].rolling(window=window, min_periods=1).mean().round(4)
                )
                # Rolling Std Dev
                featured_df[f"{col}_roll_std_{window}"] = (
                    featured_df[col].rolling(window=window, min_periods=1).std().fillna(0.0).round(4)
                )
                
        return featured_df
        
    def add_derivatives(self, df: pd.DataFrame) -> pd.DataFrame:
        """Computes rate of change (first-order differences) for telemetry."""
        featured_df = df.copy()
        for col in self.target_cols:
            if col not in featured_df.columns:
                continue
            featured_df[f"{col}_diff_1m"] = featured_df[col].diff().fillna(0.0).round(4)
        return featured_df
        
    def add_lags(self, df: pd.DataFrame, lag_steps: int = 2) -> pd.DataFrame:
        """Adds temporal delay lag steps to capture actuator lag response delays."""
        featured_df = df.copy()
        for col in self.target_cols:
            if col not in featured_df.columns:
                continue
            for lag in range(1, lag_steps + 1):
                featured_df[f"{col}_lag_{lag}"] = featured_df[col].shift(periods=lag).bfill().round(4)

        return featured_df
        
    def construct_all_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applies rolling calculations, derivatives, and lags in sequence."""
        df_roll = self.add_rolling_features(df)
        df_diff = self.add_derivatives(df_roll)
        df_lag = self.add_lags(df_diff)
        return df_lag
