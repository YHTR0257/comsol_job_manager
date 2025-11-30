"""Unit tests for custom lattice job generation."""

import pytest
from pathlib import Path
import shutil

from src.parsers import load_custom_lattice_yaml
from src.services.job_generator import JobGenerator


# Fixture paths
FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"
VALID_YAML = FIXTURES_DIR / "sample_custom_lattice.yml"
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"


class TestCustomLatticeJobGeneration:
    """Tests for custom lattice job generation."""

    @pytest.fixture
    def temp_output_dir(self, tmp_path):
        """Create temporary output directory."""
        output_dir = tmp_path / "jobs"
        output_dir.mkdir()
        yield output_dir
        # Cleanup
        if output_dir.exists():
            shutil.rmtree(output_dir)

    @pytest.fixture
    def job_generator(self, temp_output_dir):
        """Create JobGenerator instance."""
        return JobGenerator(
            template_dir=TEMPLATES_DIR,
            output_base_dir=temp_output_dir
        )

    def test_generate_single_custom_lattice_job(self, job_generator):
        """Test generating a single custom lattice job."""
        # Load custom lattice definition
        custom_job = load_custom_lattice_yaml(VALID_YAML, validate_geometry=True)

        # Generate job
        result = job_generator.generate_custom_lattice_job(
            custom_job,
            job_id="job_001",
            run_id="test_run"
        )

        # Verify structure
        assert result['run_id'] == "test_run"
        assert result['job_id'] == "job_001"
        assert result['run_dir'].exists()
        assert result['job_dir'].exists()

        # Verify files were created
        assert result['java_file'].exists()
        assert result['batch_file'].exists()
        assert result['metadata_file'].exists()

        # Verify Java file content
        java_content = result['java_file'].read_text()
        assert "public class job_001" in java_content
        assert "Sphere" in java_content or "sphere" in java_content.lower()

        # Verify metadata content
        import yaml
        with open(result['metadata_file']) as f:
            metadata = yaml.safe_load(f)
        assert metadata['job_id'] == "job_001"
        assert metadata['geometry']['num_spheres'] == 4
        assert metadata['geometry']['num_beams'] == 3

    def test_generate_parametric_study_jobs(self, job_generator):
        """Test generating multiple jobs for parametric study."""
        # Load custom lattice definition
        custom_job = load_custom_lattice_yaml(VALID_YAML, validate_geometry=True)

        # Generate parametric study
        result = job_generator.generate_parametric_study_jobs(
            custom_job,
            run_id="test_parametric_run"
        )

        # Verify run structure
        assert result['run_id'] == "test_parametric_run"
        assert result['run_dir'].exists()
        assert result['run_metadata'].exists()

        # Should generate 6 jobs (3 radii × 2 thicknesses)
        assert result['total_jobs'] == 6
        assert len(result['jobs']) == 6

        # Verify each job
        for i, job in enumerate(result['jobs'], 1):
            assert job['job_id'] == f"job_{i:03d}"
            assert job['job_dir'].exists()
            assert job['java_file'].exists()
            assert job['batch_file'].exists()
            assert job['metadata_file'].exists()

        # Verify run metadata
        import yaml
        with open(result['run_metadata']) as f:
            run_metadata = yaml.safe_load(f)
        assert run_metadata['total_jobs'] == 6
        assert run_metadata['parametric_study']['num_sweeps'] == 2

    def test_custom_lattice_job_file_names(self, job_generator):
        """Test that generated files have correct names."""
        custom_job = load_custom_lattice_yaml(VALID_YAML, validate_geometry=True)

        result = job_generator.generate_custom_lattice_job(
            custom_job,
            job_id="job_test_123",
            run_id="test_run"
        )

        # Check file names
        assert result['java_file'].name == "job_test_123.java"
        assert result['batch_file'].name == "run.bat"
        assert result['metadata_file'].name == "metadata.yml"

    def test_custom_lattice_directory_structure(self, job_generator):
        """Test that directory structure is correct."""
        custom_job = load_custom_lattice_yaml(VALID_YAML, validate_geometry=True)

        result = job_generator.generate_parametric_study_jobs(
            custom_job,
            run_id="test_structure"
        )

        # Check structure: output_dir/run_id/job_id/
        run_dir = result['run_dir']
        assert run_dir.name == "test_structure"

        # Check that job directories exist under run directory
        for i in range(1, 7):
            job_dir = run_dir / f"job_{i:03d}"
            assert job_dir.exists()
            assert job_dir.is_dir()

    def test_metadata_contains_correct_information(self, job_generator):
        """Test that metadata file contains correct information."""
        custom_job = load_custom_lattice_yaml(VALID_YAML, validate_geometry=True)

        result = job_generator.generate_custom_lattice_job(
            custom_job,
            job_id="job_001",
            run_id="test_run"
        )

        import yaml
        with open(result['metadata_file']) as f:
            metadata = yaml.safe_load(f)

        # Check metadata fields
        assert 'job_id' in metadata
        assert 'job_name' in metadata
        assert 'description' in metadata
        assert 'generated_at' in metadata
        assert 'geometry' in metadata
        assert 'scale' in metadata
        assert 'parametric' in metadata

        # Check geometry information
        assert metadata['geometry']['num_spheres'] == 4
        assert metadata['geometry']['num_beams'] == 3
        assert len(metadata['geometry']['lattice_vectors']) == 3

        # Check scale
        assert metadata['scale']['length'] == 1e-3
        assert metadata['scale']['force'] == 1e-3

    def test_auto_generated_run_id(self, job_generator):
        """Test that run_id is auto-generated if not provided."""
        custom_job = load_custom_lattice_yaml(VALID_YAML, validate_geometry=True)

        result = job_generator.generate_custom_lattice_job(
            custom_job,
            job_id="job_001"
            # run_id not provided
        )

        # Should have auto-generated run_id
        assert result['run_id'].startswith('run_')
        assert len(result['run_id']) > 4  # More than just "run_"
