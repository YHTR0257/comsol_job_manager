"""Geometry validation for custom lattice structures.

This module provides validation functions to check the physical validity
of custom lattice geometries, including sphere overlap detection and
beam-sphere connection validation.
"""

import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from ..data.models.custom_lattice import Geometry, Sphere, Beam


@dataclass
class ValidationError:
    """A single validation error.

    Attributes:
        error_type: Type of error (e.g., 'sphere_overlap', 'beam_disconnect')
        message: Human-readable error message
        element_ids: IDs of elements involved in the error
        severity: Error severity ('error', 'warning')
    """
    error_type: str
    message: str
    element_ids: List[int]
    severity: str = 'error'


@dataclass
class ValidationResult:
    """Result of geometry validation.

    Attributes:
        is_valid: Whether the geometry is valid
        errors: List of validation errors
        warnings: List of validation warnings
    """
    is_valid: bool
    errors: List[ValidationError]
    warnings: List[ValidationError]

    def get_error_summary(self) -> str:
        """Get a formatted summary of all errors and warnings."""
        lines = []
        if self.errors:
            lines.append(f"Errors ({len(self.errors)}):")
            for err in self.errors:
                lines.append(f"  - {err.message}")
        if self.warnings:
            lines.append(f"Warnings ({len(self.warnings)}):")
            for warn in self.warnings:
                lines.append(f"  - {warn.message}")
        return "\n".join(lines) if lines else "No errors or warnings"


class GeometryValidator:
    """Validator for custom lattice geometry.

    This class performs geometric checks on sphere and beam configurations
    to ensure they form a valid physical structure.
    """

    def __init__(self, tolerance: float = 1e-6):
        """Initialize the validator.

        Args:
            tolerance: Numerical tolerance for floating-point comparisons
        """
        self.tolerance = tolerance

    def validate(self, geometry: Geometry) -> ValidationResult:
        """Validate the complete geometry.

        Args:
            geometry: Geometry object to validate

        Returns:
            ValidationResult containing all errors and warnings
        """
        errors = []
        warnings = []

        # Check for sphere overlaps
        overlap_errors = self._check_sphere_overlaps(geometry.spheres)
        errors.extend(overlap_errors)

        # Check beam-sphere connections
        if geometry.beams:
            connection_errors = self._check_beam_connections(
                geometry.spheres,
                geometry.beams
            )
            errors.extend(connection_errors)

        # Note: lattice_constant validation removed (it's now a scalar, not vectors)
        # The lattice_constant is used as a reference length and doesn't need
        # geometric validation like vectors did

        is_valid = len(errors) == 0

        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings
        )

    def _check_sphere_overlaps(
        self,
        spheres: List[Sphere]
    ) -> List[ValidationError]:
        """Check if any spheres overlap.

        Two spheres overlap if the distance between their centers is less
        than the sum of their radii.

        Args:
            spheres: List of sphere definitions

        Returns:
            List of validation errors for overlapping spheres
        """
        errors = []
        n = len(spheres)

        for i in range(n):
            for j in range(i + 1, n):
                s1, s2 = spheres[i], spheres[j]
                distance = self._calculate_distance(s1.position, s2.position)
                min_distance = s1.radius + s2.radius

                if distance < min_distance - self.tolerance:
                    errors.append(ValidationError(
                        error_type='sphere_overlap',
                        message=(
                            f"Spheres {s1.id} and {s2.id} overlap: "
                            f"distance={distance:.4f}, "
                            f"min_distance={min_distance:.4f}"
                        ),
                        element_ids=[s1.id, s2.id],
                        severity='error'
                    ))

        return errors

    def _check_beam_connections(
        self,
        spheres: List[Sphere],
        beams: List[Beam]
    ) -> List[ValidationError]:
        """Check if beams properly connect their endpoint spheres.

        A beam should span approximately the distance between two sphere
        surfaces. The beam is disconnected if:
        - The gap between sphere surfaces is too large
        - The beam penetrates too deeply into the spheres

        Args:
            spheres: List of sphere definitions
            beams: List of beam definitions

        Returns:
            List of validation errors for disconnected beams
        """
        errors = []
        sphere_dict = {s.id: s for s in spheres}

        for beam in beams:
            s1_id, s2_id = beam.endpoints
            s1 = sphere_dict[s1_id]
            s2 = sphere_dict[s2_id]

            # Calculate distance between sphere centers
            center_distance = self._calculate_distance(s1.position, s2.position)

            # Calculate the gap between sphere surfaces
            gap = center_distance - s1.radius - s2.radius

            # Check if spheres are overlapping (negative gap)
            # This is the main error condition - beams can't connect overlapping spheres
            if gap < -self.tolerance:
                errors.append(ValidationError(
                    error_type='beam_excessive_penetration',
                    message=(
                        f"Beam {beam.id} connects overlapping spheres "
                        f"{s1_id} and {s2_id}: gap={gap:.4f} "
                        f"(spheres are overlapping)"
                    ),
                    element_ids=[beam.id, s1_id, s2_id],
                    severity='error'
                ))
            # Note: We don't check if the gap is "too large" because in custom lattices,
            # beams are meant to connect distant spheres. The gap size is a design choice.

        return errors

    def _check_lattice_vectors(
        self,
        lattice_vectors: List[List[float]]
    ) -> List[ValidationError]:
        """Check lattice vectors for potential issues.

        Args:
            lattice_vectors: List of three 3D lattice vectors

        Returns:
            List of validation warnings
        """
        warnings = []

        # Check if vectors are too small
        for i, vec in enumerate(lattice_vectors):
            magnitude = math.sqrt(sum(x**2 for x in vec))
            if magnitude < self.tolerance:
                warnings.append(ValidationError(
                    error_type='zero_lattice_vector',
                    message=f"Lattice vector {i+1} has near-zero magnitude: {magnitude}",
                    element_ids=[i+1],
                    severity='warning'
                ))

        # Check if vectors are coplanar (volume near zero)
        volume = self._calculate_parallelepiped_volume(lattice_vectors)
        if abs(volume) < self.tolerance:
            warnings.append(ValidationError(
                error_type='coplanar_lattice_vectors',
                message=(
                    f"Lattice vectors are coplanar (volume={volume:.6e}). "
                    "This may cause issues with periodic boundary conditions."
                ),
                element_ids=[1, 2, 3],
                severity='warning'
            ))

        return warnings

    @staticmethod
    def _calculate_distance(pos1: List[float], pos2: List[float]) -> float:
        """Calculate Euclidean distance between two positions.

        Args:
            pos1: First position [x, y, z]
            pos2: Second position [x, y, z]

        Returns:
            Euclidean distance
        """
        return math.sqrt(
            sum((a - b) ** 2 for a, b in zip(pos1, pos2))
        )

    @staticmethod
    def _calculate_parallelepiped_volume(vectors: List[List[float]]) -> float:
        """Calculate volume of parallelepiped defined by three vectors.

        Uses the scalar triple product: V = a · (b × c)

        Args:
            vectors: List of three 3D vectors

        Returns:
            Volume (can be negative depending on orientation)
        """
        a, b, c = vectors

        # Calculate cross product b × c
        cross = [
            b[1] * c[2] - b[2] * c[1],
            b[2] * c[0] - b[0] * c[2],
            b[0] * c[1] - b[1] * c[0]
        ]

        # Calculate dot product a · (b × c)
        volume = sum(a[i] * cross[i] for i in range(3))

        return volume
