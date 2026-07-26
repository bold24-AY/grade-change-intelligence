from backend.app.recommendation.schema import (
    ProcessTelemetryInput, 
    PredictionInput, 
    RecommendationOutput,
    ExplanationDetails
)
from backend.app.recommendation.rules import PhysicsControlRules
from backend.app.recommendation.historical import HistoricalMatcher

class RecommendationEngine:
    """
    Coordinates physics-based rules and nearest-neighbor search systems
    to compile a decision support recommendation card for operations.
    """
    
    def __init__(self, config_path: str = "config.yaml", data_path: str = None):
        self.rules_engine = PhysicsControlRules(config_path)
        self.historical_matcher = HistoricalMatcher(data_path)
        
    def generate_recommendation(
        self, telemetry: ProcessTelemetryInput, prediction: PredictionInput
    ) -> RecommendationOutput:
        """Runs the recommendation loop."""
        # 1. Calculate physics adjustments and reasoning
        adjustments, why_explanation = self.rules_engine.calculate_recommendations(telemetry, prediction)
        
        # 2. Match historical runs
        top_k = self.rules_engine.limits.get("top_k", 3)
        historical_runs = self.historical_matcher.find_similar_runs(telemetry, top_k=top_k)
        
        # 3. Calculate recommendation confidence
        # Formula: weighted average of prediction confidence and historical matches similarities
        mean_sim = 0.95
        if historical_runs:
            mean_sim = sum(h.similarity_score for h in historical_runs) / len(historical_runs)
            
        rec_confidence = round(0.4 * prediction.confidence_score + 0.6 * mean_sim, 4)
        
        # Gather guidelines notes
        grade = telemetry.active_grade_id
        op_guideline = self.rules_engine.OPERATOR_GUIDELINES.get(
            grade, 
            "Monitor web tension and basis weight scanner boundaries closely."
        )
        
        explanation = ExplanationDetails(
            why=why_explanation,
            confidence=rec_confidence,
            historical_evidence=historical_runs,
            operator_notes=op_guideline
        )
        
        return RecommendationOutput(
            active_grade_id=telemetry.active_grade_id,
            adjustments=adjustments,
            explanation=explanation
        )
