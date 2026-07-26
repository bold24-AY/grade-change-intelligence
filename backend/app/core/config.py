import os
import yaml
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application Settings.
    Loads configurations from config.yaml and overrides with environment variables if available.
    """
    PROJECT_NAME: str = "Grade Change Intelligence System"
    ENV: str = "development"
    DEBUG: bool = True
    
    # API server settings
    API_V1_STR: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Data Paths
    RAW_SENSOR_PATH: str = "data/raw/sensor_readings_sample.csv"
    PROCESSED_FEATURES_PATH: str = "data/processed/engineered_features_sample.csv"
    GRADE_SPEC_PATH: str = "data/external/grade_specifications.json"
    
    # Model details
    MODEL_NAME: str = "grade_transition_rf_v1"
    MODEL_VERSION: str = "1.0.0"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    class Config:
        case_sensitive = True

    def __init__(self, **values):
        super().__init__(**values)
        self._load_from_yaml()

    def _load_from_yaml(self):
        """Helper to overwrite defaults with values from config.yaml if it exists."""
        config_path = os.path.join(os.getcwd(), "config.yaml")
        if not os.path.exists(config_path):
            # Try ascending directory just in case we run tests from subdirectories
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "config.yaml")
            
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    yaml_data = yaml.safe_load(f)
                    if yaml_data:
                        if "app" in yaml_data:
                            self.PROJECT_NAME = yaml_data["app"].get("name", self.PROJECT_NAME)
                            self.ENV = yaml_data["app"].get("env", self.ENV)
                            self.DEBUG = yaml_data["app"].get("debug", self.DEBUG)
                        if "server" in yaml_data:
                            self.HOST = yaml_data["server"].get("host", self.HOST)
                            self.PORT = yaml_data["server"].get("port", self.PORT)
                        if "data" in yaml_data:
                            self.RAW_SENSOR_PATH = yaml_data["data"].get("raw_sensor_path", self.RAW_SENSOR_PATH)
                            self.PROCESSED_FEATURES_PATH = yaml_data["data"].get("processed_features_path", self.PROCESSED_FEATURES_PATH)
                            self.GRADE_SPEC_PATH = yaml_data["data"].get("grade_spec_path", self.GRADE_SPEC_PATH)
                        if "model" in yaml_data:
                            self.MODEL_NAME = yaml_data["model"].get("name", self.MODEL_NAME)
                            self.MODEL_VERSION = yaml_data["model"].get("version", self.MODEL_VERSION)
                        if "logging" in yaml_data:
                            self.LOG_LEVEL = yaml_data["logging"].get("level", self.LOG_LEVEL)
                            self.LOG_FILE = yaml_data["logging"].get("file_path", self.LOG_FILE)
            except Exception as e:
                print(f"[WARNING] Failed to parse config.yaml, using defaults. Error: {e}")

settings = Settings()
