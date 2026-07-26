#!/usr/bin/env python
"""
Basis Weight Deviation ML Pipeline Trainer.
Loads processed features, trains RandomForest, XGBoost, LightGBM, and CatBoost,
compares metrics, and registers the best classifier.
"""

import os
import sys
import pandas as pd
from loguru import logger

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from backend.app.ml.trainer import MLTrainer
from backend.app.ml.registry import ModelRegistry
from backend.app.core.config import settings

def run_model_training():
    logger.info("Initializing ML Model Selection & Training Pipeline...")
    
    # 1. Load processed features
    processed_path = os.path.join(PROJECT_ROOT, settings.PROCESSED_FEATURES_PATH)
    if not os.path.exists(processed_path):
        logger.error(f"Engineered features file not found at: {processed_path}. Please run data pipeline first.")
        sys.exit(1)
        
    # 2. Define target label and load features
    target_col = "is_basis_weight_off_spec"
    logger.info(f"Loading engineered feature store: {processed_path}")
    df = pd.read_csv(processed_path)
    
    # Drop rows where target label is missing
    df = df.dropna(subset=[target_col])
    logger.info(f"Loaded dataset with shape (after dropping missing targets): {df.shape}")
    
    if target_col not in df.columns:
        logger.error(f"Target column '{target_col}' not found in feature store.")
        sys.exit(1)

        
    # Drop labels, timestamps, and target leakages
    leakage_cols = ["timestamp", "active_grade_id", "basis_weight_gsm", "basis_weight_dev", target_col]
    feature_cols = [col for col in df.columns if col not in leakage_cols]
    
    X = df[feature_cols]
    y = df[target_col]
    
    logger.info(f"Target label distribution:\n{y.value_counts(normalize=True).round(4) * 100}")
    logger.info(f"Training on {len(feature_cols)} engineered features: {feature_cols}")
    
    # 3. Model Training & Comparison
    logger.info("Training and comparing candidate classifiers (Random Forest, XGBoost, LightGBM, CatBoost)...")
    trainer = MLTrainer(test_size=0.2, random_state=42)
    best_name, best_model, comparison = trainer.train_and_compare(X, y)
    
    logger.info("=========================================================================")
    logger.info("                           Model Comparison Log                           ")
    logger.info("=========================================================================")
    for model_name, metrics in comparison.items():
        logger.info(
            f"Model: {model_name:<15} | "
            f"Accuracy: {metrics['accuracy']:.4f} | "
            f"Precision: {metrics['precision']:.4f} | "
            f"Recall: {metrics['recall']:.4f} | "
            f"F1 Score: {metrics['f1_score']:.4f} | "
            f"ROC AUC: {metrics['roc_auc']:.4f}"
        )
    logger.info("=========================================================================")
    
    logger.info(f"Automatically selected Champion Model: [{best_name}]")
    
    # 4. Save and Register Champion Model
    logger.info("Registering champion model in local checkpoint registry...")
    registry = ModelRegistry(registry_dir=os.path.join(PROJECT_ROOT, "backend", "app", "models", "checkpoints"))
    
    champion_metrics = comparison[best_name]
    binary_path = registry.save_model(
        model_name="basis_weight_deviation_champion",
        model_type=best_name,
        model=best_model,
        metrics=champion_metrics,
        features=feature_cols
    )
    
    logger.info(f"Champion binary saved to: {binary_path}")
    
    # Log top feature importances
    logger.info("Top Feature Importances:")
    importances = champion_metrics["feature_importance"]
    sorted_importances = sorted(importances.items(), key=lambda x: x[1], reverse=True)[:5]
    for feat, imp in sorted_importances:
        logger.info(f"  - {feat:<30}: {imp:.4f}")
        
    logger.info("Confusion Matrix:")
    cm = champion_metrics["confusion_matrix"]
    logger.info(f"  - True Negatives  (TN): {cm['true_negatives']}")
    logger.info(f"  - False Positives (FP): {cm['false_positives']}")
    logger.info(f"  - False Negatives (FN): {cm['false_negatives']}")
    logger.info(f"  - True Positives  (TP): {cm['true_positives']}")
    
    logger.info("ML Model pipeline run completed successfully!")

if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stdout, level="INFO", colorize=True)
    
    run_model_training()
    sys.exit(0)
