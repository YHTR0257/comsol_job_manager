from __future__ import annotations

import os
from dataclasses import dataclass
import logging
from pathlib import Path
from typing import Optional, Tuple, Any


@dataclass
class ELFData:
    """Container for loaded ELF grid and structure.

    Attributes
    ----------
    structure: pymatgen.core.Structure
        The atomic structure associated with the grid.
    grid: np.ndarray
        3D array (nx, ny, nz) of the ELF values in fractional grid coordinates.
    origin: np.ndarray
        Origin in Cartesian coordinates (Angstrom). Typically [0,0,0] for VASP grids.
    """

    from typing import Any as _Any  # local alias to avoid exposing in __all__
    structure: _Any  # avoid hard dependency on pymatgen types at import time
    grid: Any
    origin: Any


def _require_pymatgen():
    try:
        from pymatgen.io.vasp import Chgcar  # type: ignore
    except Exception as e:  # pragma: no cover - handled at runtime with clearer error
        raise ImportError(
            "pymatgen is required for ELF loading. Please install it (e.g., pip install pymatgen)."
        ) from e
    return Chgcar


def find_elf_file(path: os.PathLike | str) -> Path:
    """Resolve an ELF-like file under a directory or file path.

    Accepts either a direct file path to ELFCAR/CHGCAR-like file or a directory
    containing "ELFCAR". If not found, raises FileNotFoundError.
    """
    p = Path(path)
    if p.is_file():
        return p
    # Common default filename from VASP
    candidates = [p / "ELFCAR", p / "CHGCAR.ELF", p / "ELFCAR.gz", p / "ELFCAR.bz2"]
    for c in candidates:
        if c.exists():
            return c
    # Fall back to first file that contains 'ELF' in name
    for child in p.iterdir():
        if child.is_file() and "ELF" in child.name.upper():
            return child
    raise FileNotFoundError(f"ELF file not found under {p}")


def load_elf(path: os.PathLike | str) -> ELFData:
    """Load an ELF grid using pymatgen from a VASP ELFCAR-like file.

    Parameters
    ----------
    path: Directory containing ELFCAR or a direct path to the file.

    Returns
    -------
    ELFData
        Dataclass with structure, grid (numpy float32), and origin.
    """
    Chgcar = _require_pymatgen()
    
    file_path = find_elf_file(path)
    chg = Chgcar.from_file(str(file_path))

    # In VASP, ELFCAR is stored in chgcar.data["total"] as a 3D array.
    # pymatgen exposes arrays with order (nx, ny, nz)
    data = chg.data.get("total")
    if data is None:
        # Some files may store as 'elf' depending on writer. Try alternatives.
        data = chg.data.get("elf") or chg.data.get("chg")
    if data is None:
        raise ValueError("ELF grid not found in file. Keys present: " + ", ".join(chg.data.keys()))

    # Lazy import to avoid hard dependency during static analysis
    import numpy as np  # type: ignore

    grid = np.asarray(data, dtype=np.float32)

    # Clip ELF values to [0, 1] range
    # ELF (Electron Localization Function) is theoretically bounded in [0, 1]
    # but numerical artifacts may cause values slightly outside this range
    grid = np.clip(grid, 0.0, 1.0)

    origin = np.zeros(3, dtype=np.float32)

    return ELFData(structure=chg.structure, grid=grid, origin=origin)


def load_elf_with_spacing(path: os.PathLike | str) -> Tuple[ELFData, Any]:
    """Load ELF and compute Cartesian voxel spacings along a, b, c directions.

    Returns (ELFData, spacings[3]) where spacings are approximate voxel sizes
    in Angstrom along lattice vectors. Useful for visualization/interpolation.
    """
    import numpy as np  # type: ignore

    elf = load_elf(path)
    # Lattice vectors (3x3), rows are a, b, c in Cartesian (Angstrom)
    lattice = np.array(elf.structure.lattice.matrix, dtype=float)
    nx, ny, nz = elf.grid.shape[:3]
    spacings = np.array([np.linalg.norm(lattice[0]) / nx,
                         np.linalg.norm(lattice[1]) / ny,
                         np.linalg.norm(lattice[2]) / nz], dtype=float)
    return elf, spacings


