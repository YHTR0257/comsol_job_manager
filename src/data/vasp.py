"""VASP data loading utilities for the ESP project."""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import pandas as pd
import numpy as np
from dataclasses import dataclass

try:
    from pymatgen.io.vasp import Poscar
    from pymatgen.core import Structure
except ImportError as e:
    raise ImportError("pymatgen is required for VASP data loading. Install pymatgen.") from e

from src.config.loader import get_logger


_logger = get_logger("data.vasp")


@dataclass
class VASPCalculation:
    """Container for VASP calculation data."""

    structure: Optional[Structure] = None
    total_energy: Optional[float] = None
    final_energy: Optional[float] = None
    efermi: Optional[float] = None
    converged: Optional[bool] = None
    kpoints: Optional[Dict] = None
    elastic_tensor: Optional[np.ndarray] = None
    elastic_constants: Optional[Dict[str, float]] = None
    metadata: Optional[Dict] = None


def parse_poscar(poscar_path: Union[str, Path]) -> Structure:
    """Parse POSCAR file and return pymatgen Structure.

    Args:
        poscar_path: Path to POSCAR file

    Returns:
        pymatgen Structure object
    """
    poscar_path = Path(poscar_path)
    if not poscar_path.exists():
        raise FileNotFoundError(f"POSCAR file not found: {poscar_path}")

    try:
        poscar = Poscar.from_file(poscar_path)
        return poscar.structure
    except Exception as e:
        _logger.error(f"Failed to parse POSCAR {poscar_path}: {e}")
        raise


def parse_kpoints(kpoints_path: Union[str, Path]) -> Dict:
    """Parse KPOINTS file and extract k-point information.

    Args:
        kpoints_path: Path to KPOINTS file

    Returns:
        Dictionary with k-point information
    """
    kpoints_path = Path(kpoints_path)
    if not kpoints_path.exists():
        raise FileNotFoundError(f"KPOINTS file not found: {kpoints_path}")

    with open(kpoints_path, 'r') as f:
        lines = f.readlines()

    if len(lines) < 4:
        raise ValueError(f"Invalid KPOINTS file format: {kpoints_path}")

    # Line 2: number of k-points (if automatic) or grid size
    kpoints_line = lines[2].strip()

    # Line 3: k-point generation style
    style = lines[3].strip().lower()

    kpoints_info = {"style": style}

    if "gamma" in style or "monkhorst" in style:
        # Automatic k-point generation
        try:
            kx, ky, kz = map(int, kpoints_line.split()[:3])
            kpoints_info.update({
                "kx": kx,
                "ky": ky,
                "kz": kz,
                "total": kx * ky * kz
            })
        except ValueError:
            _logger.warning(f"Could not parse k-point grid from: {kpoints_line}")

    return kpoints_info


def parse_elastic_tensor(elastic_file: Union[str, Path]) -> Tuple[np.ndarray, Dict[str, float]]:
    """Parse elastic tensor file and extract elastic constants.

    Args:
        elastic_file: Path to ELASTIC_TENSOR file

    Returns:
        Tuple of (6x6 elastic tensor array, dict of elastic constants)
    """
    elastic_file = Path(elastic_file)
    if not elastic_file.exists():
        raise FileNotFoundError(f"Elastic tensor file not found: {elastic_file}")

    with open(elastic_file, 'r') as f:
        lines = f.readlines()

    # Find the start of the tensor data (skip header lines)
    tensor_lines = []
    for line in lines[1:]:  # Skip first line (header)
        line = line.strip()
        if line and not line.startswith('#'):
            # Split and convert to float
            try:
                row = [float(x) for x in line.split()]
                if len(row) == 6:  # Valid tensor row
                    tensor_lines.append(row)
            except ValueError:
                continue

    if len(tensor_lines) != 6:
        raise ValueError(f"Expected 6x6 elastic tensor, got {len(tensor_lines)} rows")

    # Create elastic tensor array
    elastic_tensor = np.array(tensor_lines)

    # Extract individual elastic constants
    elastic_constants = {
        "c11": elastic_tensor[0, 0],
        "c12": elastic_tensor[0, 1],
        "c13": elastic_tensor[0, 2],
        "c22": elastic_tensor[1, 1],
        "c23": elastic_tensor[1, 2],
        "c33": elastic_tensor[2, 2],
        "c44": elastic_tensor[3, 3],
        "c55": elastic_tensor[4, 4],
        "c66": elastic_tensor[5, 5]
    }

    return elastic_tensor, elastic_constants


