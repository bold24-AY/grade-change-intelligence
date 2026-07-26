import os
import json
import joblib
from datetime import datetime
from typing import Dict, Any
from backend.app.ml.base_model import BaseMLClassifier
from backend.app.ml.random_forest import RandomForestWrapper
from backend.app.ml.xgboost_model import XGBoostWrapper
from backend.app.ml.lightgbm_model import LightGBMWrapper
from backend.app.ml.catboost_model import CatBoostWrapper

class ModelRegistry:
    """
    Saves and loads champion models, writing model descriptions
    (model cards) to register metadata versions.
    """
    
    WRAPPERS = {
        "RandomForest": RandomForestWrapper,
        "XGBoost": XGBoostWrapper,
        "LightGBM": LightGBMWrapper,
        "CatBoost": CatBoostWrapper
    }
    
    def __init__(self, registry_dir: str = None):
        self.registry_dir = registry_dir or os.path.join("backend", "app", "models", "checkpoints")
        
    def save_model(self, model_name: str, model_type: str, model: BaseMLClassifier, metrics: Dict[str, Any], features: list) -> str:
        """Saves model binaries and writes model metadata manifests."""
        os.makedirs(self.registry_dir, exist_ok=True)
        
        # Paths
        binary_path = os.path.join(self.registry_dir, f"{model_name}.joblib")
        manifest_path = os.path.join(self.registry_dir, "model_registry.json")
        
        # Save model binaries
        model.save(binary_path)
        
        # Save metadata
        metadata = {
            "model_name": model_name,
            "model_type": model_type,
            "registered_at": datetime.utcnow().isoformat(),
            "metrics": {
                "accuracy": metrics.get("accuracy"),
                "precision": metrics.get("precision"),
                "recall": metrics.get("recall"),
                "f1_score": metrics.get("f1_score"),
                "roc_auc": metrics.get("roc_auc")
            },
            "features": features
        }
        
        registry_data = {}
        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, "r") as f:
                    registry_data = json.load(f)
            except Exception:
                registry_data = {}
                
        registry_data[model_name] = metadata
        registry_data["latest"] = metadata
        
        with open(manifest_path, "w") as f:
            json.dump(registry_data, f, indent=2)
            
        return binary_path

    def load_model(self, model_name: str) -> BaseMLClassifier:
        """Loads model binaries from metadata type specifications."""
        manifest_path = os.path.join(self.registry_dir, "model_registry.json")
        if not os.path.exists(manifest_path):
            raise FileNotFoundError("Model registry manifest not found.")
            
        with open(manifest_path, "r") as f:
            registry_data = json.load(f)
            
        if model_name not in registry_data:
            raise ValueError(f"Model '{model_name}' not registered in manifest.")
            
        meta = registry_data[model_name]
        model_type = meta["model_type"]
        binary_path = os.path.join(self.registry_dir, f"{model_name}.joblib")
        
        if model_type not in self.WRAPPERS:
            raise ValueError(f"Unknown model type: {model_type}")
            
        # Instantiate empty wrapper and load parameters
        wrapper = self.WRAPPERS[model_type]()
        wrapper.load(binary_path)
        return wrapper
