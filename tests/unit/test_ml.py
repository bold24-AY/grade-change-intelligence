import os
import pytest
import pandas as pd
import numpy as np
from backend.app.ml.random_forest import RandomForestWrapper
from backend.app.ml.trainer import MLTrainer
from backend.app.ml.evaluator import MLEvaluator
from backend.app.ml.registry import ModelRegistry

@pytest.fixture
def dummy_dataset():
    """Generates a small dummy feature set and binary label for ML unit tests."""
    np.random.seed(42)
    X = pd.DataFrame({
        "feat_a": np.random.normal(0, 1, 50),
        "feat_b": np.random.uniform(2, 5, 50),
        "feat_c": np.random.choice([0, 1], 50)
    })
    
    # Label is a linear function of features with noise
    y = (X["feat_a"] + X["feat_c"] > 0.5).astype(int)
    return X, y

def test_trainer_model_comparison(dummy_dataset):
    """Verify that MLTrainer executes training comparison across wrappers."""
    X, y = dummy_dataset
    trainer = MLTrainer(test_size=0.3, random_state=42)
    
    best_name, best_model, comparison = trainer.train_and_compare(X, y)
    
    assert best_name in ["RandomForest", "XGBoost", "LightGBM", "CatBoost"]
    assert best_model is not None
    assert "RandomForest" in comparison
    assert "accuracy" in comparison["RandomForest"]

def test_evaluator_metrics_calculation(dummy_dataset):
    """Verify MLEvaluator computes all mandatory evaluation metrics."""
    X, y = dummy_dataset
    X_train, X_test = X.iloc[:40], X.iloc[40:]
    y_train, y_test = y.iloc[:40], y.iloc[40:]
    
    model = RandomForestWrapper(random_state=42)
    model.fit(X_train, y_train)
    
    metrics = MLEvaluator.evaluate_classifier(model, X_test, y_test)
    
    assert "accuracy" in metrics
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1_score" in metrics
    assert "roc_auc" in metrics
    assert "confusion_matrix" in metrics
    assert "roc_curve" in metrics
    assert "feature_importance" in metrics
    
    # Assert feature importance length matches feature count
    assert len(metrics["feature_importance"]) == 3

def test_model_registry_serialization(tmp_path, dummy_dataset):
    """Verify ModelRegistry successfully saves and loads wrapper checkpoints."""
    X, y = dummy_dataset
    model = RandomForestWrapper(random_state=42)
    model.fit(X, y)
    
    # Mock metrics
    metrics = {"accuracy": 0.9, "precision": 0.9, "recall": 0.9, "f1_score": 0.9, "roc_auc": 0.9, "feature_importance": {}}
    features = list(X.columns)
    
    registry = ModelRegistry(registry_dir=str(tmp_path))
    binary_path = registry.save_model("test_rf", "RandomForest", model, metrics, features)
    
    assert os.path.exists(binary_path)
    assert os.path.exists(tmp_path / "model_registry.json")
    
    # Load model back
    loaded_model = registry.load_model("test_rf")
    assert isinstance(loaded_model, RandomForestWrapper)
    assert loaded_model.feature_names == features
