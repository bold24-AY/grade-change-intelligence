from typing import Any, Dict
from abc import abstractmethod
from backend.app.models.base import BaseMLModel


class BaseMLClassifier(BaseMLModel):

    """
    Abstract Base Class for Machine Learning Classifiers.
    Establishes the interface for Random Forest, XGBoost, CatBoost, and LightGBM.
    """
    
    @abstractmethod
    def fit(self, X: Any, y: Any) -> Any:
        """Fits the model parameters to features X and target label y."""
        pass
        
    @abstractmethod
    def predict(self, X: Any) -> Any:
        """Classifies features X to binary labels (0 or 1)."""
        pass
        
    @abstractmethod
    def predict_proba(self, X: Any) -> Any:
        """Calculates probability class estimates for features X."""
        pass
        
    @abstractmethod
    def get_feature_importances(self, feature_names: list) -> Dict[str, float]:
        """Returns feature importances mapped to feature names."""
        pass
        
    @abstractmethod
    def save(self, filepath: str) -> None:
        """Saves model binaries to disk."""
        pass
        
    @abstractmethod
    def load(self, filepath: str) -> None:
        """Loads model binaries from disk."""
        pass
