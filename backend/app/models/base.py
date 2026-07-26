from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseMLModel(ABC):
    """
    Abstract Base Class for Machine Learning Models (SOLID - Open/Closed Principle).
    All grade change models must inherit from this class and implement the abstract methods.
    """
    
    @abstractmethod
    def fit(self, X: Any, y: Any, **kwargs) -> Any:
        """Train the model on features X and labels y."""
        pass
        
    @abstractmethod
    def predict(self, X: Any) -> Any:
        """Run prediction/inference on a set of features X."""
        pass

    @abstractmethod
    def predict_proba(self, X: Any) -> Any:
        """Run prediction probabilities on features X."""
        pass
        
    @abstractmethod
    def save(self, filepath: str) -> None:
        """Serialize and save the model weights/parameters to disk."""
        pass
        
    @abstractmethod
    def load(self, filepath: str) -> None:
        """Load the model weights/parameters from disk."""
        pass
