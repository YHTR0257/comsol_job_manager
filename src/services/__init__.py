"""Services module for COMSOL job management.

This module provides services for generating, executing, and analyzing
COMSOL simulation jobs.
"""

from src.services.job_generator import JobGenerator, validate_parameters
from src.services.batch_executor import BatchExecutor, BatchExecutionError, execute_job

__all__ = [
    "JobGenerator",
    "validate_parameters",
    "BatchExecutor",
    "BatchExecutionError",
    "execute_job",
]
