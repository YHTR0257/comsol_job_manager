"""Job generator for COMSOL simulations.

This module generates Java simulation files for COMSOL based on the reference
file and parametric study configurations.
"""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from jinja2 import Environment, FileSystemLoader, Template

from src.config.loader import get_logger

_logger = get_logger("services.job_generator")


class JobGenerator:
    """Generate COMSOL simulation jobs from templates and parameters."""

    def __init__(
        self,
        template_dir: Path | str,
        output_base_dir: Path | str,
        reference_java_path: Path | str | None = None
    ):
        """Initialize job generator.

        Args:
            template_dir: Directory containing Jinja2 templates
            output_base_dir: Base directory for job outputs
            reference_java_path: Path to reference Java file (optional)
        """
        self.template_dir = Path(template_dir)
        self.output_base_dir = Path(output_base_dir)
        self.reference_java_path = (
            Path(reference_java_path) if reference_java_path else None
        )

        # Setup Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )

        # Ensure output directory exists
        self.output_base_dir.mkdir(parents=True, exist_ok=True)

        _logger.info(f"JobGenerator initialized with template_dir={self.template_dir}")

    def generate_job_id(self) -> str:
        """Generate unique job ID with timestamp.

        Returns:
            Job ID in format: job_YYYYMMDD_HHMMSS
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"job_{timestamp}"

    def create_job_directory(self, job_id: str) -> Path:
        """Create job working directory.

        Args:
            job_id: Unique job identifier

        Returns:
            Path to created job directory
        """
        job_dir = self.output_base_dir / job_id
        job_dir.mkdir(parents=True, exist_ok=True)

        # Create results subdirectory
        results_dir = job_dir / "results"
        results_dir.mkdir(exist_ok=True)

        _logger.info(f"Created job directory: {job_dir}")
        return job_dir

    def generate_java_from_reference(
        self,
        job_dir: Path,
        params: Dict[str, Any]
    ) -> Path:
        """Generate Java file from reference implementation.

        This uses the reference Java file as a base and injects parameters
        for the geometry section only.

        Args:
            job_dir: Job working directory
            params: Dictionary of parameters for the simulation

        Returns:
            Path to generated Java file

        Raises:
            FileNotFoundError: If reference Java file not found
            ValueError: If required parameters are missing
        """
        if not self.reference_java_path or not self.reference_java_path.exists():
            raise FileNotFoundError(
                f"Reference Java file not found: {self.reference_java_path}"
            )

        _logger.info(f"Generating Java file from reference: {self.reference_java_path}")

        # Read reference file
        with open(self.reference_java_path, 'r', encoding='utf-8') as f:
            java_content = f.read()

        # Extract parameters with defaults
        lattice_constant = params.get('lattice_constant', params.get('lconst', 1.0))
        sphere_radius_ratio = params.get('sphere_radius_ratio', params.get('rs', 0.1))
        bond_radius_ratio = params.get('bond_radius_ratio', params.get('rb', 0.05))
        shift = params.get('shift', 0.0)
        num_cells = params.get('num_cells', params.get('nnn', 3))
        poisson_ratio = params.get('poisson_ratio', params.get('pratio', 0.3))
        delta = params.get('delta', params.get('delta_', 0.001))
        d_min = params.get('d_min', 0.0)
        d_max = params.get('d_max', lattice_constant * 1.5)
        dstep = params.get('dstep', '"range(0,0.0002,0.001)"')

        # Get lattice type and locations
        lattice_type = params.get('lattice_type', 'FCC')
        eps = params.get('eps', 1e-6)

        # Job metadata
        job_id = job_dir.name
        file_name = params.get('file_name', job_id)
        output_path = str(job_dir / "results")

        # Replace placeholders in Java content
        # Note: Order matters for some replacements
        replacements = [
            ('OOO.', str(lattice_constant)),
            ('AAA.', str(sphere_radius_ratio * 100)),
            ('BBB.', str(bond_radius_ratio * 100)),
            ('POISSON.', str(poisson_ratio * 100)),
            ('0.SHIFT', str(shift)),
            ('NNN', str(num_cells)),
        ]

        # Apply replacements
        modified_content = java_content
        for old, new in replacements:
            modified_content = modified_content.replace(old, new)

        # Replace path placeholders (handle after numeric replacements)
        modified_content = modified_content.replace(
            'String path = "H:/kanegae/comsol_ws/hosoda2/DATETAD";',
            f'String path = "{output_path}";'
        )
        modified_content = modified_content.replace(
            'String stlfile = "H:/kanegae/comsol_ws/hosoda2/stl/";',
            'String stlfile = "";'
        )

        # Replace file name in first occurrence
        import re
        modified_content = re.sub(
            r'String file = ".*?";',
            f'String file = "{file_name}";',
            modified_content,
            count=1
        )

        # Generate class name from job_id (sanitize for Java class name)
        class_name = job_id.replace('-', '_').replace('.', '_')

        # Replace class name in the Java file
        # Find the original class name pattern
        import re
        class_pattern = r'public class \w+'
        modified_content = re.sub(
            class_pattern,
            f'public class {class_name}',
            modified_content,
            count=1
        )

        # Write generated Java file
        java_file_path = job_dir / f"{class_name}.java"
        with open(java_file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)

        _logger.info(f"Generated Java file: {java_file_path}")
        return java_file_path

    def generate_batch_file(
        self,
        job_dir: Path,
        java_file_path: Path,
        comsol_command: str = "comsol",
        java_class_name: Optional[str] = None
    ) -> Path:
        """Generate Windows batch file to run COMSOL using Jinja2 template.

        Args:
            job_dir: Job working directory
            java_file_path: Path to generated Java file
            comsol_command: COMSOL command name (default: "comsol")
                          Assumes COMSOL is in Windows PATH
            java_class_name: Java class name (default: inferred from file)

        Returns:
            Path to generated batch file
        """
        if java_class_name is None:
            java_class_name = java_file_path.stem

        # Load template
        template = self.jinja_env.get_template('run.bat.j2')

        # Prepare template variables
        template_vars = {
            'job_id': job_dir.name,
            'job_dir': str(job_dir),
            'java_file_name': java_file_path.name,
            'class_name': java_class_name,
            'output_file': f"{java_class_name}.mph",
            'comsol_command': comsol_command,
            'generated_at': datetime.now().isoformat()
        }

        # Render template
        batch_content = template.render(**template_vars)

        # Write batch file
        batch_file_path = job_dir / "run.bat"
        with open(batch_file_path, 'w', encoding='utf-8') as f:
            f.write(batch_content)

        _logger.info(f"Generated batch file from template: {batch_file_path}")
        return batch_file_path

    def generate_config_file(
        self,
        job_dir: Path,
        params: Dict[str, Any]
    ) -> Path:
        """Generate YAML configuration file for the job.

        Args:
            job_dir: Job working directory
            params: Parameter dictionary

        Returns:
            Path to generated config file
        """
        import yaml

        config_path = job_dir / "config.yml"

        # Create config with metadata
        config = {
            'job_id': job_dir.name,
            'generated_at': datetime.now().isoformat(),
            'parameters': params
        }

        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

        _logger.info(f"Generated config file: {config_path}")
        return config_path

    def generate_job(
        self,
        params: Dict[str, Any],
        comsol_command: str = "comsol",
        job_id: Optional[str] = None
    ) -> Dict[str, Path]:
        """Generate complete job with all necessary files.

        Args:
            params: Simulation parameters
            comsol_command: COMSOL command name (default: "comsol")
                          Assumes COMSOL is in Windows PATH
            job_id: Optional job ID (auto-generated if None)

        Returns:
            Dictionary with paths to generated files:
            - 'job_dir': Job directory path
            - 'java_file': Java source file path
            - 'batch_file': Batch execution file path
            - 'config_file': Configuration file path
        """
        # Generate or use provided job ID
        if job_id is None:
            job_id = self.generate_job_id()

        _logger.info(f"Generating job: {job_id}")

        # Create job directory
        job_dir = self.create_job_directory(job_id)

        # Generate files
        java_file = self.generate_java_from_reference(job_dir, params)
        batch_file = self.generate_batch_file(
            job_dir,
            java_file,
            comsol_command,
            java_class_name=java_file.stem
        )
        config_file = self.generate_config_file(job_dir, params)

        result = {
            'job_dir': job_dir,
            'java_file': java_file,
            'batch_file': batch_file,
            'config_file': config_file
        }

        _logger.info(f"Job generation completed: {job_id}")
        return result


def validate_parameters(params: Dict[str, Any]) -> bool:
    """Validate simulation parameters.

    Args:
        params: Parameter dictionary

    Returns:
        True if valid

    Raises:
        ValueError: If parameters are invalid
    """
    # Required parameters (with aliases)
    required_keys = ['lattice_constant', 'lconst']
    if not any(k in params for k in required_keys):
        raise ValueError("Missing required parameter: lattice_constant (or lconst)")

    # Range validations
    validations = [
        ('lattice_constant', 'lconst', lambda x: 0 < x < 100, "Must be between 0 and 100"),
        ('sphere_radius_ratio', 'rs', lambda x: 0 < x < 0.5, "Must be between 0 and 0.5"),
        ('bond_radius_ratio', 'rb', lambda x: 0 < x < 0.5, "Must be between 0 and 0.5"),
        ('poisson_ratio', 'pratio', lambda x: -1 < x < 0.5, "Must be between -1 and 0.5"),
    ]

    for primary_key, alias_key, validator, msg in validations:
        value = params.get(primary_key, params.get(alias_key))
        if value is not None and not validator(value):
            raise ValueError(f"Invalid {primary_key}: {msg}")

    return True


__all__ = [
    "JobGenerator",
    "validate_parameters"
]
