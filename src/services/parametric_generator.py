"""Parametric sweep generator for custom lattice jobs.

This module generates all combinations of parametric sweep values
and creates individual parameter sets for each job.
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass
from itertools import product
from ..data.models.custom_lattice import CustomLatticeJob, ParametricSweep


@dataclass
class ParameterSet:
    """A single set of parameters for one job.

    Attributes:
        job_id: Unique job identifier (e.g., 'job_001')
        parameters: Dictionary of parameter names to values
        sweep_indices: Indices in each sweep dimension (for tracking)
    """
    job_id: str
    parameters: Dict[str, float]
    sweep_indices: Tuple[int, ...]


class ParametricGenerator:
    """Generator for parametric sweep combinations.

    This class takes a CustomLatticeJob definition and expands
    the parametric sweeps into individual parameter sets for each job.
    """

    def __init__(self, job: CustomLatticeJob):
        """Initialize the generator.

        Args:
            job: CustomLatticeJob definition containing parametric sweeps
        """
        self.job = job
        self.default_params = job.job.parametric.default
        self.sweeps = job.job.parametric.sweeps or []

    def generate_parameter_sets(self) -> List[ParameterSet]:
        """Generate all parameter set combinations.

        Returns:
            List of ParameterSet objects, one for each job to be created

        Example:
            If sweep1 has 3 values and sweep2 has 2 values,
            this will return 6 ParameterSet objects (3 × 2)
        """
        if not self.sweeps:
            # No sweeps defined - return single parameter set with defaults
            return [ParameterSet(
                job_id="job_001",
                parameters=self.default_params.copy(),
                sweep_indices=()
            )]

        # Get all sweep values
        sweep_values = [sweep.values for sweep in self.sweeps]
        sweep_params = [sweep.parameter for sweep in self.sweeps]

        # Generate all combinations using Cartesian product
        parameter_sets = []
        job_counter = 1

        for indices_tuple in product(*[range(len(vals)) for vals in sweep_values]):
            # Start with default parameters
            params = self.default_params.copy()

            # Override with sweep values
            for sweep_idx, value_idx in enumerate(indices_tuple):
                param_name = sweep_params[sweep_idx]
                param_value = sweep_values[sweep_idx][value_idx]
                params[param_name] = param_value

            # Create parameter set
            job_id = f"job_{job_counter:03d}"
            parameter_sets.append(ParameterSet(
                job_id=job_id,
                parameters=params,
                sweep_indices=indices_tuple
            ))
            job_counter += 1

        return parameter_sets

    def get_sweep_info(self) -> Dict[str, any]:
        """Get information about the parametric sweeps.

        Returns:
            Dictionary with sweep statistics and information
        """
        if not self.sweeps:
            return {
                'num_sweeps': 0,
                'total_jobs': 1,
                'sweep_dimensions': []
            }

        sweep_dimensions = []
        total_jobs = 1

        for sweep in self.sweeps:
            num_values = len(sweep.values)
            total_jobs *= num_values
            sweep_dimensions.append({
                'parameter': sweep.parameter,
                'num_values': num_values,
                'values': sweep.values
            })

        return {
            'num_sweeps': len(self.sweeps),
            'total_jobs': total_jobs,
            'sweep_dimensions': sweep_dimensions
        }

    def apply_parameters_to_geometry(
        self,
        param_set: ParameterSet
    ) -> 'CustomLatticeJob':
        """Apply parameter set to geometry.

        This creates a new job definition with parameters applied to
        the geometry (updating sphere radii, beam thickness, etc.)

        Args:
            param_set: Parameter set to apply

        Returns:
            New CustomLatticeJob with parameters applied
        """
        import copy

        # Deep copy the job to avoid modifying the original
        new_job = copy.deepcopy(self.job)

        # Apply parameters to geometry
        for param_name, param_value in param_set.parameters.items():
            if param_name.startswith('sphere.radius'):
                # Apply to all spheres or specific sphere
                for sphere in new_job.geometry.sphere:
                    sphere.radius = param_value
            elif param_name.startswith('beam.thickness'):
                # Apply to all beams or specific beam
                for beam in new_job.geometry.beam:
                    beam.thickness = param_value
            # Add more parameter types as needed

        return new_job


def generate_all_jobs(job: CustomLatticeJob) -> List[Tuple[str, CustomLatticeJob]]:
    """Generate all job variations from parametric sweeps.

    This is a convenience function that generates parameter sets
    and applies them to create complete job definitions.

    Args:
        job: Base CustomLatticeJob definition

    Returns:
        List of (job_id, job_definition) tuples
    """
    generator = ParametricGenerator(job)
    parameter_sets = generator.generate_parameter_sets()

    jobs = []
    for param_set in parameter_sets:
        job_with_params = generator.apply_parameters_to_geometry(param_set)
        jobs.append((param_set.job_id, job_with_params))

    return jobs


def get_parameter_summary(parameter_sets: List[ParameterSet]) -> str:
    """Generate a human-readable summary of parameter sets.

    Args:
        parameter_sets: List of parameter sets

    Returns:
        Formatted string summarizing the parameter combinations
    """
    if not parameter_sets:
        return "No parameter sets generated"

    lines = [f"Total jobs: {len(parameter_sets)}"]
    lines.append("")

    # Get all unique parameter names
    if parameter_sets:
        param_names = sorted(parameter_sets[0].parameters.keys())
        lines.append("Parameters:")
        for name in param_names:
            values = [ps.parameters[name] for ps in parameter_sets]
            unique_values = sorted(set(values))
            if len(unique_values) > 1:
                lines.append(f"  {name}: {len(unique_values)} values {unique_values}")
            else:
                lines.append(f"  {name}: {unique_values[0]} (constant)")

    return "\n".join(lines)
