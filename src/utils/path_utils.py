"""Path utility functions for WSL-Windows path conversion.

This module provides utilities for converting between WSL and Windows paths,
which is essential for running Windows applications (like COMSOL) from WSL.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Optional

from src.config.loader import get_logger

_logger = get_logger("utils.path_utils")


def detect_wsl() -> bool:
    """Detect if running in WSL environment.

    Returns:
        True if running in WSL, False otherwise
    """
    try:
        # Check for WSL-specific files
        if os.path.exists('/proc/version'):
            with open('/proc/version', 'r') as f:
                version = f.read().lower()
                if 'microsoft' in version or 'wsl' in version:
                    return True

        # Check if wslpath command exists
        result = subprocess.run(
            ['which', 'wslpath'],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0

    except Exception:
        return False


def wsl_to_windows_path(wsl_path: Path | str) -> str:
    """Convert WSL path to Windows path.

    Args:
        wsl_path: Path in WSL filesystem (e.g., /home/user/file.txt)

    Returns:
        Windows-style path (e.g., C:\\Users\\user\\file.txt or
        \\\\wsl.localhost\\Ubuntu\\home\\user\\file.txt)

    Raises:
        RuntimeError: If path conversion fails

    Examples:
        >>> wsl_to_windows_path('/home/user/data.txt')
        'C:\\\\Users\\\\user\\\\data.txt'
        >>> wsl_to_windows_path('/mnt/c/data')
        'C:\\\\data'
    """
    wsl_path_str = str(wsl_path)

    # If not in WSL, return path as-is
    if not detect_wsl():
        _logger.debug(f"Not in WSL, using path as-is: {wsl_path_str}")
        return wsl_path_str

    try:
        result = subprocess.run(
            ['wslpath', '-w', wsl_path_str],
            capture_output=True,
            text=True,
            timeout=10,
            check=True
        )
        windows_path = result.stdout.strip()
        _logger.debug(f"Converted path: {wsl_path_str} -> {windows_path}")
        return windows_path

    except subprocess.CalledProcessError as e:
        error_msg = f"Failed to convert path '{wsl_path_str}': {e.stderr}"
        _logger.error(error_msg)
        raise RuntimeError(error_msg) from e

    except subprocess.TimeoutExpired as e:
        error_msg = f"Path conversion timed out for '{wsl_path_str}'"
        _logger.error(error_msg)
        raise RuntimeError(error_msg) from e

    except FileNotFoundError:
        # wslpath not found, return path as-is with warning
        _logger.warning("wslpath command not found, using path as-is")
        return wsl_path_str


def windows_to_wsl_path(windows_path: str) -> str:
    """Convert Windows path to WSL path.

    Args:
        windows_path: Windows-style path (e.g., C:\\Users\\user\\file.txt)

    Returns:
        WSL path (e.g., /mnt/c/Users/user/file.txt)

    Raises:
        RuntimeError: If path conversion fails

    Examples:
        >>> windows_to_wsl_path('C:\\\\Users\\\\user\\\\data.txt')
        '/mnt/c/Users/user/data.txt'
    """
    # If not in WSL, return path as-is
    if not detect_wsl():
        _logger.debug(f"Not in WSL, using path as-is: {windows_path}")
        return windows_path

    try:
        result = subprocess.run(
            ['wslpath', '-u', windows_path],
            capture_output=True,
            text=True,
            timeout=10,
            check=True
        )
        wsl_path = result.stdout.strip()
        _logger.debug(f"Converted path: {windows_path} -> {wsl_path}")
        return wsl_path

    except subprocess.CalledProcessError as e:
        error_msg = f"Failed to convert path '{windows_path}': {e.stderr}"
        _logger.error(error_msg)
        raise RuntimeError(error_msg) from e

    except subprocess.TimeoutExpired as e:
        error_msg = f"Path conversion timed out for '{windows_path}'"
        _logger.error(error_msg)
        raise RuntimeError(error_msg) from e

    except FileNotFoundError:
        # wslpath not found, return path as-is with warning
        _logger.warning("wslpath command not found, using path as-is")
        return windows_path


def normalize_path_for_platform(path: Path | str) -> str:
    """Normalize path for the current platform.

    If running in WSL and the path needs to be used by Windows applications,
    this function will convert it to Windows format. Otherwise, it returns
    the path as a string.

    Args:
        path: Path to normalize

    Returns:
        Normalized path string suitable for the current platform

    Examples:
        >>> normalize_path_for_platform('/home/user/data.txt')
        'C:\\\\Users\\\\user\\\\data.txt'  # In WSL
        >>> normalize_path_for_platform('/home/user/data.txt')
        '/home/user/data.txt'  # In native Linux
    """
    path_str = str(path)

    # In WSL, convert to Windows path for cross-platform compatibility
    if detect_wsl():
        return wsl_to_windows_path(path_str)

    return path_str


__all__ = [
    'detect_wsl',
    'wsl_to_windows_path',
    'windows_to_wsl_path',
    'normalize_path_for_platform',
]
