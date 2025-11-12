"""Utilities for loading features from Parquet files.

This module provides functions to load feature data from Parquet files,
maintaining compatibility with the NPZ format used previously.
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple, List, Optional

import numpy as np
import pandas as pd

from src.config.loader import get_logger


_logger = get_logger("data.parquet_loader")


def load_features_from_parquet(
    parquet_path: str | Path,
    id_column: str = "system_id",
    feature_prefix: Optional[str] = None,
    return_feature_names: bool = False
) -> Tuple[List[str], np.ndarray] | Tuple[List[str], np.ndarray, List[str]]:
    """Load features from a Parquet file.

    Parameters
    ----------
    parquet_path : str | Path
        Path to the Parquet file containing features.
    id_column : str
        Name of the column containing system IDs. Default: 'system_id'.
    feature_prefix : str | None
        If specified, only load features with column names starting with this prefix.
        For example, 'shape_' or 'flatten_'. If None, loads all columns except id_column.
    return_feature_names : bool
        If True, returns feature column names as a third element. Default: False.

    Returns
    -------
    ids : list of str
        List of system IDs.
    X : np.ndarray
        Feature matrix of shape (n_samples, n_features).
    feature_names : list of str (optional)
        List of feature column names (if return_feature_names=True).

    Examples
    --------
    >>> ids, X = load_features_from_parquet("data/features.parquet")
    >>> print(f"Loaded {len(ids)} samples with {X.shape[1]} features")

    >>> # Load only shape features
    >>> ids, X = load_features_from_parquet(
    ...     "data/features.parquet",
    ...     feature_prefix="shape_"
    ... )

    >>> # Get feature names
    >>> ids, X, names = load_features_from_parquet(
    ...     "data/features.parquet",
    ...     return_feature_names=True
    ... )
    """
    parquet_path = Path(parquet_path)

    if not parquet_path.exists():
        raise FileNotFoundError(f"Parquet file not found: {parquet_path}")

    _logger.debug(f"Loading features from {parquet_path}")

    # Load the Parquet file
    df = pd.read_parquet(parquet_path)

    # Extract IDs
    if id_column not in df.columns:
        raise KeyError(
            f"ID column '{id_column}' not found in Parquet file. "
            f"Available columns: {list(df.columns)}"
        )

    ids = df[id_column].astype(str).tolist()

    # Select feature columns
    if feature_prefix is not None:
        feature_cols = [col for col in df.columns if col.startswith(feature_prefix)]
        if not feature_cols:
            raise ValueError(
                f"No columns found with prefix '{feature_prefix}'. "
                f"Available columns: {list(df.columns)}"
            )
    else:
        # All columns except ID column
        feature_cols = [col for col in df.columns if col != id_column]

    # Extract feature matrix
    X = df[feature_cols].to_numpy()

    _logger.info(
        f"Loaded {len(ids)} samples with {len(feature_cols)} features "
        f"from {parquet_path}"
    )

    if return_feature_names:
        return ids, X, feature_cols
    else:
        return ids, X


def load_multiple_feature_sets(
    parquet_path: str | Path,
    id_column: str = "system_id"
) -> dict:
    """Load all feature sets from a Parquet file.

    This function detects and loads different feature sets based on column prefixes
    (e.g., 'flatten_', 'shape_').

    Parameters
    ----------
    parquet_path : str | Path
        Path to the Parquet file.
    id_column : str
        Name of the ID column. Default: 'system_id'.

    Returns
    -------
    dict
        Dictionary with keys:
        - 'ids': list of system IDs
        - 'flatten': np.ndarray (if flatten features exist)
        - 'shape': np.ndarray (if shape features exist)
        - 'flatten_names': list of column names (if flatten features exist)
        - 'shape_names': list of column names (if shape features exist)

    Examples
    --------
    >>> data = load_multiple_feature_sets("data/features.parquet")
    >>> print(f"Feature sets: {[k for k in data.keys() if k != 'ids']}")
    >>> X_shape = data.get('shape')
    """
    parquet_path = Path(parquet_path)
    df = pd.read_parquet(parquet_path)

    result = {}

    # Extract IDs
    if id_column not in df.columns:
        raise KeyError(f"ID column '{id_column}' not found")

    result['ids'] = df[id_column].astype(str).tolist()

    # Detect feature prefixes
    feature_cols = [col for col in df.columns if col != id_column]
    prefixes = set()
    for col in feature_cols:
        if '_' in col:
            prefix = col.split('_')[0]
            prefixes.add(prefix)

    _logger.info(f"Detected feature prefixes: {sorted(prefixes)}")

    # Load each feature set
    for prefix in prefixes:
        cols = [col for col in feature_cols if col.startswith(f"{prefix}_")]
        if cols:
            result[prefix] = df[cols].to_numpy()
            result[f"{prefix}_names"] = cols
            _logger.info(f"  {prefix}: {result[prefix].shape}")

    return result


def convert_npz_to_parquet(
    npz_path: str | Path,
    output_parquet_path: str | Path,
    id_array_name: str = "systems",
    compression: str = "snappy"
) -> None:
    """Convert an NPZ file to Parquet format.

    This is a utility function to migrate existing NPZ feature files to Parquet.

    Parameters
    ----------
    npz_path : str | Path
        Path to input NPZ file.
    output_parquet_path : str | Path
        Path to output Parquet file.
    id_array_name : str
        Name of the array containing system IDs in the NPZ file. Default: 'systems'.
    compression : str
        Compression algorithm to use. Default: 'snappy'.

    Examples
    --------
    >>> convert_npz_to_parquet(
    ...     "data/old_features.npz",
    ...     "data/new_features.parquet"
    ... )
    """
    npz_path = Path(npz_path)
    output_parquet_path = Path(output_parquet_path)

    _logger.info(f"Converting {npz_path} to {output_parquet_path}")

    # Load NPZ data
    data = np.load(npz_path, allow_pickle=True)

    # Start with system IDs
    if id_array_name not in data:
        raise KeyError(f"ID array '{id_array_name}' not found in NPZ file")

    ids = data[id_array_name]
    if ids.dtype == object:
        ids = [str(x) for x in ids.tolist()]
    else:
        ids = [str(x) for x in ids]

    df_data = {'system_id': ids}

    # Process other arrays
    for key in data.keys():
        if key == id_array_name:
            continue

        arr = data[key]

        # Skip metadata arrays
        if arr.dtype == object and arr.ndim == 1:
            _logger.warning(f"Skipping object array '{key}' (likely metadata)")
            continue

        # Handle 2D feature arrays
        if arr.ndim == 2:
            prefix = key.replace('X_', '')
            for i in range(arr.shape[1]):
                df_data[f"{prefix}_{i:05d}"] = arr[:, i]
            _logger.info(f"  Converted {key}: {arr.shape}")

        # Handle 1D arrays
        elif arr.ndim == 1:
            df_data[key] = arr
            _logger.info(f"  Converted {key}: {arr.shape}")

    # Create DataFrame and save
    df = pd.DataFrame(df_data)
    df.to_parquet(output_parquet_path, compression=compression, index=False)

    _logger.info(
        f"Successfully converted to Parquet: {len(df)} samples, "
        f"{len(df.columns)-1} features"
    )


__all__ = [
    "load_features_from_parquet",
    "load_multiple_feature_sets",
    "convert_npz_to_parquet",
]
