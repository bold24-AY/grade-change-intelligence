const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Common fetch helper to handle JSON parsing and errors.
 */
async function fetchJson(endpoint, options = {}) {
  const url = `${API_BASE_URL}/api/v1${endpoint}`;
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });
    
    if (!response.ok) {
      const errBody = await response.json().catch(() => ({}));
      throw new Error(errBody.detail || `HTTP Error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error(`API request failed on ${endpoint}:`, error);
    throw error;
  }
}

export const api = {
  /**
   * Run telemetry inference.
   */
  async predict(telemetryData) {
    try {
      return await fetchJson('/prediction/predict', {
        method: 'POST',
        body: JSON.stringify(telemetryData),
      });
    } catch (e) {
      console.warn("Falling back to local simulated predictions...");
      // Simulated frontend fallback if backend isn't running
      const isTransitioning = telemetryData.machine_speed_mpm < 840 || telemetryData.consistency_pct < 3.2;
      return {
        timestamp: telemetryData.timestamp || new Date().toISOString(),
        is_transitioning: isTransitioning,
        confidence_score: isTransitioning ? 0.88 + Math.random() * 0.1 : 0.95 + Math.random() * 0.04,
        predicted_target_grade: isTransitioning ? 'GRADE_B' : null,
        anomaly_detected: false
      };
    }
  },

  /**
   * Get health metrics.
   */
  async getHealth() {
    try {
      return await fetchJson('/monitoring/health');
    } catch (e) {
      return {
        status: 'simulated-local',
        timestamp: new Date().toISOString(),
        model_version: '1.0.0-mock',
        uptime_seconds: 9999
      };
    }
  },

  /**
   * Get grade specifications metadata.
   */
  async getSpecs() {
    try {
      return await fetchJson('/monitoring/specs');
    } catch (e) {
      return {
        "GRADE_A": {
          "name": "Standard Copier Paper 80gsm",
          "target_basis_weight_gsm": 80.0,
          "tolerance_basis_weight_gsm": 1.5,
          "target_moisture_pct": 5.5,
          "tolerance_moisture_pct": 0.3,
          "nominal_machine_speed_mpm": 850.0
        },
        "GRADE_B": {
          "name": "Premium Heavyweight Cardstock 120gsm",
          "target_basis_weight_gsm": 120.0,
          "tolerance_basis_weight_gsm": 2.0,
          "target_moisture_pct": 6.2,
          "tolerance_moisture_pct": 0.4,
          "nominal_machine_speed_mpm": 750.0
        },
        "GRADE_C": {
          "name": "Lightweight Newsprint 45gsm",
          "target_basis_weight_gsm": 45.0,
          "tolerance_basis_weight_gsm": 1.0,
          "target_moisture_pct": 8.0,
          "tolerance_moisture_pct": 0.5,
          "nominal_machine_speed_mpm": 1100.0
        }
      };
    }
  }
};
export default api;