__all__ = [
    "ELFData",
    "find_elf_file",
    "load_elf",
    "load_elf_with_spacing",
    # serialization
    "elf_to_npz",
    # resampling
    "resample_grid_linear",
    "resample_elf",
    "resize_to_match",
    "interpolate_nd_linear",
]


def _structure_to_metadata(structure) -> dict[str, Any]:
    """Extract minimal structure metadata for serialization.

    Returns keys: lattice (3x3), species (list[str]), frac_coords (n,3), formula (str)
    """
    import numpy as np  # type: ignore

    return {
        "lattice": np.asarray(structure.lattice.matrix, dtype=float),
        "species": [str(sp) for sp in structure.species],
        "frac_coords": np.asarray(structure.frac_coords, dtype=float),
        "formula": str(structure.composition.reduced_formula),
    }


def elf_to_npz(input_path: os.PathLike | str,
               output: os.PathLike | str | None = None,
               include_spacing: bool = False,
               compress: bool = True) -> str:
    """Load ELFCAR-like file and save as NPZ.

    Parameters
    ----------
    input_path : path to ELFCAR file or its directory
    output : desired .npz output path (default: <input>.npz or <dir>/ELFCAR.npz)
    include_spacing : include voxel spacings along a,b,c
    compress : use numpy.savez_compressed when True

    Returns
    -------
    str : path to the written NPZ file
    """
    import numpy as np  # type: ignore

    in_path = Path(input_path)
    if include_spacing:
        elf, spacings = load_elf_with_spacing(in_path)
    else:
        elf = load_elf(in_path)
        spacings = None

    meta = _structure_to_metadata(elf.structure)

    if output is None:
        out_path = Path(str(in_path))
        if out_path.is_dir():
            out_path = out_path / "ELFCAR.npz"
        if out_path.suffix.lower() != ".npz":
            out_path = out_path.with_suffix(".npz")
    else:
        out_path = Path(output)

    arrays: dict[str, Any] = {
        "grid": np.asarray(elf.grid, dtype=np.float32),
        "origin": np.asarray(elf.origin, dtype=np.float32),
        "lattice": np.asarray(meta["lattice"], dtype=np.float64),
        "species": np.array(meta["species"], dtype=object),
        "frac_coords": np.asarray(meta["frac_coords"], dtype=np.float64),
        "formula": np.array(meta["formula"], dtype=object),
    }
    if spacings is not None:
        arrays["spacings"] = np.asarray(spacings, dtype=np.float64)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    if compress:
        np.savez_compressed(out_path, **arrays)
    else:
        np.savez(out_path, **arrays)

    return str(out_path)


# ---- Resampling utilities ----

def _compute_axis_indices(n_src: int, n_dst: int, align_corners: bool = True):
    import numpy as np  # type: ignore

    if n_dst <= 0:
        raise ValueError("n_dst must be positive")
    if n_src <= 0:
        raise ValueError("n_src must be positive")

    if n_dst == 1:
        # All points map to 0
        x = np.zeros(1, dtype=float)
    else:
        if align_corners:
            x = np.linspace(0, n_src - 1, n_dst, dtype=float)
        else:
            # half-pixel convention
            x = (np.arange(n_dst, dtype=float) + 0.5) * (n_src / n_dst) - 0.5
            x = np.clip(x, 0.0, n_src - 1)

    i0 = np.floor(x).astype(int)
    i1 = np.clip(i0 + 1, 0, n_src - 1)
    w1 = x - i0
    w0 = 1.0 - w1
    return i0, i1, w0, w1


