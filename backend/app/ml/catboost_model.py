import os
import joblib
from typing import Any, Dict
from backend.app.ml.base_model import BaseMLClassifier

try:
    from catboost import CatBoostClassifier
    CATBOOST_AVAILABLE = True
except ImportError:
    from sklearn.ensemble import AdaBoostClassifier
    CATBOOST_AVAILABLE = False

class CatBoostWrapper(BaseMLClassifier):
    """
    CatBoost Classifier wrapper. Falls back to scikit-learn AdaBoost
    if catboost package is not installed.
    """
    
    def __init__(self, iterations: int = 100, depth: int = 6, learning_rate: float = 0.1, random_state: int = 42):
        self.catboost_available = CATBOOST_AVAILABLE
        self.feature_names = []
        
        if self.catboost_available:
            self.model = CatBoostClassifier(
                iterations=iterations,
                depth=depth,
                learning_rate=learning_rate,
                random_seed=random_state,
                verbose=0
            )
        else:
            self.model = AdaBoostClassifier(
                n_estimators=iterations,
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
            "catboost_available": self.catboost_available
        }, filepath)
        
    def load(self, filepath: str) -> None:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found at: {filepath}")
        data = joblib.load(filepath)
        self.model = data["model"]
        self.feature_names = data.get("feature_names", [])
        self.catboost_available = data.get("catboost_available", self.catboost_available)
