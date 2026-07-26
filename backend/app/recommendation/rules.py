import yaml
import os
from typing import Dict, Any, Tuple
from backend.app.recommendation.schema import ProcessTelemetryInput, PredictionInput, AdjustmentRecommendation

class PhysicsControlRules:
    """
    Applies configurable physical heuristics and safety limits
    to recommend actuator setpoint delta changes.
    """
    
    OPERATOR_GUIDELINES = {
        "GRADE_A": "For standard 80gsm copy paper, prioritize pulp flow consistency checks. Maintain speed above 800mpm.",
        "GRADE_B": "For 120gsm cardstock, ensure slow machine deceleration. Steam cylinder pressure must scale up early to prevent moisture dampness.",
        "GRADE_C": "For newsprint lightweight transitions, watch for sheet flutter. Keep draw tension tight; keep speed high."
    }
    
    def __init__(self, config_path: str = "config.yaml"):
        self.gains = {
            "stock_flow_per_gsm_dev": -5.5,
            "filler_flow_per_gsm_dev": -2.0,
            "steam_pressure_per_moisture_dev": 0.4,
            "speed_adjustment_gain": 0.05
        }
        self.limits = {
            "max_stock_flow_change_pct": 10.0,
            "max_filler_flow_change_pct": 15.0,
            "max_steam_pressure_change_bar": 1.5,
            "max_speed_change_mpm": 50.0
        }
        self._load_from_yaml(config_path)

    def _load_from_yaml(self, config_path: str) -> None:
        """Loads control variables from configuration file."""
        if not os.path.exists(config_path):
            # Fallback path lookup for test environments
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config.yaml")
            
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    data = yaml.safe_load(f)
                    if data and "recommendation" in data:
                        rec = data["recommendation"]
                        if "gains" in rec:
                            self.gains.update(rec["gains"])
                        if "limits" in rec:
                            self.limits.update(rec["limits"])
            except Exception:
                pass # Use hardcoded defaults if parsing fails

    def calculate_recommendations(
        self, telemetry: ProcessTelemetryInput, prediction: PredictionInput
    ) -> Tuple[AdjustmentRecommendation, str]:
        """Calculates delta adjustments based on physical gains and limits."""
        deviation = prediction.basis_weight_dev
        
        # 1. Stock Flow Delta (thick stock pulp flow)
        raw_stock_delta = self.gains["stock_flow_per_gsm_dev"] * deviation
        # Apply safety bounds clipping
        max_stock_change = telemetry.pulp_flow_m3h * (self.limits["max_stock_flow_change_pct"] / 100.0)
        stock_delta = max(min(raw_stock_delta, max_stock_change), -max_stock_change)
        
        # 2. Filler Flow Delta (proportionate to pulp flow changes to maintain ash ratio)
        raw_filler_delta = self.gains["filler_flow_per_gsm_dev"] * deviation
        max_filler_change = 100.0 * (self.limits["max_filler_flow_change_pct"] / 100.0) # assume baseline 100
        filler_delta = max(min(raw_filler_delta, max_filler_change), -max_filler_change)
        
        # 3. Steam Pressure Delta (if basis weight is off-spec, moisture correlates.
        # We increase drying pressure if basis weight is high, to maintain target moisture).
        raw_steam_delta = 0.0
        if prediction.is_basis_weight_off_spec and deviation > 0:
            # basis weight too high requires more drying steam
            raw_steam_delta = self.gains["steam_pressure_per_moisture_dev"] * deviation
        steam_delta = max(min(raw_steam_delta, self.limits["max_steam_pressure_change_bar"]), -self.limits["max_steam_pressure_change_bar"])
        
        # 4. Machine Speed Delta (speed can be slightly altered to spread or compress basis weight)
        raw_speed_delta = self.gains["speed_adjustment_gain"] * (-deviation) * telemetry.machine_speed_mpm / 100.0
        speed_delta = max(min(raw_speed_delta, self.limits["max_speed_change_mpm"]), -self.limits["max_speed_change_mpm"])
        
        # Construct output
        adjustments = AdjustmentRecommendation(
            stock_flow_m3h_delta=round(stock_delta, 2),
            filler_flow_lmin_delta=round(filler_delta, 2),
            steam_pressure_bar_delta=round(steam_delta, 2),
            machine_speed_mpm_delta=round(speed_delta, 2)
        )
        
        # Causal Explanation
        direction = "reduce" if deviation > 0 else "increase"
        explanation = (
            f"The scanner measures a basis weight deviation of {deviation:+.2f} gsm. "
            f"To correct this, we recommend to {direction} stock flow by {abs(adjustments.stock_flow_m3h_delta)} m3/h. "
            f"Machine speed is adjusted by {adjustments.machine_speed_mpm_delta:+.1f} mpm to stabilize basis weight profile spread."
        )
        
        return adjustments, explanation
