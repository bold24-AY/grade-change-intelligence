import os
import pytest
from backend.app.core.config import Settings

def test_settings_load_defaults():
    """Verify that settings can be loaded and have default values."""
    settings = Settings()
    # Check defaults or environment injections
    assert settings.ENV in ["development", "testing", "production"]
    assert settings.PROJECT_NAME is not None
    assert settings.LOG_LEVEL in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

def test_settings_paths_present():
    """Verify that settings file paths are populated."""
    settings = Settings()
    assert settings.RAW_SENSOR_PATH is not None
    assert settings.PROCESSED_FEATURES_PATH is not None
    assert settings.GRADE_SPEC_PATH is not None
