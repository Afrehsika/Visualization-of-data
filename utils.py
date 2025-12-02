"""
Data Management Utilities
Handles file I/O, data validation, and preprocessing
"""

import csv
import os
import pandas as pd
import numpy as np
from typing import List, Tuple, Dict, Optional


def read_csv_data(file_path: str) -> Tuple[List[str], List[List[str]]]:
    """
    Reads a CSV file and returns headers and data.
    Assumes the first row is headers.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
    
    if not data:
        return [], []
        
    headers = data[0]
    rows = data[1:]
    return headers, rows


def read_excel_data(file_path: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
    """
    Reads an Excel file and returns a pandas DataFrame
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name or 0)
        return df
    except Exception as e:
        raise ValueError(f"Error reading Excel file: {str(e)}")


def read_data_file(file_path: str) -> pd.DataFrame:
    """
    Automatically detect file type and read data
    Supports CSV and Excel files
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == '.csv':
        return pd.read_csv(file_path)
    elif file_ext in ['.xlsx', '.xls']:
        return pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")


def preview_data(df: pd.DataFrame, rows: int = 5) -> str:
    """
    Generate a preview of the DataFrame
    """
    preview = f"Data Preview ({len(df)} rows, {len(df.columns)} columns)\n"
    preview += "="*60 + "\n"
    preview += df.head(rows).to_string()
    preview += "\n\nData Types:\n"
    preview += df.dtypes.to_string()
    return preview


def get_numeric_columns(df: pd.DataFrame) -> List[str]:
    """
    Get list of numeric column names
    """
    return df.select_dtypes(include=[np.number]).columns.tolist()


def detect_missing_values(df: pd.DataFrame) -> Dict[str, int]:
    """
    Detect missing values in each column
    """
    return df.isnull().sum().to_dict()


def handle_missing_values(df: pd.DataFrame, method: str = 'drop', fill_value: Optional[float] = None) -> pd.DataFrame:
    """
    Handle missing values in DataFrame
    
    Methods:
    - 'drop': Remove rows with missing values
    - 'mean': Fill with column mean
    - 'median': Fill with column median
    - 'mode': Fill with column mode
    - 'constant': Fill with specified value
    """
    df_copy = df.copy()
    
    if method == 'drop':
        return df_copy.dropna()
    elif method == 'mean':
        return df_copy.fillna(df_copy.mean(numeric_only=True))
    elif method == 'median':
        return df_copy.fillna(df_copy.median(numeric_only=True))
    elif method == 'mode':
        return df_copy.fillna(df_copy.mode().iloc[0])
    elif method == 'constant' and fill_value is not None:
        return df_copy.fillna(fill_value)
    else:
        raise ValueError(f"Invalid method: {method}")


def normalize_data(data: List[float]) -> List[float]:
    """
    Normalize data to 0-1 range using min-max scaling
    """
    data_array = np.array(data)
    min_val = np.min(data_array)
    max_val = np.max(data_array)
    
    if max_val == min_val:
        return [0.5] * len(data)
    
    normalized = (data_array - min_val) / (max_val - min_val)
    return normalized.tolist()


def standardize_data(data: List[float]) -> List[float]:
    """
    Standardize data to have mean=0 and std=1 (z-score normalization)
    """
    data_array = np.array(data)
    mean = np.mean(data_array)
    std = np.std(data_array)
    
    if std == 0:
        return [0.0] * len(data)
    
    standardized = (data_array - mean) / std
    return standardized.tolist()


def parse_numeric_data(data_string: str) -> List[float]:
    """
    Parses a comma-separated string into a list of floats.
    """
    if not data_string:
        return []
    return [float(x.strip()) for x in data_string.split(',') if x.strip()]


def export_to_csv(data: pd.DataFrame, file_path: str) -> None:
    """
    Export DataFrame to CSV file
    """
    data.to_csv(file_path, index=False)


def validate_numeric_input(text: str) -> bool:
    """
    Validate that input string contains valid numeric data
    """
    if not text:
        return False
    
    try:
        parse_numeric_data(text)
        return True
    except (ValueError, TypeError):
        return False
