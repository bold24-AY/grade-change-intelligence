import numpy as np
from typing import Dict, Any, Tuple
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    roc_curve
)
from backend.app.ml.base_model import BaseMLClassifier

class MLEvaluator:
    """
    Computes validation and evaluation metrics on test sets:
    Accuracy, Precision, Recall, F1, Confusion Matrix, and ROC curves.
    """
    
    @staticmethod
    def evaluate_classifier(model: BaseMLClassifier, X_test: Any, y_test: Any) -> Dict[str, Any]:
        """Runs predictions and calculates all scoring metrics."""
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)
        
        # Ensure we take the positive class probability
        if y_prob.ndim > 1 and y_prob.shape[1] > 1:
            y_prob_pos = y_prob[:, 1]
        else:
            y_prob_pos = y_prob
            
        accuracy = float(accuracy_score(y_test, y_pred))
        precision = float(precision_score(y_test, y_pred, zero_division=0))
        recall = float(recall_score(y_test, y_pred, zero_division=0))
        f1 = float(f1_score(y_test, y_pred, zero_division=0))
        
        try:
            auc = float(roc_auc_score(y_test, y_prob_pos))
        except ValueError:
            auc = 0.5  # Default if only one class is present in test subset
            
        # Confusion Matrix
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred, labels=[0, 1]).ravel()
        conf_matrix = {
            "true_negatives": int(tn),
            "false_positives": int(fp),
            "false_negatives": int(fn),
            "true_positives": int(tp)
        }
        
        # ROC Curve coords
        fpr, tpr, thresholds = roc_curve(y_test, y_prob_pos, pos_label=1)
        roc_curve_data = {
            "fpr": fpr.tolist(),
            "tpr": tpr.tolist(),
            "thresholds": thresholds.tolist()
        }
        
        # Feature importances
        feature_names = list(X_test.columns) if hasattr(X_test, "columns") else []
        importances = model.get_feature_importances(feature_names)
        
        return {
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "roc_auc": round(auc, 4),
            "confusion_matrix": conf_matrix,
            "roc_curve": roc_curve_data,
            "feature_importance": importances
        }
