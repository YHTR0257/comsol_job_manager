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
from src.utils.path_utils import detect_wsl, wsl_to_windows_path
from src.validators.template_validator import validate_generated_java

_logger = get_logger("services.job_generator")


class JobGenerator:
    """Generate COMSOL simulation jobs from templates and parameters."""

    def __init__(
        self,
        template_dir: Path | str,
        output_base_dir: Path | str
    ):
        """Initialize job generator.

        Args:
            template_dir: Directory containing Jinja2 templates
                         (must contain simulation.java.j2 and run.bat.j2)
            output_base_dir: Base directory for job outputs
        """
        self.template_dir = Path(template_dir)
        self.output_base_dir = Path(output_base_dir)

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

    def generate_java_from_template(
        self,
        job_dir: Path,
        params: Dict[str, Any]
    ) -> Path:
        """Generate Java file from Jinja2 template.

        Args:
            job_dir: Job working directory
            params: Dictionary of parameters for the simulation

        Returns:
            Path to generated Java file

        Raises:
            ValueError: If required parameters are missing
        """
        _logger.info(f"Generating Java file from template for job: {job_dir.name}")

        # Load template
        template = self.jinja_env.get_template('simulation.java.j2')

        # Extract parameters with defaults
        lattice_constant = params.get('lattice_constant', params.get('lconst', 1.0))
        sphere_radius_ratio = params.get('sphere_radius_ratio', params.get('rs', 0.1))
        bond_radius_ratio = params.get('bond_radius_ratio', params.get('rb', 0.05))
        shift = params.get('shift', 0.0)
        num_cells = params.get('num_cells', params.get('nnn', 3))
        poisson_ratio = params.get('poisson_ratio', params.get('pratio', 0.3))
        delta = params.get('delta', params.get('delta_', 0.001))
        dstep = params.get('dstep', '"range(0,0.0002,0.001)"')
        lattice_type = params.get('lattice_type', 'FCC').lower()

        # Job metadata
        job_id = job_dir.name
        file_name = params.get('file_name', job_id)
        output_path = str(job_dir / "results")
        class_name = job_id.replace('-', '_').replace('.', '_')

        # Calculate derived values
        d_min = params.get('d_min', 0.0)
        d_max = params.get('d_max', lattice_constant * 1.5)

        # Prepare template variables
        template_vars = {
            'class_name': class_name,
            'file_name': file_name,
            'output_path': output_path,
            'stl_path': params.get('stl_path', ''),
            'lattice_constant': lattice_constant,
            'sphere_radius_ratio': sphere_radius_ratio,
            'bond_radius_ratio': bond_radius_ratio,
            'poisson_ratio': poisson_ratio,
            'shift': shift,
            'num_cells': num_cells,
            'lattice_type': lattice_type,
            'delta': delta,
            'dstep': dstep,
            'd_min': d_min,
            'd_max': d_max,
            'eps': params.get('eps', 1e-6),
        }

        # Render template
        java_content = template.render(**template_vars)

        # Write generated Java file
        java_file_path = job_dir / f"{class_name}.java"
        with open(java_file_path, 'w', encoding='utf-8') as f:
            f.write(java_content)

        _logger.info(f"Generated Java file from template: {java_file_path}")
        return java_file_path

    def generate_batch_file(
        self,
        job_dir: Path,
        java_file_path: Path,
        java_class_name: Optional[str] = None
    ) -> Path:
        """Generate Windows batch file to run COMSOL using Jinja2 template.

        Args:
            job_dir: Job working directory
            java_file_path: Path to generated Java file
            java_class_name: Java class name (default: inferred from file)

        Returns:
            Path to generated batch file
        """
        if java_class_name is None:
            java_class_name = java_file_path.stem

        # Load template
        template = self.jinja_env.get_template('run.bat.j2')

        # Convert job_dir to Windows path if in WSL
        if detect_wsl():
            job_dir_str = wsl_to_windows_path(job_dir)
            _logger.debug(f"Converted WSL path to Windows path: {job_dir} -> {job_dir_str}")
        else:
            job_dir_str = str(job_dir)

        # Prepare template variables
        template_vars = {
            'job_id': job_dir.name,
            'job_dir': job_dir_str,
            'java_file_name': java_file_path.name,
            'class_name': java_class_name,
            'output_file': f"{java_class_name}.mph",
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
        job_id: Optional[str] = None
    ) -> Dict[str, Path]:
        """Generate complete job with all necessary files.

        Args:
            params: Simulation parameters
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
        java_file = self.generate_java_from_template(job_dir, params)
        batch_file = self.generate_batch_file(
            job_dir,
            java_file,
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

    def generate_custom_lattice_job(
        self,
        custom_job: 'CustomLatticeJob',
        job_id: Optional[str] = None,
        run_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate job for custom lattice structure.

        Args:
            custom_job: CustomLatticeJob object from YAML
            job_id: Optional specific job ID (for parametric sweeps)
            run_id: Optional run ID for grouping multiple jobs

        Returns:
            Dictionary with paths to generated files and metadata
        """
        from ..data.models.custom_lattice import CustomLatticeJob

        # Generate run ID if not provided (for grouping parametric sweep jobs)
        if run_id is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            run_id = f"run_{timestamp}"

        # Generate job ID if not provided
        if job_id is None:
            job_id = "job_001"

        _logger.info(f"Generating custom lattice job: {run_id}/{job_id}")

        # Create run directory
        run_dir = self.output_base_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        # Create job directory within run
        job_dir = run_dir / job_id
        job_dir.mkdir(parents=True, exist_ok=True)

        # Generate Java file from custom lattice template
        java_file = self._generate_custom_lattice_java(
            job_dir,
            custom_job,
            job_id
        )

        # Generate batch file
        batch_file = self.generate_batch_file(
            job_dir,
            java_file,
            java_class_name=java_file.stem
        )

        # Generate metadata file for this job
        metadata_file = self._generate_job_metadata(
            job_dir,
            custom_job,
            job_id
        )

        result = {
            'run_id': run_id,
            'job_id': job_id,
            'run_dir': run_dir,
            'job_dir': job_dir,
            'java_file': java_file,
            'batch_file': batch_file,
            'metadata_file': metadata_file
        }

        _logger.info(f"Custom lattice job generation completed: {run_id}/{job_id}")
        return result

    def _generate_custom_lattice_java(
        self,
        job_dir: Path,
        custom_job: 'CustomLatticeJob',
        job_id: str
    ) -> Path:
        """Generate Java file for custom lattice from template.

        Args:
            job_dir: Job directory
            custom_job: CustomLatticeJob definition
            job_id: Job identifier

        Returns:
            Path to generated Java file
        """
        # Load custom lattice template
        template = self.jinja_env.get_template('custom_lattice.java.j2')

        # Prepare template variables
        class_name = job_id.replace('-', '_').replace('.', '_')
        output_path = str(job_dir)
        stl_path = str(job_dir / "structure.stl")

        # Get first material (assuming single material for now)
        first_material = list(custom_job.materials.values())[0]

        # Prepare strain study parameters
        # Study contains strain delta and range directly
        strain_delta = custom_job.study.strain_delta
        strain_min, strain_max = custom_job.study.strain_range

        template_vars = {
            'class_name': class_name,
            'file_name': job_id,
            'output_path': output_path,
            'stl_path': stl_path,
            # Scale
            'scale_length': custom_job.job.scale.length,
            'scale_force': custom_job.job.scale.force,
            # Unit cell size
            'unit_cell_size': custom_job.job.unit_cell_size,
            # Material
            'youngs_modulus': first_material.youngs_modulus,
            'poissons_ratio': first_material.poissons_ratio,
            'density': first_material.density,
            # Mesh
            'mesh_size': custom_job.mesh.size,
            'mesh_type': custom_job.mesh.type,
            # Strain study
            'strain_delta': strain_delta,
            'strain_min': strain_min,
            'strain_max': strain_max,
            # Geometry
            'lattice_vectors': custom_job.geometry.lattice_vector,
            'spheres': custom_job.geometry.sphere,
            'beams': custom_job.geometry.beam,
        }

        # Render template
        java_content = template.render(**template_vars)

        # Validate rendered Java code
        validation_result = validate_generated_java(java_content)

        if not validation_result.is_valid:
            _logger.error(f"Template validation failed:")
            _logger.error(validation_result.get_error_summary())
            raise ValueError(f"Generated Java code has validation errors:\n{validation_result.get_error_summary()}")

        if validation_result.warnings:
            _logger.warning(f"Template validation warnings:")
            _logger.warning(validation_result.get_error_summary())

        # Write Java file
        java_file_path = job_dir / f"{class_name}.java"
        with open(java_file_path, 'w', encoding='utf-8') as f:
            f.write(java_content)

        _logger.info(f"Generated custom lattice Java file: {java_file_path}")
        return java_file_path

    def _generate_job_metadata(
        self,
        job_dir: Path,
        custom_job: 'CustomLatticeJob',
        job_id: str
    ) -> Path:
        """Generate metadata YAML file for the job.

        Args:
            job_dir: Job directory
            custom_job: CustomLatticeJob definition
            job_id: Job identifier

        Returns:
            Path to metadata file
        """
        import yaml

        metadata = {
            'job_id': job_id,
            'job_name': custom_job.job.name,
            'description': custom_job.job.description,
            'generated_at': datetime.now().isoformat(),
            'geometry': {
                'num_spheres': len(custom_job.geometry.sphere),
                'num_beams': len(custom_job.geometry.beam),
                'lattice_vectors': custom_job.geometry.lattice_vector,
            },
            'scale': {
                'length': custom_job.job.scale.length,
                'force': custom_job.job.scale.force,
            },
            'parametric': {
                'defaults': custom_job.job.parametric.default,
            }
        }

        metadata_path = job_dir / "metadata.yml"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            yaml.dump(metadata, f, default_flow_style=False, allow_unicode=True)

        _logger.info(f"Generated metadata file: {metadata_path}")
        return metadata_path

    def generate_parametric_study_jobs(
        self,
        custom_job: 'CustomLatticeJob',
        run_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate all jobs for a parametric study.

        Args:
            custom_job: CustomLatticeJob definition
            run_id: Optional run ID (auto-generated if None)

        Returns:
            Dictionary with run information and list of generated jobs
        """
        from ..services.parametric_generator import ParametricGenerator

        # Generate run ID
        if run_id is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            run_id = f"run_{timestamp}"

        _logger.info(f"Generating parametric study: {run_id}")

        # Create run directory
        run_dir = self.output_base_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        # Generate parameter sets
        generator = ParametricGenerator(custom_job)
        param_sets = generator.generate_parameter_sets()
        sweep_info = generator.get_sweep_info()

        _logger.info(f"Parametric study will generate {len(param_sets)} jobs")

        # Generate run-level metadata
        run_metadata = {
            'run_id': run_id,
            'job_name': custom_job.job.name,
            'description': custom_job.job.description,
            'generated_at': datetime.now().isoformat(),
            'parametric_study': sweep_info,
            'total_jobs': len(param_sets)
        }

        run_metadata_path = run_dir / "metadata.yml"
        import yaml
        with open(run_metadata_path, 'w', encoding='utf-8') as f:
            yaml.dump(run_metadata, f, default_flow_style=False, allow_unicode=True)

        # Generate each job
        jobs = []
        for param_set in param_sets:
            # Apply parameters to create job-specific configuration
            job_with_params = generator.apply_parameters_to_geometry(param_set)

            # Generate job
            result = self.generate_custom_lattice_job(
                job_with_params,
                job_id=param_set.job_id,
                run_id=run_id
            )
            jobs.append(result)

        _logger.info(f"Parametric study generation completed: {run_id} ({len(jobs)} jobs)")

        return {
            'run_id': run_id,
            'run_dir': run_dir,
            'run_metadata': run_metadata_path,
            'total_jobs': len(jobs),
            'jobs': jobs
        }


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