def load_vasp_calculation(calc_dir: Union[str, Path]) -> VASPCalculation:
    """Load VASP calculation data from directory.

    Args:
        calc_dir: Path to VASP calculation directory

    Returns:
        VASPCalculation object with loaded data
    """
    calc_dir = Path(calc_dir)
    if not calc_dir.exists():
        raise FileNotFoundError(f"Calculation directory not found: {calc_dir}")

    _logger.info(f"Loading VASP calculation from: {calc_dir}")

    calc = VASPCalculation()
    calc.metadata = {"calc_dir": str(calc_dir)}

    # Parse POSCAR if present
    poscar_path = calc_dir / "POSCAR"
    if poscar_path.exists():
        try:
            calc.structure = parse_poscar(poscar_path)
            _logger.debug(f"Loaded structure from {poscar_path}")
        except Exception as e:
            _logger.warning(f"Failed to parse POSCAR: {e}")

    # Parse KPOINTS if present
    kpoints_path = calc_dir / "KPOINTS"
    if kpoints_path.exists():
        try:
            calc.kpoints = parse_kpoints(kpoints_path)
            _logger.debug(f"Loaded k-points from {kpoints_path}")
        except Exception as e:
            _logger.warning(f"Failed to parse KPOINTS: {e}")

    # Parse elastic tensor if present
    elastic_path = calc_dir / "ELASTIC_TENSOR"
    if elastic_path.exists():
        try:
            calc.elastic_tensor, calc.elastic_constants = parse_elastic_tensor(elastic_path)
            _logger.debug(f"Loaded elastic tensor from {elastic_path}")
        except Exception as e:
            _logger.warning(f"Failed to parse elastic tensor: {e}")

    return calc


def load_elastic_constants_csv(csv_path: Union[str, Path]) -> pd.DataFrame:
    """Load elastic constants from CSV file.

    Expected format: kpoints,c11,c12,c44 (no header)

    Args:
        csv_path: Path to CSV file

    Returns:
        DataFrame with columns: kpoints, c11, c12, c44
    """
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    try:
        df = pd.read_csv(csv_path, header=None, names=['kpoints', 'c11', 'c12', 'c44'])
        _logger.info(f"Loaded {len(df)} elastic constant records from {csv_path}")
        return df
    except Exception as e:
        _logger.error(f"Failed to load CSV {csv_path}: {e}")
        raise


def analyze_kpoint_convergence(df: pd.DataFrame) -> Dict:
    """Analyze k-point convergence of elastic constants.

    Args:
        df: DataFrame with kpoints and elastic constant columns

    Returns:
        Dictionary with convergence analysis results
    """
    if df.empty:
        return {}

    # Sort by k-points
    df_sorted = df.sort_values('kpoints')

    # Calculate differences between consecutive k-point calculations
    analysis = {
        "kpoints_range": (df_sorted['kpoints'].min(), df_sorted['kpoints'].max()),
        "num_calculations": len(df_sorted),
        "convergence": {}
    }

    for prop in ['c11', 'c12', 'c44']:
        if prop in df_sorted.columns:
            values = df_sorted[prop].values

            # Calculate relative changes
            rel_changes = []
            for i in range(1, len(values)):
                rel_change = abs(values[i] - values[i-1]) / abs(values[i-1]) * 100
                rel_changes.append(rel_change)

            analysis["convergence"][prop] = {
                "final_value": values[-1] if len(values) > 0 else None,
                "std_dev": np.std(values) if len(values) > 1 else 0,
                "max_rel_change": max(rel_changes) if rel_changes else 0,
                "avg_rel_change": np.mean(rel_changes) if rel_changes else 0
            }

    return analysis


__all__ = [
    "VASPCalculation",
    "parse_poscar",
    "parse_kpoints",
    "parse_elastic_tensor",
    "load_vasp_calculation",
    "load_elastic_constants_csv",
    "analyze_kpoint_convergence"
]