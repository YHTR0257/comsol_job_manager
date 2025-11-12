"""LOBSTER data loading utilities."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import numpy as np
import pandas as pd


@dataclass
class ICOBIData:
    """Container for ICOBILIST data.

    Attributes
    ----------
    cobi_index : np.ndarray
        COBI indices (integer array)
    atom_mu : np.ndarray
        First atom labels (object array)
    atom_nu : np.ndarray
        Second atom labels (object array)
    distance : np.ndarray
        Bond distances in Angstroms (float array)
    translation : np.ndarray
        Translation vectors (n_bonds, 3) integer array
    icobi_spin1 : np.ndarray
        ICOBI values for spin 1 (float array)
    icobi_spin2 : Optional[np.ndarray]
        ICOBI values for spin 2 (float array, None if non-spin-polarized)
    """
    cobi_index: np.ndarray
    atom_mu: np.ndarray
    atom_nu: np.ndarray
    distance: np.ndarray
    translation: np.ndarray
    icobi_spin1: np.ndarray
    icobi_spin2: Optional[np.ndarray] = None


def find_icobilist_file(path: os.PathLike | str) -> Path:
    """Resolve an ICOBILIST file under a directory or file path.

    Accepts either a direct file path or a directory containing ICOBILIST files.
    """
    p = Path(path)
    if p.is_file():
        return p

    # Common LOBSTER filename patterns
    candidates = [
        p / "ICOBILIST.lobster",
        p / "ICOBILIST",
        p / "ICOBILIST.gz",
    ]
    for c in candidates:
        if c.exists():
            return c

    # Fall back to first file that contains 'ICOBILIST' in name
    for child in p.iterdir():
        if child.is_file() and "ICOBILIST" in child.name.upper():
            return child

    raise FileNotFoundError(f"ICOBILIST file not found under {p}")


def load_icobilist(path: os.PathLike | str) -> ICOBIData:
    """Load ICOBILIST.lobster file from LOBSTER calculation.

    Parameters
    ----------
    path : Directory containing ICOBILIST.lobster or direct path to the file

    Returns
    -------
    ICOBIData
        Dataclass containing parsed ICOBILIST data
    """
    file_path = find_icobilist_file(path)

    # Read the file, skipping the header (first 2 lines)
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Parse header to detect number of columns
    # Header line 1: column names
    # Header line 2: spin labels (if spin-polarized)
    header_line = lines[0].strip()

    # Detect if spin-polarized (two ICOBI columns)
    is_spin_polarized = "for spin" in lines[1] if len(lines) > 1 else False

    # Parse data lines (skip first 2 header lines)
    data_lines = [line for line in lines[2:] if line.strip()]

    if not data_lines:
        raise ValueError(f"No data found in ICOBILIST file: {file_path}")

    # Parse each line
    cobi_indices = []
    atom_mus = []
    atom_nus = []
    distances = []
    translations = []
    icobi_spin1_vals = []
    icobi_spin2_vals = []

    for line in data_lines:
        parts = line.split()
        if len(parts) < 7:
            continue  # Skip malformed lines

        try:
            cobi_idx = int(parts[0])
            atom_mu = parts[1]
            atom_nu = parts[2]
            dist = float(parts[3])
            trans_x = int(parts[4])
            trans_y = int(parts[5])
            trans_z = int(parts[6])
            icobi_s1 = float(parts[7])

            cobi_indices.append(cobi_idx)
            atom_mus.append(atom_mu)
            atom_nus.append(atom_nu)
            distances.append(dist)
            translations.append([trans_x, trans_y, trans_z])
            icobi_spin1_vals.append(icobi_s1)

            if is_spin_polarized and len(parts) >= 9:
                icobi_s2 = float(parts[8])
                icobi_spin2_vals.append(icobi_s2)
        except (ValueError, IndexError):
            continue  # Skip lines that can't be parsed

    # Convert to numpy arrays
    cobi_index = np.array(cobi_indices, dtype=np.int32)
    atom_mu = np.array(atom_mus, dtype=object)
    atom_nu = np.array(atom_nus, dtype=object)
    distance = np.array(distances, dtype=np.float32)
    translation = np.array(translations, dtype=np.int32)
    icobi_spin1 = np.array(icobi_spin1_vals, dtype=np.float32)
    icobi_spin2 = np.array(icobi_spin2_vals, dtype=np.float32) if is_spin_polarized else None

    return ICOBIData(
        cobi_index=cobi_index,
        atom_mu=atom_mu,
        atom_nu=atom_nu,
        distance=distance,
        translation=translation,
        icobi_spin1=icobi_spin1,
        icobi_spin2=icobi_spin2
    )


def get_nearest_neighbor_summary(cobi_data: ICOBIData,
                                  n_neighbors: int = 2) -> dict[str, Any]:
    """Extract nearest neighbor ICOBI statistics.

    Parameters
    ----------
    cobi_data : ICOBIData
        Loaded ICOBILIST data
    n_neighbors : int
        Number of nearest neighbor shells to analyze

    Returns
    -------
    dict
        Dictionary with statistics for each neighbor shell:
        - 'nn{i}_distance_mean': mean distance for i-th shell
        - 'nn{i}_icobi_mean': mean ICOBI for i-th shell (averaged over spins)
        - 'nn{i}_icobi_std': std ICOBI for i-th shell
    """
    # Group by distance (with small tolerance for numerical precision)
    distances_unique = np.unique(np.round(cobi_data.distance, decimals=4))

    stats = {}
    for i in range(min(n_neighbors, len(distances_unique))):
        dist = distances_unique[i]
        mask = np.abs(cobi_data.distance - dist) < 0.01  # 0.01 Angstrom tolerance

        # Average ICOBI over spins if spin-polarized
        if cobi_data.icobi_spin2 is not None:
            icobi_vals = (cobi_data.icobi_spin1[mask] + cobi_data.icobi_spin2[mask]) / 2
        else:
            icobi_vals = cobi_data.icobi_spin1[mask]

        nn_label = i + 1  # 1-indexed (1st NN, 2nd NN, etc.)
        stats[f'nn{nn_label}_distance_mean'] = float(np.mean(cobi_data.distance[mask]))
        stats[f'nn{nn_label}_icobi_mean'] = float(np.mean(icobi_vals))
        stats[f'nn{nn_label}_icobi_std'] = float(np.std(icobi_vals))

    return stats


__all__ = [
    "ICOBIData",
    "find_icobilist_file",
    "load_icobilist",
    "get_nearest_neighbor_summary",
]
