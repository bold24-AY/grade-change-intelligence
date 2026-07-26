import os
import joblib
from typing import Any, Dict
from backend.app.ml.base_model import BaseMLClassifier

try:
    from xgboost import XGBClassifier
    XGB_AVAILABLE = True
except ImportError:
    from sklearn.ensemble import GradientBoostingClassifier
    XGB_AVAILABLE = False

class XGBoostWrapper(BaseMLClassifier):
    """
    XGBoost Classifier wrapper. Falls back to scikit-learn GradientBoosting
    if xgboost package is not installed.
    """
    
    def __init__(self, n_estimators: int = 100, max_depth: int = 6, learning_rate: float = 0.1, random_state: int = 42):
        self.xgb_available = XGB_AVAILABLE
        self.feature_names = []
        
        if self.xgb_available:
            self.model = XGBClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                learning_rate=learning_rate,
                random_state=random_state,
                eval_metric="logloss"
            )
        else:
            self.model = GradientBoostingClassifier(
                n_estimators=n_estimators,
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
        importances = self.model.feature_importances_
        names = feature_names if feature_names else self.feature_names
        if not names:
            names = [f"feature_{i}" for i in range(len(importances))]
        return dict(zip(names, importances))
        
    def save(self, filepath: str) -> None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump({
            "model": self.model, 
            "feature_names": self.feature_names,
            "xgb_available": self.xgb_available
        }, filepath)
        
    def load(self, filepath: str) -> None:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found at: {filepath}")
        data = joblib.load(filepath)
        self.model = data["model"]
        self.feature_names = data.get("feature_names", [])
        self.xgb_available = data.get("xgb_available", self.xgb_available)
