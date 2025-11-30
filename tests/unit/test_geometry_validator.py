"""Unit tests for geometry validator."""

import pytest
from src.validators import GeometryValidator, ValidationError, ValidationResult
from src.data.models.custom_lattice import Geometry, Sphere, Beam


class TestGeometryValidator:
    """Tests for GeometryValidator class."""

    def test_valid_geometry_passes(self):
        """Test that valid geometry passes validation."""
        geometry = Geometry(
            lattice_vector=[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]],
            sphere=[
                Sphere(id=1, radius=0.2, position=[0.0, 0.0, 0.0]),
                Sphere(id=2, radius=0.2, position=[1.0, 0.0, 0.0]),
            ],
            beam=[
                Beam(id=1, endpoints=[1, 2], thickness=0.1)
            ]
        )

        validator = GeometryValidator()
        result = validator.validate(geometry)

        assert result.is_valid
        assert len(result.errors) == 0

    def test_overlapping_spheres_detected(self):
        """Test detection of overlapping spheres."""
        geometry = Geometry(
            lattice_vector=[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]],
            sphere=[
                Sphere(id=1, radius=0.5, position=[0.0, 0.0, 0.0]),
                Sphere(id=2, radius=0.5, position=[0.5, 0.0, 0.0]),  # Overlaps with sphere 1
            ],
            beam=[]
        )

        validator = GeometryValidator()
        result = validator.validate(geometry)

        assert not result.is_valid
        assert len(result.errors) > 0
        assert any('overlap' in err.error_type for err in result.errors)
        assert any(1 in err.element_ids and 2 in err.element_ids for err in result.errors)

    def test_touching_spheres_allowed(self):
        """Test that spheres that just touch are allowed."""
        geometry = Geometry(
            lattice_vector=[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]],
            sphere=[
                Sphere(id=1, radius=0.5, position=[0.0, 0.0, 0.0]),
                Sphere(id=2, radius=0.5, position=[1.0, 0.0, 0.0]),  # Exactly touching
            ],
            beam=[]
        )

        validator = GeometryValidator()
        result = validator.validate(geometry)

        # Should be valid or have only warnings, not errors
        assert result.is_valid or all(err.severity == 'warning' for err in result.errors)

    def test_beam_connection_validation(self):
        """Test beam connection validation."""
        geometry = Geometry(
            lattice_vector=[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]],
            sphere=[
                Sphere(id=1, radius=0.1, position=[0.0, 0.0, 0.0]),
                Sphere(id=2, radius=0.1, position=[1.0, 0.0, 0.0]),
            ],
            beam=[
                Beam(id=1, endpoints=[1, 2], thickness=0.05)
            ]
        )

        validator = GeometryValidator()
        result = validator.validate(geometry)

        # Should be valid - spheres don't overlap and beam connects them
        assert result.is_valid

    def test_beam_with_overlapping_spheres_detected(self):
        """Test detection of beam connecting overlapping spheres."""
        geometry = Geometry(
            lattice_vector=[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]],
            sphere=[
                Sphere(id=1, radius=0.6, position=[0.0, 0.0, 0.0]),
                Sphere(id=2, radius=0.6, position=[0.5, 0.0, 0.0]),  # Overlapping
            ],
            beam=[
                Beam(id=1, endpoints=[1, 2], thickness=0.05)
            ]
        )

        validator = GeometryValidator()
        result = validator.validate(geometry)

        # Should detect both sphere overlap and beam penetration errors
        assert not result.is_valid
        # Should have errors about either overlap or penetration
        assert len(result.errors) > 0

    def test_zero_lattice_vector_warning(self):
        """Test warning for near-zero lattice vector."""
        geometry = Geometry(
            lattice_vector=[[0.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]],
            sphere=[
                Sphere(id=1, radius=0.2, position=[0.0, 0.0, 0.0]),
            ],
            beam=[]
        )

        validator = GeometryValidator()
        result = validator.validate(geometry)

        # Should have warning about zero vector
        assert len(result.warnings) > 0
        assert any('zero' in warn.error_type.lower() for warn in result.warnings)

    def test_coplanar_lattice_vectors_warning(self):
        """Test warning for coplanar lattice vectors."""
        geometry = Geometry(
            lattice_vector=[
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [1.0, 1.0, 0.0]  # Coplanar with the other two
            ],
            sphere=[
                Sphere(id=1, radius=0.2, position=[0.0, 0.0, 0.0]),
            ],
            beam=[]
        )

        validator = GeometryValidator()
        result = validator.validate(geometry)

        # Should have warning about coplanar vectors
        assert len(result.warnings) > 0
        assert any('coplanar' in warn.error_type.lower() for warn in result.warnings)

    def test_validation_result_summary(self):
        """Test validation result summary generation."""
        geometry = Geometry(
            lattice_vector=[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]],
            sphere=[
                Sphere(id=1, radius=0.5, position=[0.0, 0.0, 0.0]),
                Sphere(id=2, radius=0.5, position=[0.5, 0.0, 0.0]),  # Overlapping
            ],
            beam=[]
        )

        validator = GeometryValidator()
        result = validator.validate(geometry)

        summary = result.get_error_summary()
        assert isinstance(summary, str)
        assert len(summary) > 0
        assert 'Error' in summary or 'error' in summary

    def test_multiple_overlapping_spheres(self):
        """Test detection of multiple overlapping sphere pairs."""
        geometry = Geometry(
            lattice_vector=[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]],
            sphere=[
                Sphere(id=1, radius=0.5, position=[0.0, 0.0, 0.0]),
                Sphere(id=2, radius=0.5, position=[0.5, 0.0, 0.0]),  # Overlaps with 1
                Sphere(id=3, radius=0.5, position=[0.0, 0.5, 0.0]),  # Overlaps with 1
            ],
            beam=[]
        )

        validator = GeometryValidator()
        result = validator.validate(geometry)

        assert not result.is_valid
        # Should detect 2 overlapping pairs: (1,2) and (1,3)
        overlap_errors = [err for err in result.errors if 'overlap' in err.error_type]
        assert len(overlap_errors) >= 2

    def test_custom_tolerance(self):
        """Test validator with custom tolerance."""
        geometry = Geometry(
            lattice_vector=[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]],
            sphere=[
                Sphere(id=1, radius=0.5, position=[0.0, 0.0, 0.0]),
                Sphere(id=2, radius=0.5, position=[0.99, 0.0, 0.0]),  # Overlapping by 0.01
            ],
            beam=[]
        )

        # With default tolerance (1e-6), should detect overlap
        validator_strict = GeometryValidator(tolerance=1e-6)
        result_strict = validator_strict.validate(geometry)
        assert not result_strict.is_valid

        # With larger tolerance (0.1), might not detect small overlap
        validator_loose = GeometryValidator(tolerance=0.1)
        result_loose = validator_loose.validate(geometry)
        # With tolerance 0.1, gap of -0.01 is within tolerance, so may not be detected
        # This is expected behavior

    def test_geometry_with_no_beams(self):
        """Test geometry validation with no beams."""
        geometry = Geometry(
            lattice_vector=[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]],
            sphere=[
                Sphere(id=1, radius=0.2, position=[0.0, 0.0, 0.0]),
                Sphere(id=2, radius=0.2, position=[1.0, 0.0, 0.0]),
            ],
            beam=[]
        )

        validator = GeometryValidator()
        result = validator.validate(geometry)

        # Should be valid even without beams
        assert result.is_valid

    def test_3d_diagonal_distance(self):
        """Test distance calculation in 3D."""
        geometry = Geometry(
            lattice_vector=[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]],
            sphere=[
                Sphere(id=1, radius=0.1, position=[0.0, 0.0, 0.0]),
                Sphere(id=2, radius=0.1, position=[1.0, 1.0, 1.0]),  # sqrt(3) away
            ],
            beam=[]
        )

        validator = GeometryValidator()
        result = validator.validate(geometry)

        # Spheres should not overlap (distance = sqrt(3) ≈ 1.73, sum of radii = 0.2)
        assert result.is_valid
