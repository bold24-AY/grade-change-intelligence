import os
import joblib
from typing import Any, Dict
from sklearn.ensemble import RandomForestClassifier
from backend.app.ml.base_model import BaseMLClassifier

class RandomForestWrapper(BaseMLClassifier):
    """
    Random Forest Classifier wrapper using scikit-learn.
    """
    
    def __init__(self, n_estimators: int = 100, max_depth: int = 10, random_state: int = 42):
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state
        )
        self.feature_names = []
        
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
        # Use provided feature names or fallback to saved ones
        names = feature_names if feature_names else self.feature_names
        if not names:
            names = [f"feature_{i}" for i in range(len(importances))]
        return dict(zip(names, importances))
        
    def save(self, filepath: str) -> None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump({"model": self.model, "feature_names": self.feature_names}, filepath)
        
    def load(self, filepath: str) -> None:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found at: {filepath}")
        data = joblib.load(filepath)
        self.model = data["model"]
        self.feature_names = data.get("feature_names", [])
