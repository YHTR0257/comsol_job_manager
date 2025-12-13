"""Pydantic models for custom lattice YAML job definitions.

This module defines the data models for custom lattice structures used in
COMSOL simulations. It uses Pydantic for validation and parsing of YAML
job files.

Design version: v2.0 (2025-12-13)
Based on: docs/feature/FU01_custom_lattice.md
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field, field_validator, model_validator


class Sphere(BaseModel):
    """Sphere geometry definition.

    Attributes:
        id: Unique identifier for the sphere (1-indexed in YAML)
        position: Position [x, y, z] in mm (absolute coordinates)
        radius: Radius in mm (must be positive)
    """
    id: int = Field(..., gt=0, description="Sphere ID must be positive")
    position: List[float] = Field(..., min_length=3, max_length=3)
    radius: float = Field(..., gt=0, description="Radius must be positive")

    @field_validator('position')
    @classmethod
    def validate_position(cls, v):
        """Validate position is a 3D coordinate."""
        if len(v) != 3:
            raise ValueError(f"Position must be [x, y, z], got {len(v)} components")
        return v


class Beam(BaseModel):
    """Beam (cylinder) geometry connecting two spheres.

    Attributes:
        id: Unique identifier for the beam (1-indexed in YAML)
        endpoints: List of two sphere IDs (1-indexed) that this beam connects
        thickness: Thickness/diameter in mm (must be positive)
    """
    id: int = Field(..., gt=0, description="Beam ID must be positive")
    endpoints: List[int] = Field(..., min_length=2, max_length=2)
    thickness: float = Field(..., gt=0, description="Thickness must be positive")

    @field_validator('endpoints')
    @classmethod
    def validate_endpoints(cls, v):
        """Validate endpoints are exactly two sphere IDs."""
        if len(v) != 2:
            raise ValueError(f"Beam must connect exactly 2 spheres, got {len(v)}")
        if v[0] == v[1]:
            raise ValueError("Beam cannot connect a sphere to itself")
        return v


class Geometry(BaseModel):
    """Complete geometry definition for custom lattice.

    Attributes:
        lattice_constant: Lattice constant in mm (scalar)
        spheres: List of sphere definitions
        beams: List of beam definitions
    """
    lattice_constant: float = Field(..., gt=0, description="Lattice constant in mm")
    spheres: List[Sphere] = Field(..., min_length=1)
    beams: List[Beam] = Field(default_factory=list)

    @model_validator(mode='after')
    def validate_beam_references(self):
        """Validate that beam endpoints reference existing spheres."""
        sphere_ids = {s.id for s in self.spheres}
        for beam in self.beams:
            for endpoint_id in beam.endpoints:
                if endpoint_id not in sphere_ids:
                    raise ValueError(
                        f"Beam {beam.id} references non-existent sphere {endpoint_id}"
                    )
        return self

    @model_validator(mode='after')
    def validate_unique_sphere_ids(self):
        """Validate that all sphere IDs are unique."""
        sphere_ids = [s.id for s in self.spheres]
        if len(sphere_ids) != len(set(sphere_ids)):
            duplicates = [sid for sid in sphere_ids if sphere_ids.count(sid) > 1]
            raise ValueError(f"Duplicate sphere IDs found: {set(duplicates)}")
        return self

    @model_validator(mode='after')
    def validate_unique_beam_ids(self):
        """Validate that all beam IDs are unique."""
        beam_ids = [b.id for b in self.beams]
        if len(beam_ids) != len(set(beam_ids)):
            duplicates = [bid for bid in beam_ids if beam_ids.count(bid) > 1]
            raise ValueError(f"Duplicate beam IDs found: {set(duplicates)}")
        return self


class Mesh(BaseModel):
    """Mesh configuration for COMSOL.

    Attributes:
        size: Mesh size parameter (autoMeshSize value: 1-9)
        type: Mesh type (e.g., FreeTri) - currently unused, for future extension
    """
    size: int = Field(..., ge=1, le=9, description="Mesh size must be 1-9")
    type: str = Field(default="FreeTri")


class Material(BaseModel):
    """Material properties definition.

    Attributes:
        name: Material identifier
        youngs_modulus: Young's modulus in Pa
        poissons_ratio: Poisson's ratio (dimensionless)
        density: Density in kg/m^3
    """
    name: str
    youngs_modulus: float = Field(..., gt=0)
    poissons_ratio: float = Field(..., ge=-1, le=0.5)
    density: float = Field(..., gt=0)


class BoundaryConditions(BaseModel):
    """Boundary conditions for the study.

    Attributes:
        fixed: Whether to apply fixed boundary conditions
        copyface: Whether to apply periodic (copyface) boundary conditions
    """
    fixed: bool = True
    copyface: bool = True


class StrainConfig(BaseModel):
    """Strain configuration for the study.

    Attributes:
        delta: Maximum strain (e.g., 0.01 = 1%)
        steps: Displacement steps (e.g., "0, 0.25, 0.5, 0.75, 1")
    """
    delta: float = Field(..., gt=0, description="Maximum strain")
    steps: str = Field(..., description="Displacement steps")


class Study(BaseModel):
    """Study configuration.

    Attributes:
        strain: Strain configuration
        boundary_conditions: Boundary condition settings
    """
    strain: StrainConfig
    boundary_conditions: BoundaryConditions


class ParametricSweep(BaseModel):
    """Single parametric sweep definition.

    Attributes:
        parameter: Parameter name (e.g., 'sphere.radius')
        values: List of values to sweep
    """
    parameter: str
    values: List[float] = Field(..., min_length=1)


class Parametric(BaseModel):
    """Parametric study configuration.

    Attributes:
        default: Default parameter values
        sweeps: List of parametric sweeps
    """
    default: Dict[str, float] = Field(default_factory=dict)
    sweeps: List[ParametricSweep] = Field(default_factory=list)


class Job(BaseModel):
    """Job metadata.

    Attributes:
        name: Job name
        description: Job description
        unit_cell_size: Unit cell dimensions [Lx, Ly, Lz] in mm
        parametric: Parametric study configuration
    """
    name: str
    description: str = ""
    unit_cell_size: List[float] = Field(..., min_length=3, max_length=3)
    parametric: Parametric = Field(default_factory=Parametric)

    @field_validator('unit_cell_size')
    @classmethod
    def validate_unit_cell_size(cls, v):
        """Validate unit cell size has 3 positive components."""
        if any(x <= 0 for x in v):
            raise ValueError(f"Unit cell size must have all positive components, got {v}")
        return v


class CustomLatticeJob(BaseModel):
    """Complete custom lattice job definition.

    This is the top-level model for parsing custom lattice YAML files.
    Design based on docs/feature/FU01_custom_lattice.md v2.0

    Attributes:
        job: Job metadata and parametric configuration
        geometry: Lattice geometry definition (spheres and beams)
        materials: Material properties dictionary
        mesh: Mesh configuration
        study: Study configuration (strain and boundary conditions)
    """
    job: Job
    geometry: Geometry
    materials: Dict[str, Material]
    mesh: Mesh
    study: Study

    @model_validator(mode='after')
    def validate_parametric_parameters(self):
        """Validate that parametric sweep parameters are valid.

        Supports:
        - sphere.radius (all spheres)
        - sphere.{index}.radius (specific sphere, 0-indexed)
        - beam.thickness (all beams)
        - beam.{index}.thickness (specific beam, 0-indexed)
        """
        valid_patterns = [
            'sphere.radius',
            'sphere.',  # Allows sphere.0.radius, sphere.1.radius, etc.
            'beam.thickness',
            'beam.',     # Allows beam.0.thickness, beam.1.thickness, etc.
        ]

        for sweep in self.job.parametric.sweeps:
            param = sweep.parameter
            is_valid = any(param.startswith(pattern) for pattern in valid_patterns)

            if not is_valid:
                raise ValueError(
                    f"Invalid parametric parameter '{param}'. "
                    f"Must match: sphere.radius, sphere.{{N}}.radius, "
                    f"beam.thickness, or beam.{{N}}.thickness"
                )

            # Validate index if specific element is referenced
            if '.' in param and param.count('.') == 2:
                parts = param.split('.')
                prefix, index_str, field = parts

                try:
                    index = int(index_str)
                except ValueError:
                    raise ValueError(
                        f"Invalid index in parameter '{param}': '{index_str}' is not an integer"
                    )

                # Validate index is within bounds
                if prefix == 'sphere':
                    if index < 0 or index >= len(self.geometry.spheres):
                        raise ValueError(
                            f"Sphere index {index} out of bounds (0-{len(self.geometry.spheres)-1})"
                        )
                    if field != 'radius':
                        raise ValueError(f"Invalid field for sphere: '{field}' (must be 'radius')")

                elif prefix == 'beam':
                    if index < 0 or index >= len(self.geometry.beams):
                        raise ValueError(
                            f"Beam index {index} out of bounds (0-{len(self.geometry.beams)-1})"
                        )
                    if field != 'thickness':
                        raise ValueError(f"Invalid field for beam: '{field}' (must be 'thickness')")

        return self
