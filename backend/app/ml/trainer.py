from typing import Dict, Any, Tuple
from sklearn.model_selection import train_test_split
from backend.app.ml.random_forest import RandomForestWrapper
from backend.app.ml.xgboost_model import XGBoostWrapper
from backend.app.ml.lightgbm_model import LightGBMWrapper
from backend.app.ml.catboost_model import CatBoostWrapper
from backend.app.ml.evaluator import MLEvaluator
from backend.app.ml.base_model import BaseMLClassifier

class MLTrainer:
    """
    Manages candidates initialization, datasets splitting, training,
    and automatic champion model selection.
    """
    
    def __init__(self, test_size: float = 0.2, random_state: int = 42):
        self.test_size = test_size
        self.random_state = random_state
        self.candidates: Dict[str, BaseMLClassifier] = {
            "RandomForest": RandomForestWrapper(random_state=random_state),
            "XGBoost": XGBoostWrapper(random_state=random_state),
            "LightGBM": LightGBMWrapper(random_state=random_state),
            "CatBoost": CatBoostWrapper(random_state=random_state)
        }
        
    def split_data(self, X: Any, y: Any) -> Tuple[Any, Any, Any, Any]:
        """Splits datasets into train/test sets."""
        return train_test_split(
            X, y, 
            test_size=self.test_size, 
            random_state=self.random_state,
            stratify=y if len(set(y)) > 1 else None
        )
        
    def train_and_compare(self, X: Any, y: Any) -> Tuple[str, BaseMLClassifier, Dict[str, Dict[str, Any]]]:
        """
        Fits all models, evaluates metrics, and chooses the champion
        based on validation F1 Score.
        """
        X_train, X_test, y_train, y_test = self.split_data(X, y)
        
        comparison_results = {}
        best_score = -1.0
        best_model_name = None
        best_model = None
        
        for name, wrapper in self.candidates.items():
            # Fit model
            wrapper.fit(X_train, y_train)
            
            # Evaluate metrics
            metrics = MLEvaluator.evaluate_classifier(wrapper, X_test, y_test)
            comparison_results[name] = metrics
            
            # Champion selection rule (maximize F1 score, default to Accuracy if F1 tied)
            f1 = metrics["f1_score"]
            if f1 > best_score:
                best_score = f1
                best_model_name = name
                best_model = wrapper
            elif abs(f1 - best_score) < 1e-5:
                # Tie-breaker: use Accuracy
                if best_model_name is None or metrics["accuracy"] > comparison_results[best_model_name]["accuracy"]:
                    best_model_name = name
                    best_model = wrapper
                    
        return best_model_name, best_model, comparison_results
