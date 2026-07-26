import pandas as pd
from typing import List, Tuple, Dict

class DataValidator:
    """
    Validates process telemetry dataframes for schema conformance,
    missing structure, and extreme value violations.
    """
    
    REQUIRED_COLUMNS = [
        "timestamp", 
        "pulp_flow_m3h", 
        "consistency_pct", 
        "steam_pressure_bar", 
        "machine_speed_mpm", 
        "active_grade_id"
    ]
    
    # Boundary logic for physical process limits
    LIMITS = {
        "pulp_flow_m3h": {"min": 0.0, "max": 2000.0},
        "consistency_pct": {"min": 0.0, "max": 10.0},
        "steam_pressure_bar": {"min": 0.0, "max": 15.0},
        "machine_speed_mpm": {"min": 0.0, "max": 2500.0}
    }
    
    def validate_schema(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Verifies if all required columns are present in the DataFrame."""
        errors = []
        missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            errors.append(f"Missing required columns in dataset: {missing_cols}")
            
        return len(errors) == 0, errors
        
    def validate_types(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Validates that columns match expected types."""
        errors = []
        
        # Verify timestamp can be parsed
        if "timestamp" in df.columns:
            try:
                pd.to_datetime(df["timestamp"])
            except Exception:
                errors.append("Column 'timestamp' contains values that cannot be parsed as datetimes.")
                
        # Verify numeric columns are float/int
        numeric_cols = ["pulp_flow_m3h", "consistency_pct", "steam_pressure_bar", "machine_speed_mpm"]
        for col in numeric_cols:
            if col in df.columns:
                if not pd.api.types.is_numeric_dtype(df[col]):
                    errors.append(f"Column '{col}' is not numeric. Type: {df[col].dtype}")
                    
        return len(errors) == 0, errors
        
    def validate_logical_boundaries(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Checks for values exceeding absolute physical limitations (e.g. negative speeds)."""
        errors = []
        for col, bounds in self.LIMITS.items():
            if col in df.columns:
                out_of_bounds = df[(df[col] < bounds["min"]) | (df[col] > bounds["max"])]
                if not out_of_bounds.empty:
                    count = len(out_of_bounds)
                    errors.append(
                        f"Column '{col}' contains {count} values violating boundary threshold "
                        f"[{bounds['min']}, {bounds['max']}]."
                    )
                    
        return len(errors) == 0, errors

    def validate_all(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Runs all checks in sequence."""
        all_errors = []
        
        ok_schema, schema_errs = self.validate_schema(df)
        all_errors.extend(schema_errs)
        
        if ok_schema:
            _, type_errs = self.validate_types(df)
            all_errors.extend(type_errs)
            
            _, boundary_errs = self.validate_logical_boundaries(df)
            all_errors.extend(boundary_errs)
            
        return len(all_errors) == 0, all_errors
