"""YAML loader for custom lattice job definitions.

This module provides functions to load and parse YAML files containing
custom lattice job definitions, with comprehensive validation and error
reporting.
"""

import yaml
from pathlib import Path
from typing import Union
from pydantic import ValidationError
from ..data.models.custom_lattice import CustomLatticeJob
from ..validators import GeometryValidator, ValidationResult


class YAMLParseError(Exception):
    """Exception raised when YAML parsing or validation fails.

    Attributes:
        message: Error message
        errors: List of specific validation errors (if available)
    """

    def __init__(self, message: str, errors: list = None):
        """Initialize the error.

        Args:
            message: Main error message
            errors: Optional list of detailed errors
        """
        super().__init__(message)
        self.message = message
        self.errors = errors or []

    def __str__(self):
        """Format error message with details."""
        if not self.errors:
            return self.message

        error_details = "\n".join(f"  - {err}" for err in self.errors)
        return f"{self.message}\n{error_details}"


def load_custom_lattice_yaml(
    filepath: Union[str, Path],
    validate_geometry: bool = True,
    strict: bool = True
) -> CustomLatticeJob:
    """Load and validate a custom lattice YAML file.

    This function performs the following steps:
    1. Load YAML file
    2. Parse into Pydantic model (validates schema and data types)
    3. Optionally validate geometry (sphere overlaps, beam connections)

    Args:
        filepath: Path to the YAML file
        validate_geometry: Whether to perform geometric validation
        strict: If True, raise error on geometry warnings; if False, only
                raise on errors

    Returns:
        CustomLatticeJob object containing the parsed job definition

    Raises:
        YAMLParseError: If file cannot be loaded or validation fails
        FileNotFoundError: If the specified file does not exist
    """
    filepath = Path(filepath)

    # Check if file exists
    if not filepath.exists():
        raise FileNotFoundError(f"YAML file not found: {filepath}")

    # Load YAML file
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise YAMLParseError(
            f"Failed to parse YAML file: {filepath}",
            [str(e)]
        )
    except Exception as e:
        raise YAMLParseError(
            f"Failed to read file: {filepath}",
            [str(e)]
        )

    # Parse into Pydantic model
    try:
        job = CustomLatticeJob(**data)
    except ValidationError as e:
        errors = []
        for error in e.errors():
            loc = " -> ".join(str(x) for x in error['loc'])
            errors.append(f"{loc}: {error['msg']}")

        raise YAMLParseError(
            f"YAML validation failed for: {filepath}",
            errors
        )

    # Perform geometric validation
    if validate_geometry:
        validator = GeometryValidator()
        result = validator.validate(job.geometry)

        if not result.is_valid:
            errors = [err.message for err in result.errors]
            raise YAMLParseError(
                f"Geometry validation failed for: {filepath}",
                errors
            )

        if strict and result.warnings:
            warnings = [warn.message for warn in result.warnings]
            raise YAMLParseError(
                f"Geometry validation warnings (strict mode) for: {filepath}",
                warnings
            )

    return job


def validate_yaml_file(filepath: Union[str, Path]) -> ValidationResult:
    """Validate a YAML file without loading it completely.

    This is useful for checking files before processing them.

    Args:
        filepath: Path to the YAML file

    Returns:
        ValidationResult with any errors or warnings found

    Raises:
        FileNotFoundError: If the file does not exist
        YAMLParseError: If YAML parsing fails
    """
    try:
        job = load_custom_lattice_yaml(
            filepath,
            validate_geometry=True,
            strict=False
        )
        validator = GeometryValidator()
        return validator.validate(job.geometry)
    except YAMLParseError as e:
        # Convert parse errors to validation result
        from ..validators import ValidationError as ValError
        errors = [
            ValError(
                error_type='parse_error',
                message=err,
                element_ids=[],
                severity='error'
            )
            for err in e.errors
        ]
        from ..validators import ValidationResult
        return ValidationResult(
            is_valid=False,
            errors=errors,
            warnings=[]
        )


def get_job_summary(job: CustomLatticeJob) -> str:
    """Get a human-readable summary of a job definition.

    Args:
        job: CustomLatticeJob object

    Returns:
        Formatted string with job summary
    """
    lines = [
        f"Job: {job.job.name}",
        f"Description: {job.job.description}",
        f"Unit Cell: {job.job.unit_cell_size} mm",
        f"",
        f"Geometry:",
        f"  Lattice constant: {job.geometry.lattice_constant} mm",
        f"  Spheres: {len(job.geometry.spheres)}",
        f"  Beams: {len(job.geometry.beams)}",
        f"",
        f"Materials: {', '.join(job.materials.keys())}",
        f"",
        f"Mesh:",
        f"  Type: {job.mesh.type}",
        f"  Size: {job.mesh.size}",
        f"",
        f"Study:",
        f"  Strain delta: {job.study.strain.delta}",
        f"  Strain steps: {job.study.strain.steps}",
        f"",
        f"Parametric Study:",
        f"  Default parameters: {len(job.job.parametric.default)}",
        f"  Sweeps: {len(job.job.parametric.sweeps)}",
    ]

    for idx, sweep in enumerate(job.job.parametric.sweeps, 1):
        lines.append(
            f"    Sweep {idx}: {sweep.parameter} "
            f"({len(sweep.values)} values: {sweep.values})"
        )

    return "\n".join(lines)
