"""Batch executor for running COMSOL jobs on Windows from WSL.

This module provides functionality to execute Windows batch files from WSL,
handling path conversion and process management.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional
import time

from src.config.loader import get_logger

_logger = get_logger("services.batch_executor")


class BatchExecutionError(Exception):
    """Exception raised when batch execution fails."""
    pass


class BatchExecutor:
    """Execute Windows batch files from WSL/Linux."""

    def __init__(self, timeout: int = 3600):
        """Initialize batch executor.

        Args:
            timeout: Default timeout in seconds (default: 1 hour)
        """
        self.default_timeout = timeout
        self.is_wsl = self._detect_wsl()
        _logger.info(f"BatchExecutor initialized with timeout={timeout}s")
        _logger.info(f"WSL environment detected: {self.is_wsl}")

    def _detect_wsl(self) -> bool:
        """Detect if running in WSL environment.

        Returns:
            True if running in WSL, False otherwise
        """
        try:
            # Check for WSL-specific files
            import os
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

    def convert_wsl_to_windows_path(self, wsl_path: Path | str) -> str:
        """Convert WSL path to Windows path.

        Args:
            wsl_path: Path in WSL filesystem

        Returns:
            Windows-style path (e.g., C:\\Users\\...)

        Raises:
            BatchExecutionError: If path conversion fails
        """
        wsl_path = str(wsl_path)

        # If not in WSL, return path as-is
        if not self.is_wsl:
            _logger.debug(f"Not in WSL, using path as-is: {wsl_path}")
            return wsl_path

        try:
            result = subprocess.run(
                ['wslpath', '-w', wsl_path],
                capture_output=True,
                text=True,
                timeout=10,
                check=True
            )
            windows_path = result.stdout.strip()
            _logger.debug(f"Converted path: {wsl_path} -> {windows_path}")
            return windows_path

        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to convert path: {e.stderr}"
            _logger.error(error_msg)
            raise BatchExecutionError(error_msg) from e

        except subprocess.TimeoutExpired as e:
            error_msg = "Path conversion timed out"
            _logger.error(error_msg)
            raise BatchExecutionError(error_msg) from e

        except FileNotFoundError:
            # wslpath not found, fallback to direct path
            _logger.warning("wslpath not found, using path as-is")
            return wsl_path

    def execute_batch(
        self,
        batch_file: Path | str,
        timeout: Optional[int] = None,
        convert_path: bool = True
    ) -> subprocess.CompletedProcess:
        """Execute Windows batch file from WSL.

        Args:
            batch_file: Path to .bat file (WSL or Windows path)
            timeout: Timeout in seconds (uses default if None)
            convert_path: Convert WSL path to Windows path (default: True)

        Returns:
            CompletedProcess with returncode, stdout, stderr

        Raises:
            BatchExecutionError: If execution fails
            subprocess.TimeoutExpired: If execution times out
        """
        timeout = timeout or self.default_timeout

        # Convert path if needed
        if convert_path:
            batch_file_str = self.convert_wsl_to_windows_path(batch_file)
        else:
            batch_file_str = str(batch_file)

        _logger.info(f"Executing batch file: {batch_file_str}")
        _logger.info(f"Timeout: {timeout}s")

        start_time = time.time()

        try:
            # Check if cmd.exe is available (WSL environment)
            if self.is_wsl:
                cmd = ['cmd.exe', '/c', batch_file_str]
            else:
                # In non-WSL Linux, we can't execute Windows batch files
                # This is mainly for testing/development
                _logger.warning("Not in WSL environment - batch execution may fail")
                _logger.warning("For actual COMSOL execution, use WSL or Windows")

                # Try to execute directly (will fail for .bat files)
                cmd = [batch_file_str]

            # Execute command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False  # Don't raise on non-zero exit
            )

            elapsed = time.time() - start_time

            _logger.info(f"Batch execution completed in {elapsed:.1f}s")
            _logger.info(f"Exit code: {result.returncode}")

            if result.returncode != 0:
                _logger.warning(f"Batch file exited with non-zero code: {result.returncode}")
                _logger.debug(f"STDOUT:\n{result.stdout}")
                _logger.debug(f"STDERR:\n{result.stderr}")

            return result

        except subprocess.TimeoutExpired as e:
            elapsed = time.time() - start_time
            error_msg = f"Batch execution timed out after {elapsed:.1f}s"
            _logger.error(error_msg)
            raise

        except Exception as e:
            error_msg = f"Unexpected error during batch execution: {e}"
            _logger.error(error_msg)
            raise BatchExecutionError(error_msg) from e

    def execute_batch_async(
        self,
        batch_file: Path | str,
        convert_path: bool = True
    ) -> subprocess.Popen:
        """Execute batch file asynchronously (non-blocking).

        Args:
            batch_file: Path to .bat file
            convert_path: Convert WSL path to Windows path (default: True)

        Returns:
            Popen process object (can be monitored/terminated)

        Raises:
            BatchExecutionError: If execution fails to start
        """
        # Convert path if needed
        if convert_path:
            batch_file_str = self.convert_wsl_to_windows_path(batch_file)
        else:
            batch_file_str = str(batch_file)

        _logger.info(f"Starting async batch execution: {batch_file_str}")

        try:
            process = subprocess.Popen(
                ['cmd.exe', '/c', batch_file_str],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            _logger.info(f"Batch process started with PID: {process.pid}")
            return process

        except Exception as e:
            error_msg = f"Failed to start batch process: {e}"
            _logger.error(error_msg)
            raise BatchExecutionError(error_msg) from e

    def check_comsol_available(self) -> bool:
        """Check if COMSOL command is available in Windows PATH.

        Returns:
            True if COMSOL is available, False otherwise
        """
        try:
            result = subprocess.run(
                ['cmd.exe', '/c', 'where', 'comsol'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                comsol_path = result.stdout.strip()
                _logger.info(f"COMSOL found at: {comsol_path}")
                return True
            else:
                _logger.warning("COMSOL not found in Windows PATH")
                return False

        except Exception as e:
            _logger.error(f"Error checking COMSOL availability: {e}")
            return False


def execute_job(
    job_dir: Path | str,
    timeout: int = 3600
) -> subprocess.CompletedProcess:
    """Convenience function to execute a job's run.bat file.

    Args:
        job_dir: Job directory containing run.bat
        timeout: Timeout in seconds

    Returns:
        CompletedProcess with execution results

    Raises:
        BatchExecutionError: If batch file not found or execution fails
        subprocess.TimeoutExpired: If execution times out
    """
    job_dir = Path(job_dir)
    batch_file = job_dir / "run.bat"

    if not batch_file.exists():
        raise BatchExecutionError(f"Batch file not found: {batch_file}")

    executor = BatchExecutor(timeout=timeout)
    return executor.execute_batch(batch_file)


__all__ = [
    "BatchExecutor",
    "BatchExecutionError",
    "execute_job"
]