def resample_grid_linear(grid: Any, target_shape: tuple[int, int, int], align_corners: bool = True):
    """Trilinear resampling of a 3D grid to a target shape.

    Parameters
    ----------
    grid : np.ndarray of shape (nx, ny, nz)
    target_shape : (nx', ny', nz')
    align_corners : If True, map endpoints exactly (like many DL libs).

    Returns
    -------
    np.ndarray of shape target_shape, dtype float32
    """
    import numpy as np  # type: ignore

    g = np.asarray(grid, dtype=float)
    if g.ndim != 3:
        raise ValueError("grid must be 3D (nx, ny, nz)")
    nx, ny, nz = g.shape
    tx, ty, tz = target_shape

    ix0, ix1, wx0, wx1 = _compute_axis_indices(nx, tx, align_corners)
    iy0, iy1, wy0, wy1 = _compute_axis_indices(ny, ty, align_corners)
    iz0, iz1, wz0, wz1 = _compute_axis_indices(nz, tz, align_corners)

    # Interpolate along x
    gx0 = np.take(g, ix0, axis=0)  # (tx, ny, nz)
    gx1 = np.take(g, ix1, axis=0)
    gx = gx0 * wx0[:, None, None] + gx1 * wx1[:, None, None]

    # Interpolate along y
    gy0 = np.take(gx, iy0, axis=1)  # (tx, ty, nz)
    gy1 = np.take(gx, iy1, axis=1)
    gy = gy0 * wy0[None, :, None] + gy1 * wy1[None, :, None]

    # Interpolate along z
    gz0 = np.take(gy, iz0, axis=2)  # (tx, ty, tz)
    gz1 = np.take(gy, iz1, axis=2)
    gz = gz0 * wz0[None, None, :] + gz1 * wz1[None, None, :]

    return gz.astype(np.float32, copy=False)


def resample_elf(elf: ELFData, target_shape: tuple[int, int, int], align_corners: bool = True) -> ELFData:
    """Return a new ELFData with grid resampled to target_shape."""
    new_grid = resample_grid_linear(elf.grid, target_shape, align_corners=align_corners)
    return ELFData(structure=elf.structure, grid=new_grid, origin=elf.origin)


def resize_to_match(elf: ELFData, reference: ELFData, align_corners: bool = True) -> ELFData:
    """Resize an ELF grid to match another ELF grid's shape."""
    ref_shape = reference.grid.shape
    return resample_elf(elf, ref_shape, align_corners=align_corners)


def interpolate_nd_linear(data: Any,
                          new_points: tuple[int, ...] | list[int],
                          align_corners: bool = True) -> Any:
    """Generic N-D linear interpolation using SciPy RegularGridInterpolator.

    Parameters
    ----------
    data : np.ndarray
        N-D input array (1 <= N <= 4 supported here).
    new_points : tuple/list of ints
        Target resolution along each axis.
    align_corners : bool
        If True, sample includes exact endpoints [0, 1] along each axis.

    Returns
    -------
    np.ndarray with shape equal to new_points
    """
    import numpy as np  # type: ignore
    logger = logging.getLogger("esp.data.elf")

    try:
        from scipy.interpolate import RegularGridInterpolator as RGI  # type: ignore
    except Exception as e:
        raise ImportError("SciPy is required for interpolate_nd_linear. Install scipy.") from e

    try:
        data = np.asarray(data)
        ndim = data.ndim
        if not (1 <= ndim <= 4):
            raise ValueError(f"Unsupported number of dimensions: {ndim}")

        new_points = tuple(int(n) for n in new_points)
        if len(new_points) != ndim:
            raise ValueError(f"new_points length ({len(new_points)}) must equal data.ndim ({ndim})")

        # Coordinate axes in [0,1]
        coords = []
        for i in range(ndim):
            n = data.shape[i]
            if align_corners:
                coords.append(np.linspace(0.0, 1.0, n))
            else:
                # center-of-cell sampling
                coords.append((np.arange(n, dtype=float) + 0.5) / n)

        interpolar = RGI(tuple(coords), data, method="linear", bounds_error=False, fill_value=None)

        # Build mesh grid for target shape
        slices = [slice(0.0, 1.0, complex(n)) for n in new_points]
        mesh = np.mgrid[tuple(slices)]  # shape (ndim, N0, N1, ...)
        points = np.moveaxis(mesh, 0, -1).reshape(-1, ndim)

        values = interpolar(points)
        interpolated_data = values.reshape(new_points).astype(np.float32, copy=False)

        logger.info(f"Successfully interpolated to shape {interpolated_data.shape}")
        return interpolated_data
    except Exception as e:
        error_msg = f"Interpolation failed: {str(e)}"
        logger.error(error_msg)
        raise ValueError(error_msg) from e

