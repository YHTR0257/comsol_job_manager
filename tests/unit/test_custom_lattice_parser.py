"""Unit tests for custom lattice YAML parser."""

import pytest
from pathlib import Path
from pydantic import ValidationError

from src.parsers import load_custom_lattice_yaml, YAMLParseError
from src.data.models.custom_lattice import CustomLatticeJob


# Fixture paths
FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"
VALID_YAML = FIXTURES_DIR / "sample_custom_lattice.yml"
INVALID_OVERLAP_YAML = FIXTURES_DIR / "invalid_overlapping_spheres.yml"


class TestYAMLLoader:
    """Tests for YAML loading and parsing."""

    def test_load_valid_yaml(self):
        """Test loading a valid YAML file."""
        job = load_custom_lattice_yaml(VALID_YAML, validate_geometry=False)

        assert isinstance(job, CustomLatticeJob)
        assert job.job.name == "Simple Custom Lattice Test"
        assert len(job.geometry.sphere) == 4
        assert len(job.geometry.beam) == 3

    def test_job_metadata(self):
        """Test job metadata parsing."""
        job = load_custom_lattice_yaml(VALID_YAML, validate_geometry=False)

        assert job.job.name == "Simple Custom Lattice Test"
        assert job.job.description == "A simple custom lattice structure for testing"
        assert job.job.scale.length == 1e-3
        assert job.job.scale.force == 1e-3

    def test_geometry_parsing(self):
        """Test geometry parsing."""
        job = load_custom_lattice_yaml(VALID_YAML, validate_geometry=False)

        # Check lattice vectors
        assert len(job.geometry.lattice_vector) == 3
        assert job.geometry.lattice_vector[0] == [2.0, 0.0, 0.0]

        # Check spheres
        assert len(job.geometry.sphere) == 4
        assert job.geometry.sphere[0].id == 1
        assert job.geometry.sphere[0].radius == 0.2
        assert job.geometry.sphere[0].position == [0.0, 0.0, 0.0]

        # Check beams
        assert len(job.geometry.beam) == 3
        assert job.geometry.beam[0].id == 1
        assert job.geometry.beam[0].endpoints == [1, 2]
        assert job.geometry.beam[0].thickness == 0.1

    def test_material_parsing(self):
        """Test material properties parsing."""
        job = load_custom_lattice_yaml(VALID_YAML, validate_geometry=False)

        assert "material_1" in job.materials
        mat = job.materials["material_1"]
        assert mat.name == "mat1"
        assert mat.youngs_modulus == 200e9
        assert mat.poissons_ratio == 0.3
        assert mat.density == 960

    def test_parametric_study_parsing(self):
        """Test parametric study configuration parsing."""
        job = load_custom_lattice_yaml(VALID_YAML, validate_geometry=False)

        assert job.job.parametric.default == {
            "sphere.radius": 0.2,
            "beam.thickness": 0.1
        }

        assert job.job.parametric.sweep1 is not None
        assert job.job.parametric.sweep1.parameter == "sphere.radius"
        assert job.job.parametric.sweep1.values == [0.15, 0.2, 0.25]

        assert job.job.parametric.sweep2 is not None
        assert job.job.parametric.sweep2.parameter == "beam.thickness"
        assert job.job.parametric.sweep2.values == [0.08, 0.1]

    def test_mesh_configuration_parsing(self):
        """Test mesh configuration parsing."""
        job = load_custom_lattice_yaml(VALID_YAML, validate_geometry=False)

        assert job.mesh.size == 5
        assert job.mesh.type == "FreeTri"

    def test_study_configuration_parsing(self):
        """Test study configuration parsing."""
        job = load_custom_lattice_yaml(VALID_YAML, validate_geometry=False)

        strain_study = job.study.parametric_sweep["strain"]
        assert strain_study.delta == 0.01
        assert strain_study.range == [0.0, 0.05]

        assert job.study.boundary_conditions.fixed is True
        assert job.study.boundary_conditions.copyface is True

    def test_file_not_found(self):
        """Test error handling for non-existent file."""
        with pytest.raises(FileNotFoundError):
            load_custom_lattice_yaml("nonexistent.yml")

    def test_invalid_yaml_syntax(self, tmp_path):
        """Test error handling for invalid YAML syntax."""
        invalid_file = tmp_path / "invalid.yml"
        invalid_file.write_text("invalid: yaml: syntax:")

        with pytest.raises(YAMLParseError):
            load_custom_lattice_yaml(invalid_file)

    def test_missing_required_fields(self, tmp_path):
        """Test error handling for missing required fields."""
        incomplete_file = tmp_path / "incomplete.yml"
        incomplete_file.write_text("""
job:
  name: "Test"
# Missing geometry, materials, etc.
""")

        with pytest.raises(YAMLParseError):
            load_custom_lattice_yaml(incomplete_file)


class TestValidation:
    """Tests for validation logic."""

    def test_duplicate_sphere_ids(self, tmp_path):
        """Test detection of duplicate sphere IDs."""
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
geometry:
  lattice_vector:
    - [2.0, 0.0, 0.0]
    - [0.0, 2.0, 0.0]
    - [0.0, 0.0, 2.0]
  sphere:
    - id: 1
      radius: 0.2
      position: [0.0, 0.0, 0.0]
    - id: 1
      radius: 0.2
      position: [1.0, 0.0, 0.0]
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
        yaml_file = tmp_path / "duplicate_ids.yml"
        yaml_file.write_text(yaml_content)

        with pytest.raises(YAMLParseError) as exc_info:
            load_custom_lattice_yaml(yaml_file, validate_geometry=False)

        assert "Duplicate sphere IDs" in str(exc_info.value)

    def test_beam_references_nonexistent_sphere(self, tmp_path):
        """Test detection of beam referencing non-existent sphere."""
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
geometry:
  lattice_vector:
    - [2.0, 0.0, 0.0]
    - [0.0, 2.0, 0.0]
    - [0.0, 0.0, 2.0]
  sphere:
    - id: 1
      radius: 0.2
      position: [0.0, 0.0, 0.0]
  beam:
    - id: 1
      endpoints: [1, 999]  # Sphere 999 does not exist
      thickness: 0.1
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
        yaml_file = tmp_path / "bad_beam_ref.yml"
        yaml_file.write_text(yaml_content)

        with pytest.raises(YAMLParseError) as exc_info:
            load_custom_lattice_yaml(yaml_file, validate_geometry=False)

        assert "non-existent sphere" in str(exc_info.value)

    def test_negative_radius(self, tmp_path):
        """Test detection of negative radius."""
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
geometry:
  lattice_vector:
    - [2.0, 0.0, 0.0]
    - [0.0, 2.0, 0.0]
    - [0.0, 0.0, 2.0]
  sphere:
    - id: 1
      radius: -0.2  # Invalid negative radius
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
        yaml_file = tmp_path / "negative_radius.yml"
        yaml_file.write_text(yaml_content)

        with pytest.raises(YAMLParseError):
            load_custom_lattice_yaml(yaml_file, validate_geometry=False)

    def test_overlapping_spheres_geometry_validation(self):
        """Test geometric validation detects overlapping spheres."""
        with pytest.raises(YAMLParseError) as exc_info:
            load_custom_lattice_yaml(INVALID_OVERLAP_YAML, validate_geometry=True)

        assert "overlap" in str(exc_info.value).lower()

    def test_geometry_validation_can_be_disabled(self):
        """Test that geometry validation can be disabled."""
        # Should not raise even though spheres overlap
        job = load_custom_lattice_yaml(INVALID_OVERLAP_YAML, validate_geometry=False)
        assert job is not None
