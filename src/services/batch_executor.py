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
from src.utils.path_utils import detect_wsl, wsl_to_windows_path

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
        self.is_wsl = detect_wsl()
        _logger.info(f"BatchExecutor initialized with timeout={timeout}s")
        _logger.info(f"WSL environment detected: {self.is_wsl}")

    def convert_wsl_to_windows_path(self, wsl_path: Path | str) -> str:
        """Convert WSL path to Windows path.

        Deprecated: Use src.utils.path_utils.wsl_to_windows_path instead.

        Args:
            wsl_path: Path in WSL filesystem

        Returns:
            Windows-style path (e.g., C:\\Users\\...)

        Raises:
            BatchExecutionError: If path conversion fails
        """
        try:
            return wsl_to_windows_path(wsl_path)
        except RuntimeError as e:
            raise BatchExecutionError(str(e)) from e

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
            # Get batch file directory for cwd
            # Note: cwd must be in WSL/Linux format (not Windows format)
            # because subprocess.run() needs to access the actual filesystem
            batch_path = Path(batch_file)
            batch_dir = batch_path.parent
            cwd = str(batch_dir)  # Use WSL path for subprocess.run()
            _logger.debug(f"Working directory (WSL): {cwd}")

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

            # Execute command with cwd set to batch file directory
            # Note: Windows cmd.exe output may be in cp932 (Shift-JIS)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=False,  # Get bytes instead of text
                timeout=timeout,
                check=False,  # Don't raise on non-zero exit
                cwd=cwd  # Set working directory (WSL path)
            )

            # Decode output with fallback for Japanese Windows
            try:
                stdout = result.stdout.decode('utf-8')
                stderr = result.stderr.decode('utf-8')
            except UnicodeDecodeError:
                # Try cp932 (Shift-JIS) for Japanese Windows
                try:
                    stdout = result.stdout.decode('cp932')
                    stderr = result.stderr.decode('cp932')
                except UnicodeDecodeError:
                    # Fallback to latin-1 (never fails)
                    stdout = result.stdout.decode('latin-1')
                    stderr = result.stderr.decode('latin-1')

            # Create a new CompletedProcess with decoded text
            result = subprocess.CompletedProcess(
                args=result.args,
                returncode=result.returncode,
                stdout=stdout,
                stderr=stderr
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
