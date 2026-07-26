import os
import joblib
from typing import Any, Dict
from backend.app.ml.base_model import BaseMLClassifier

try:
    from lightgbm import LGBMClassifier
    LGBM_AVAILABLE = True
except ImportError:
    from sklearn.ensemble import HistGradientBoostingClassifier
    LGBM_AVAILABLE = False

class LightGBMWrapper(BaseMLClassifier):
    """
    LightGBM Classifier wrapper. Falls back to scikit-learn HistGradientBoosting
    if lightgbm package is not installed.
    """
    
    def __init__(self, n_estimators: int = 100, max_depth: int = 6, learning_rate: float = 0.1, random_state: int = 42):
        self.lgbm_available = LGBM_AVAILABLE
        self.feature_names = []
        
        if self.lgbm_available:
            self.model = LGBMClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                learning_rate=learning_rate,
                random_state=random_state,
                verbose=-1
            )
        else:
            self.model = HistGradientBoostingClassifier(
                max_iter=n_estimators,
                max_depth=max_depth,
                learning_rate=learning_rate,
                random_state=random_state
            )
            
    def fit(self, X: Any, y: Any) -> Any:
        if hasattr(X, "columns"):
            self.feature_names = list(X.columns)
        self.model.fit(X, y)
        return self
        
    def predict(self, X: Any) -> Any:
        return self.model.predict(X)
        
    def predict_proba(self, X: Any) -> Any:
        return self.model.predict_proba(X)
        
    def get_feature_importances(self, feature_names: list) -> Dict[str, float]:
        names = feature_names if feature_names else self.feature_names
        
        if self.lgbm_available:
            importances = self.model.feature_importances_
        else:
            # HistGradientBoosting doesn't provide standard importances natively.
            # We default to uniform baseline for fallback metrics or permutation-ready weights.
            importances = [1.0 / len(names)] * len(names) if names else [0.0]
            
        if not names:
            names = [f"feature_{i}" for i in range(len(importances))]
        return dict(zip(names, importances))
        
    def save(self, filepath: str) -> None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump({
            "model": self.model, 
            "feature_names": self.feature_names,
            "lgbm_available": self.lgbm_available
        }, filepath)
        
    def load(self, filepath: str) -> None:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found at: {filepath}")
        data = joblib.load(filepath)
        self.model = data["model"]
        self.feature_names = data.get("feature_names", [])
        self.lgbm_available = data.get("lgbm_available", self.lgbm_available)
