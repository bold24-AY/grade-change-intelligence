import os
import json
import hashlib
import pandas as pd
from datetime import datetime

class DataVersioner:
    """
    Simulates data versioning by computing cryptographic hashes of processed 
    datasets and writing version descriptor manifests (JSON).
    """
    
    def __init__(self, manifest_dir: str = None):
        self.manifest_dir = manifest_dir or os.path.join("data", "processed")
        
    def calculate_dataset_hash(self, df: pd.DataFrame) -> str:
        """Computes a SHA-256 hash of the DataFrame contents."""
        # Convert DataFrame to csv bytes to get stable hash representation
        csv_bytes = df.to_csv(index=False).encode('utf-8')
        return hashlib.sha256(csv_bytes).hexdigest()
        
    def register_version(self, df: pd.DataFrame, dataset_name: str, schema_version: str = "1.0.0") -> dict:
        """
        Creates and registers a version entry in version_manifest.json.
        """
        os.makedirs(self.manifest_dir, exist_ok=True)
        manifest_path = os.path.join(self.manifest_dir, "version_manifest.json")
        
        # Calculate stats
        row_count = len(df)
        col_list = list(df.columns)
        data_hash = self.calculate_dataset_hash(df)
        
        new_version_info = {
            "version_tag": f"v_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.utcnow().isoformat(),
            "dataset_name": dataset_name,
            "schema_version": schema_version,
            "row_count": row_count,
            "columns": col_list,
            "sha256_hash": data_hash
        }
        
        # Load existing manifest or initialize
        manifest_data = {}
        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, "r") as f:
                    manifest_data = json.load(f)
            except Exception:
                manifest_data = {}
                
        # Append entry under history
        if "history" not in manifest_data:
            manifest_data["history"] = []
            
        manifest_data["history"].append(new_version_info)
        manifest_data["latest"] = new_version_info
        
        # Write back to manifest
        with open(manifest_path, "w") as f:
            json.dump(manifest_data, f, indent=2)
            
        return new_version_info
