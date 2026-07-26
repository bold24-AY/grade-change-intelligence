#!/usr/bin/env python
"""
Grade Change Intelligence Pipeline Runner.
Orchestrates loading raw CSV/Excel telemetry log files, cleaning data,
generating statistical time-series features, validating values, and versioning.
"""

import os
import sys
import pandas as pd
from loguru import logger

# Add project root to path to resolve backend modules
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from backend.app.pipeline.loader import DataLoader
from backend.app.pipeline.cleaner import DataCleaner
from backend.app.pipeline.features import FeatureEngineer
from backend.app.pipeline.processor import DataProcessor
from backend.app.pipeline.validator import DataValidator
from backend.app.pipeline.versioner import DataVersioner
from backend.app.core.config import settings

def run_end_to_end_pipeline():
    logger.info("Initializing Grade Change Intelligence Data Pipeline...")
    
    # 1. Scans and loads files
    raw_dir = os.path.join(PROJECT_ROOT, "data", "raw")
    logger.info(f"Scanning raw telemetry files in: {raw_dir}")
    
    loader = DataLoader()
    raw_df = loader.scan_and_load_directory(raw_dir)
    
    if raw_df.empty:
        logger.error("No telemetry data found in raw directory. Aborting pipeline execution.")
        sys.exit(1)
        
    logger.info(f"Successfully loaded and merged {len(raw_df)} raw process readings.")
    
    # 2. Structural Data Validation
    logger.info("Running schema and data type validation checks...")
    validator = DataValidator()
    
    ok_schema, schema_errs = validator.validate_schema(raw_df)
    if not ok_schema:
        logger.error(f"Schema validation failed: {schema_errs}")
        sys.exit(1)
        
    _, type_errs = validator.validate_types(raw_df)
    if type_errs:
        for err in type_errs:
            logger.warning(err)
            
    # Check boundaries and print violations before cleaning
    _, bounds_errs = validator.validate_logical_boundaries(raw_df)
    if bounds_errs:
        logger.warning(f"Process boundary anomalies detected before cleaning: {len(bounds_errs)} columns violated bounds.")
        for err in bounds_errs:
            logger.debug(err)
            
    # 3. Clean Missing Values & Outliers
    logger.info("Cleaning process telemetry...")
    cleaner = DataCleaner()
    
    # Impute missing values (ffill then bfill suitable for time-series streams)
    imputed_df = cleaner.impute_missing(raw_df)
    
    # Clip extreme sensor spikes/noise (rolling Z-score bounds clipping)
    logger.info("Clipping process sensor noise outliers...")
    clean_df = cleaner.handle_outliers_zscore(imputed_df, threshold=3.0, action="clip")
    
    # 4. Feature Engineering
    logger.info("Engineering rolling averages, rate-of-change derivatives, and actuator lag offsets...")
    engineer = FeatureEngineer(window_sizes=[3, 5])
    featured_df = engineer.construct_all_features(clean_df)
    
    # 5. Feature Normalization and Label Encoding
    logger.info("Normalizing features and encoding grade labels...")
    # Gather engineered numeric columns
    numeric_cols = [col for col in featured_df.columns if col not in ["timestamp", "active_grade_id"]]
    processor = DataProcessor(numeric_cols=numeric_cols, categorical_cols=["active_grade_id"])
    
    # Fit stats and scale
    processor.fit_standardize(featured_df)
    scaled_df = processor.transform_standardize(featured_df)
    
    # Encode active grade IDs
    processor.fit_label_encode(scaled_df)
    final_df = processor.transform_label_encode(scaled_df)
    
    # 6. Post-processing Validation
    logger.info("Validating clean, processed features dataframe...")
    ok_final, final_errs = validator.validate_types(final_df)
    if not ok_final:
        logger.error(f"Processed feature validation failed: {final_errs}")
        sys.exit(1)
        
    # 7. Dataset Versioning & Registration
    logger.info("Hashing processed features and registering version manifest...")
    versioner = DataVersioner(manifest_dir=os.path.join(PROJECT_ROOT, "data", "processed"))
    version_manifest = versioner.register_version(final_df, "grade_change_engineered_features")
    
    logger.info(f"Registered version: {version_manifest['version_tag']} | Hash: {version_manifest['sha256_hash'][:12]}")
    
    # 8. Save Processed Dataset
    processed_path = os.path.join(PROJECT_ROOT, settings.PROCESSED_FEATURES_PATH)
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    final_df.to_csv(processed_path, index=False)
    
    logger.info(f"Processed features saved successfully to: {processed_path}")
    logger.info(f"Data pipeline run completed successfully. Total processed rows: {len(final_df)}")

if __name__ == "__main__":
    # Configure logger output to console
    logger.remove()
    logger.add(sys.stdout, level="INFO", colorize=True)
    
    run_end_to_end_pipeline()
    sys.exit(0)
