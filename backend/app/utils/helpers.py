"""
Utility helpers for mathematical and coordinate conversions.
"""

def mpm_to_fpm(speed_mpm: float) -> float:
    """
    Convert machine speed from Meters per Minute (MPM) to Feet per Minute (FPM).
    Formula: fpm = mpm * 3.28084
    """
    return round(speed_mpm * 3.28084, 2)

def calculate_broke_tonnage(
    transition_duration_minutes: float, 
    speed_mpm: float, 
    basis_weight_gsm: float,
    web_width_meters: float = 8.5
) -> float:
    """
    Estimate total tons of broke paper generated during a grade change transition.
    Formula: tonnage = speed (m/min) * duration (min) * width (m) * basis_weight (g/m2) / 1,000,000 (g to tons)
    """
    total_area_m2 = speed_mpm * transition_duration_minutes * web_width_meters
    total_mass_grams = total_area_m2 * basis_weight_gsm
    return round(total_mass_grams / 1e6, 3)
