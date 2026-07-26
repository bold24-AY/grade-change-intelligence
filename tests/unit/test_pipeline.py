import os
import shutil
import pytest
import pandas as pd
import numpy as np
from backend.app.pipeline.loader import DataLoader
from backend.app.pipeline.cleaner import DataCleaner
from backend.app.pipeline.features import FeatureEngineer
from backend.app.pipeline.processor import DataProcessor
from backend.app.pipeline.validator import DataValidator
from backend.app.pipeline.versioner import DataVersioner

@pytest.fixture
def sample_raw_dataframe():
    """Provides a sample raw dataframe containing missing values and outliers."""
    return pd.DataFrame({
        "timestamp": pd.date_range(start="2026-07-26 12:00:00", periods=5, freq="10S"),
        "pulp_flow_m3h": [450.0, np.nan, 460.0, 9999.0, 440.0],  # NaN and Outlier
        "consistency_pct": [3.4, 3.5, np.nan, 3.3, 3.4],        # NaN
        "steam_pressure_bar": [4.2, 4.3, 4.2, 4.1, 4.2],
        "machine_speed_mpm": [850.0, 850.0, -120.0, 848.0, 850.0],  # Outlier (negative speed)
        "basis_weight_gsm": [80.0, 80.5, 79.5, 80.2, 80.1],
        "basis_weight_dev": [0.0, 0.5, -0.5, 0.2, 0.1],
        "is_basis_weight_off_spec": [0, 0, 0, 0, 0],
        "active_grade_id": ["GRADE_A", "GRADE_A", "GRADE_A", "GRADE_B", "GRADE_B"]
    })


def test_loader_csv_parsing(tmp_path, sample_raw_dataframe):
    """Verify that DataLoader can parse CSV files."""
    csv_file = tmp_path / "test_data.csv"
    sample_raw_dataframe.to_csv(csv_file, index=False)
    
    loader = DataLoader()
    loaded_df = loader.load_single_file(str(csv_file))
    
    assert len(loaded_df) == 5
    assert "pulp_flow_m3h" in loaded_df.columns

def test_cleaner_missing_imputation(sample_raw_dataframe):
    """Verify cleaner forward-fills missing values."""
    cleaner = DataCleaner()
    cleaned = cleaner.impute_missing(sample_raw_dataframe)
    
    # Assert missing values are imputed
    assert not cleaned["pulp_flow_m3h"].isnull().any()
    assert not cleaned["consistency_pct"].isnull().any()
    # The second element was NaN, should forward-fill from first (450.0)
    assert cleaned["pulp_flow_m3h"].iloc[1] == 450.0

def test_cleaner_outlier_clipping(sample_raw_dataframe):
    """Verify cleaner clips outliers correctly."""
    cleaner = DataCleaner(target_cols=["pulp_flow_m3h", "machine_speed_mpm"])
    # Standard Z-score outlier clipping
    clipped = cleaner.handle_outliers_zscore(sample_raw_dataframe, threshold=1.0, action="clip")
    
    # Assert outlier (9999.0) is clipped to standard boundary value
    assert clipped["pulp_flow_m3h"].max() < 9000.0

def test_feature_engineering_calculations(sample_raw_dataframe):
    """Verify FeatureEngineer appends rolling windows, lags, and diff columns."""
    # Clean data first so window functions don't propagate NaNs
    cleaner = DataCleaner()
    cleaned = cleaner.impute_missing(sample_raw_dataframe)
    
    engineer = FeatureEngineer(window_sizes=[2])
    featured = engineer.construct_all_features(cleaned)
    
    assert "pulp_flow_m3h_roll_mean_2" in featured.columns
    assert "pulp_flow_m3h_diff_1m" in featured.columns
    assert "pulp_flow_m3h_lag_1" in featured.columns

def test_processor_standardization_and_encoding(sample_raw_dataframe):
    """Verify DataProcessor standardizes numeric variables and encodes labels."""
    processor = DataProcessor()
    
    # Clean NaNs
    cleaner = DataCleaner()
    cleaned = cleaner.impute_missing(sample_raw_dataframe)
    
    # Fit and transform scaling
    processor.fit_standardize(cleaned)
    scaled = processor.transform_standardize(cleaned)
    
    # Mean of standardized values should be close to 0
    assert abs(scaled["pulp_flow_m3h"].mean()) < 1e-6
    
    # Label encoding
    processor.fit_label_encode(cleaned)
    encoded = processor.transform_label_encode(cleaned)
    assert encoded["active_grade_id"].iloc[0] == 0
    assert encoded["active_grade_id"].iloc[3] == 1

def test_validator_schema_checks(sample_raw_dataframe):
    """Verify DataValidator catches boundary and schema errors."""
    validator = DataValidator()
    
    # Schema should match required columns
    ok, errors = validator.validate_schema(sample_raw_dataframe)
    assert ok is True
    
    # Should catch negative machine speed boundary violation
    ok_bounds, boundary_errors = validator.validate_logical_boundaries(sample_raw_dataframe)
    assert ok_bounds is False
    assert any("machine_speed_mpm" in err for err in boundary_errors)

def test_versioner_manifest_writing(tmp_path, sample_raw_dataframe):
    """Verify DataVersioner outputs manifest descriptors files."""
    versioner = DataVersioner(manifest_dir=str(tmp_path))
    manifest_info = versioner.register_version(sample_raw_dataframe, "test_dataset")
    
    assert os.path.exists(tmp_path / "version_manifest.json")
    assert manifest_info["row_count"] == 5
    assert manifest_info["dataset_name"] == "test_dataset"
