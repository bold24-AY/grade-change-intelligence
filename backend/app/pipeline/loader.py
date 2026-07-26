import os
import glob
import pandas as pd
from typing import List, Union

class DataLoader:
    """
    Ingestion class handling multi-format log loading.
    Supports CSV, Excel, and multi-file directory scans.
    """
    
    def load_single_file(self, filepath: str) -> pd.DataFrame:
        """Loads a single file depending on extension (.csv or .xlsx)."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Input file not found at: {filepath}")
            
        ext = os.path.splitext(filepath)[1].lower()
        if ext == '.csv':
            return pd.read_csv(filepath)
        elif ext in ['.xlsx', '.xls']:
            try:
                return pd.read_excel(filepath)
            except ImportError:
                # Fallback check to ensure openpyxl is installed
                raise ImportError(
                    "Excel engine openpyxl is required to parse Excel files. "
                    "Run: pip install openpyxl"
                )
        else:
            raise ValueError(f"Unsupported file format: {ext}. System parses only CSV or Excel files.")
            
    def load_multiple_files(self, filepaths: List[str]) -> pd.DataFrame:
        """Loads and concatenates multiple data frames from a list of paths."""
        dfs = []
        for path in filepaths:
            df = self.load_single_file(path)
            dfs.append(df)
            
        if not dfs:
            return pd.DataFrame()
            
        # Concatenate and sort chronologically by timestamp
        combined = pd.concat(dfs, ignore_index=True)
        if 'timestamp' in combined.columns:
            combined['timestamp'] = pd.to_datetime(combined['timestamp'], format='mixed')
            combined = combined.sort_values('timestamp').reset_index(drop=True)

            
        return combined

    def scan_and_load_directory(self, dir_path: str, extensions: List[str] = ["csv", "xlsx"]) -> pd.DataFrame:
        """Finds all files matching extensions in the directory and loads them."""
        matched_files = []
        for ext in extensions:
            matched_files.extend(glob.glob(os.path.join(dir_path, f"*.{ext}")))
            
        return self.load_multiple_files(matched_files)
