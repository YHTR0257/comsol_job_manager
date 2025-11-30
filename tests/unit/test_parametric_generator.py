"""Unit tests for parametric sweep generator."""

import pytest
from pathlib import Path

from src.services.parametric_generator import (
    ParametricGenerator,
    ParameterSet,
    generate_all_jobs,
    get_parameter_summary
)
from src.parsers import load_custom_lattice_yaml


# Fixture paths
FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"
VALID_YAML = FIXTURES_DIR / "sample_custom_lattice.yml"


class TestParametricGenerator:
    """Tests for ParametricGenerator class."""

    def test_no_sweeps(self, tmp_path):
        """Test generator with no parametric sweeps."""
        yaml_content = """
job:
  name: "Test"
  description: ""
  scale:
    length: 1e-3
    force: 1e-3
  parametric:
    default:
      sphere.radius: 0.2
      beam.thickness: 0.1
geometry:
  lattice_vector:
    - [2.0, 0.0, 0.0]
    - [0.0, 2.0, 0.0]
    - [0.0, 0.0, 2.0]
  sphere:
    - id: 1
      radius: 0.2
      position: [0.0, 0.0, 0.0]
  beam: []
mesh:
  size: 5
  type: "FreeTri"
materials:
  material_1:
    name: "mat1"
    youngs_modulus: 200e9
    poissons_ratio: 0.3
    density: 960
study:
  parametic_sweep:
    strain:
      delta: 0.01
      range: [0.0, 0.05]
  boundary_conditions:
    fixed: true
    copyface: true
"""
        yaml_file = tmp_path / "no_sweeps.yml"
        yaml_file.write_text(yaml_content)

        job = load_custom_lattice_yaml(yaml_file, validate_geometry=False)
        generator = ParametricGenerator(job)
        param_sets = generator.generate_parameter_sets()

        # Should generate exactly 1 job with default parameters
        assert len(param_sets) == 1
        assert param_sets[0].job_id == "job_001"
        assert param_sets[0].parameters == {
            "sphere.radius": 0.2,
            "beam.thickness": 0.1
        }

    def test_single_sweep(self, tmp_path):
        """Test generator with single parametric sweep."""
        yaml_content = """
job:
  name: "Test"
  description: ""
  scale:
    length: 1e-3
    force: 1e-3
  parametric:
    default:
      sphere.radius: 0.2
      beam.thickness: 0.1
    sweep1:
      parameter: "sphere.radius"
      values: [0.15, 0.2, 0.25]
geometry:
  lattice_vector:
    - [2.0, 0.0, 0.0]
    - [0.0, 2.0, 0.0]
    - [0.0, 0.0, 2.0]
  sphere:
    - id: 1
      radius: 0.2
      position: [0.0, 0.0, 0.0]
  beam: []
mesh:
  size: 5
  type: "FreeTri"
materials:
  material_1:
    name: "mat1"
    youngs_modulus: 200e9
    poissons_ratio: 0.3
    density: 960
study:
  parametic_sweep:
    strain:
      delta: 0.01
      range: [0.0, 0.05]
  boundary_conditions:
    fixed: true
    copyface: true
"""
        yaml_file = tmp_path / "single_sweep.yml"
        yaml_file.write_text(yaml_content)

        job = load_custom_lattice_yaml(yaml_file, validate_geometry=False)
        generator = ParametricGenerator(job)
        param_sets = generator.generate_parameter_sets()

        # Should generate 3 jobs (one for each sweep value)
        assert len(param_sets) == 3
        assert param_sets[0].parameters["sphere.radius"] == 0.15
        assert param_sets[1].parameters["sphere.radius"] == 0.2
        assert param_sets[2].parameters["sphere.radius"] == 0.25

        # All should have same beam.thickness (default)
        for ps in param_sets:
            assert ps.parameters["beam.thickness"] == 0.1

    def test_two_sweeps(self):
        """Test generator with two parametric sweeps."""
        job = load_custom_lattice_yaml(VALID_YAML, validate_geometry=False)
        generator = ParametricGenerator(job)
        param_sets = generator.generate_parameter_sets()

        # sweep1: 3 values, sweep2: 2 values -> 6 combinations
        assert len(param_sets) == 6

        # Check job IDs are sequential
        assert param_sets[0].job_id == "job_001"
        assert param_sets[5].job_id == "job_006"

        # Check all combinations are present
        radius_values = [ps.parameters["sphere.radius"] for ps in param_sets]
        thickness_values = [ps.parameters["beam.thickness"] for ps in param_sets]

        assert set(radius_values) == {0.15, 0.2, 0.25}
        assert set(thickness_values) == {0.08, 0.1}

        # Each radius should appear with each thickness
        for r in [0.15, 0.2, 0.25]:
            for t in [0.08, 0.1]:
                assert any(
                    ps.parameters["sphere.radius"] == r and
                    ps.parameters["beam.thickness"] == t
                    for ps in param_sets
                )

    def test_three_sweeps(self, tmp_path):
        """Test generator with three parametric sweeps."""
        yaml_content = """
job:
  name: "Test"
  description: ""
  scale:
    length: 1e-3
    force: 1e-3
  parametric:
    default:
      sphere.radius: 0.2
      beam.thickness: 0.1
      scale.factor: 1.0
    sweeps:
      - parameter: "sphere.radius"
        values: [0.15, 0.2]
      - parameter: "beam.thickness"
        values: [0.08, 0.1]
      - parameter: "scale.factor"
        values: [0.9, 1.0, 1.1]
geometry:
  lattice_vector:
    - [2.0, 0.0, 0.0]
    - [0.0, 2.0, 0.0]
    - [0.0, 0.0, 2.0]
  sphere:
    - id: 1
      radius: 0.2
      position: [0.0, 0.0, 0.0]
  beam: []
mesh:
  size: 5
  type: "FreeTri"
materials:
  material_1:
    name: "mat1"
    youngs_modulus: 200e9
    poissons_ratio: 0.3
    density: 960
study:
  parametic_sweep:
    strain:
      delta: 0.01
      range: [0.0, 0.05]
  boundary_conditions:
    fixed: true
    copyface: true
"""
        yaml_file = tmp_path / "three_sweeps.yml"
        yaml_file.write_text(yaml_content)

        job = load_custom_lattice_yaml(yaml_file, validate_geometry=False)
        generator = ParametricGenerator(job)
        param_sets = generator.generate_parameter_sets()

        # 2 × 2 × 3 = 12 combinations
        assert len(param_sets) == 12

        # Check all parameters are varied correctly
        radius_values = set(ps.parameters["sphere.radius"] for ps in param_sets)
        thickness_values = set(ps.parameters["beam.thickness"] for ps in param_sets)
        scale_values = set(ps.parameters["scale.factor"] for ps in param_sets)

        assert radius_values == {0.15, 0.2}
        assert thickness_values == {0.08, 0.1}
        assert scale_values == {0.9, 1.0, 1.1}

    def test_sweep_info(self):
        """Test getting sweep information."""
        job = load_custom_lattice_yaml(VALID_YAML, validate_geometry=False)
        generator = ParametricGenerator(job)
        info = generator.get_sweep_info()

        assert info['num_sweeps'] == 2
        assert info['total_jobs'] == 6
        assert len(info['sweep_dimensions']) == 2

        # Check first sweep
        assert info['sweep_dimensions'][0]['parameter'] == 'sphere.radius'
        assert info['sweep_dimensions'][0]['num_values'] == 3
        assert info['sweep_dimensions'][0]['values'] == [0.15, 0.2, 0.25]

        # Check second sweep
        assert info['sweep_dimensions'][1]['parameter'] == 'beam.thickness'
        assert info['sweep_dimensions'][1]['num_values'] == 2
        assert info['sweep_dimensions'][1]['values'] == [0.08, 0.1]

    def test_sweep_indices(self):
        """Test that sweep indices are correctly tracked."""
        job = load_custom_lattice_yaml(VALID_YAML, validate_geometry=False)
        generator = ParametricGenerator(job)
        param_sets = generator.generate_parameter_sets()

        # Check indices make sense
        # With 3 values in sweep1 and 2 in sweep2, we expect:
        # (0,0), (0,1), (1,0), (1,1), (2,0), (2,1)
        expected_indices = [
            (0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)
        ]

        actual_indices = [ps.sweep_indices for ps in param_sets]
        assert actual_indices == expected_indices

    def test_apply_parameters_to_geometry(self):
        """Test applying parameters to geometry."""
        job = load_custom_lattice_yaml(VALID_YAML, validate_geometry=False)
        generator = ParametricGenerator(job)
        param_sets = generator.generate_parameter_sets()

        # Apply first parameter set
        modified_job = generator.apply_parameters_to_geometry(param_sets[0])

        # Check that sphere radius was updated
        assert modified_job.geometry.sphere[0].radius == param_sets[0].parameters["sphere.radius"]

        # Check that beam thickness was updated
        if modified_job.geometry.beam:
            assert modified_job.geometry.beam[0].thickness == param_sets[0].parameters["beam.thickness"]

        # Original job should not be modified
        assert job.geometry.sphere[0].radius == 0.2


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_generate_all_jobs(self):
        """Test generate_all_jobs convenience function."""
        job = load_custom_lattice_yaml(VALID_YAML, validate_geometry=False)
        jobs = generate_all_jobs(job)

        assert len(jobs) == 6

        # Check structure
        for job_id, job_def in jobs:
            assert job_id.startswith("job_")
            assert job_def is not None
            assert hasattr(job_def, 'geometry')

    def test_get_parameter_summary(self):
        """Test parameter summary generation."""
        job = load_custom_lattice_yaml(VALID_YAML, validate_geometry=False)
        generator = ParametricGenerator(job)
        param_sets = generator.generate_parameter_sets()

        summary = get_parameter_summary(param_sets)

        assert "Total jobs: 6" in summary
        assert "sphere.radius" in summary
        assert "beam.thickness" in summary

    def test_get_parameter_summary_empty(self):
        """Test parameter summary with empty list."""
        summary = get_parameter_summary([])
        assert "No parameter sets" in summary


class TestBackwardCompatibility:
    """Tests for backward compatibility with sweep1/sweep2."""

    def test_sweep1_sweep2_converted_to_sweeps(self):
        """Test that sweep1/sweep2 are automatically converted to sweeps list."""
        job = load_custom_lattice_yaml(VALID_YAML, validate_geometry=False)

        # Should have sweeps list populated from sweep1 and sweep2
        assert job.job.parametric.sweeps is not None
        assert len(job.job.parametric.sweeps) == 2
        assert job.job.parametric.sweeps[0].parameter == "sphere.radius"
        assert job.job.parametric.sweeps[1].parameter == "beam.thickness"
