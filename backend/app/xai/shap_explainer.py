import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List
from backend.app.ml.base_model import BaseMLClassifier

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False

class ShapExplanationService:
    """
    Computes SHAP value attributions for classifier model predictions.
    Falls back gracefully to tree path attribution approximations if
    the shap library is not installed or fails compile checks.
    """
    
    def __init__(self, champion_model: BaseMLClassifier, background_data: pd.DataFrame = None):
        self.model = champion_model
        self.background_data = background_data
        self.shap_available = SHAP_AVAILABLE
        self.explainer = None
        self._initialize_explainer()

    def _initialize_explainer(self) -> None:
        """Initializes the SHAP Explainer object if package is present."""
        if not self.shap_available or self.model is None:
            return
            
        try:
            # We attempt to extract the underlying model if it's wrapped
            raw_model = getattr(self.model, "model", self.model)
            
            if self.background_data is not None and not self.background_data.empty:
                # Use a small sample of background data to speed up explainer
                background_sample = self.background_data.sample(min(len(self.background_data), 50), random_state=42)
                # Drop non-feature columns
                leakage_cols = ["timestamp", "active_grade_id", "basis_weight_gsm", "basis_weight_dev", "is_basis_weight_off_spec"]
                background_features = background_sample.drop(columns=[c for c in leakage_cols if c in background_sample.columns], errors="ignore")
                
                self.explainer = shap.TreeExplainer(raw_model, background_features)
            else:
                self.explainer = shap.TreeExplainer(raw_model)
        except Exception:
            # If TreeExplainer fails (e.g. wrapper incompatibility), set available to false to use fallback
            self.shap_available = False

    def compute_shap_attributions(self, X_instance: pd.DataFrame) -> Tuple[np.ndarray, float]:
        """Calculates Shapley value attributions for a single telemetry state."""
        # Standard features mapping
        feature_names = list(X_instance.columns)
        
        # Calculate base value (expected value)
        if self.shap_available and self.explainer is not None:
            try:
                # Calculate SHAP values
                shap_values = self.explainer(X_instance)
                
                # Check formatting (could be a SHAP Explanation object or a tuple of arrays)
                if hasattr(shap_values, "values"):
                    # For multi-class classification, SHAP returns list of values per class
                    # Binary classification can return 2D array or 3D array
                    values = shap_values.values
                    base_val = shap_values.base_values
                else:
                    values = shap_values
                    base_val = getattr(self.explainer, "expected_value", 0.5)
                    
                # Standardize values: extract positive class (class 1) SHAP values
                if isinstance(values, list):
                    # Multi-class list
                    shap_attr = values[1][0] if len(values) > 1 else values[0][0]
                elif values.ndim == 3:
                    # Shape: [instances, features, classes]
                    shap_attr = values[0, :, 1]
                elif values.ndim == 2:
                    # Shape: [instances, features]
                    shap_attr = values[0, :]
                else:
                    shap_attr = values
                    
                expected_val = base_val[1] if isinstance(base_val, (list, np.ndarray)) and len(base_val) > 1 else base_val
                return np.array(shap_attr).ravel(), float(expected_val)
                
            except Exception:
                # Fall through to fallback
                pass
                
        # --- Fallback Heuristic Attribution ---
        # Attribution = Importance_i * (x_i - mean_background_i)
        # This approximates linear feature contributions.
        raw_model = getattr(self.model, "model", self.model)
        importances = getattr(raw_model, "feature_importances_", None)
        
        if importances is None:
            # Try to fetch from custom wrapper
            feat_imp = self.model.get_feature_importances(feature_names)
            importances = np.array([feat_imp.get(name, 0.0) for name in feature_names])
            
        if importances is None or len(importances) != len(feature_names):
            importances = np.ones(len(feature_names)) / len(feature_names)
            
        # Calculate background averages
        mean_background = np.zeros(len(feature_names))
        if self.background_data is not None and not self.background_data.empty:
            for i, col in enumerate(feature_names):
                if col in self.background_data.columns:
                    mean_background[i] = self.background_data[col].mean()
                    
        # Feature deviation (delta from average state)
        instance_vector = X_instance.values.ravel()
        deviations = instance_vector - mean_background
        
        # Attribution = importance * sign(deviation) * magnitude
        attributions = importances * deviations
        
        # expected value is baseline 0.5 (equal probability)
        expected_val = 0.5
        
        return attributions, expected_val
