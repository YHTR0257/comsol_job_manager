"""Services module for COMSOL job management.

This module provides services for generating, executing, and analyzing
COMSOL simulation jobs.
"""

from src.services.job_generator import JobGenerator, validate_parameters

__all__ = [
    "JobGenerator",
    "validate_parameters",
]
