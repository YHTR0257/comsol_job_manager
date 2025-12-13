"""Pydantic models for custom lattice YAML job definitions.

This module defines the data models for custom lattice structures used in
COMSOL simulations. It uses Pydantic for validation and parsing of YAML
job files.
"""

from typing import List, Dict, Optional, Union
from pydantic import BaseModel, Field, field_validator, model_validator
from pathlib import Path


class LatticeVector(BaseModel):
    """Lattice vector definition for periodic boundary conditions.

    Attributes:
        x: X component of the lattice vector
        y: Y component of the lattice vector
        z: Z component of the lattice vector
    """
    x: float
    y: float
    z: float

    @classmethod
    def from_list(cls, data: List[float]) -> "LatticeVector":
        """Create LatticeVector from a list [x, y, z]."""
        if len(data) != 3:
            raise ValueError(f"Lattice vector must have 3 components, got {len(data)}")
        return cls(x=data[0], y=data[1], z=data[2])


class Sphere(BaseModel):
    """Sphere geometry definition.

    Attributes:
        id: Unique identifier for the sphere
        radius: Radius of the sphere (must be positive)
        position: Position [x, y, z] of the sphere center
    """
    id: int = Field(..., gt=0, description="Sphere ID must be positive")
    radius: float = Field(..., gt=0, description="Radius must be positive")
    position: List[float] = Field(..., min_length=3, max_length=3)

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
        id: Unique identifier for the beam
        endpoints: List of two sphere IDs that this beam connects
        thickness: Thickness (diameter) of the beam (must be positive)
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
        lattice_vector: Three lattice vectors defining the unit cell
        sphere: List of sphere definitions
        beam: List of beam definitions
    """
    lattice_vector: List[List[float]] = Field(..., min_length=3, max_length=3)
    sphere: List[Sphere] = Field(..., min_length=1)
    beam: List[Beam] = Field(default_factory=list)

    @field_validator('lattice_vector')
    @classmethod
    def validate_lattice_vectors(cls, v):
        """Validate lattice vectors are 3D."""
        for i, vec in enumerate(v):
            if len(vec) != 3:
                raise ValueError(f"Lattice vector {i+1} must have 3 components")
        return v

    @model_validator(mode='after')
    def validate_beam_references(self):
        """Validate that beam endpoints reference existing spheres."""
        sphere_ids = {s.id for s in self.sphere}
        for beam in self.beam:
            for endpoint_id in beam.endpoints:
                if endpoint_id not in sphere_ids:
                    raise ValueError(
                        f"Beam {beam.id} references non-existent sphere {endpoint_id}"
                    )
        return self

    @model_validator(mode='after')
    def validate_unique_sphere_ids(self):
        """Validate that all sphere IDs are unique."""
        sphere_ids = [s.id for s in self.sphere]
        if len(sphere_ids) != len(set(sphere_ids)):
            duplicates = [sid for sid in sphere_ids if sphere_ids.count(sid) > 1]
            raise ValueError(f"Duplicate sphere IDs found: {set(duplicates)}")
        return self

    @model_validator(mode='after')
    def validate_unique_beam_ids(self):
        """Validate that all beam IDs are unique."""
        beam_ids = [b.id for b in self.beam]
        if len(beam_ids) != len(set(beam_ids)):
            duplicates = [bid for bid in beam_ids if beam_ids.count(bid) > 1]
            raise ValueError(f"Duplicate beam IDs found: {set(duplicates)}")
        return self


class Mesh(BaseModel):
    """Mesh configuration for COMSOL.

    Attributes:
        size: Mesh element size parameter
        type: Mesh type (e.g., FreeTri, FreeQuad)
    """
    size: float = Field(..., gt=0, description="Mesh size must be positive")
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


class Study(BaseModel):
    """Study configuration.

    Attributes:
        strain_delta: Strain increment for parametric sweep
        strain_range: [min, max] strain range
        boundary_conditions: Boundary condition settings
    """
    strain_delta: float = Field(..., gt=0)
    strain_range: List[float] = Field(..., min_length=2, max_length=2)
    boundary_conditions: BoundaryConditions

    @field_validator('strain_range')
    @classmethod
    def validate_strain_range(cls, v):
        """Validate strain_range is [min, max] with min < max."""
        if v[0] >= v[1]:
            raise ValueError(f"Strain range must be [min, max] with min < max, got {v}")
        return v


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
        sweeps: List of parametric sweeps (can be any number)
        sweep1: First parametric sweep (optional, for backward compatibility)
        sweep2: Second parametric sweep (optional, for backward compatibility)
    """
    default: Dict[str, float]
    sweeps: Optional[List[ParametricSweep]] = None
    sweep1: Optional[ParametricSweep] = None
    sweep2: Optional[ParametricSweep] = None

    @model_validator(mode='after')
    def consolidate_sweeps(self):
        """Consolidate sweep1/sweep2 into sweeps list for unified handling."""
        if self.sweeps is None:
            self.sweeps = []

        # Add sweep1 and sweep2 to sweeps list if they exist
        if self.sweep1 is not None and self.sweep1 not in self.sweeps:
            self.sweeps.append(self.sweep1)
        if self.sweep2 is not None and self.sweep2 not in self.sweeps:
            self.sweeps.append(self.sweep2)

        return self


class Scale(BaseModel):
    """Scaling factors for the simulation.

    Attributes:
        length: Length scale in meters
        force: Force scale in Newtons
    """
    length: float = Field(..., gt=0)
    force: float = Field(..., gt=0)


class Job(BaseModel):
    """Job metadata.

    Attributes:
        name: Job name
        description: Job description
        scale: Scaling factors
        parametric: Parametric study configuration
        unit_cell_size: Unit cell dimensions [Lx, Ly, Lz] in scaled units
    """
    name: str
    description: str = ""
    scale: Scale
    parametric: Parametric
    unit_cell_size: List[float] = Field(..., min_length=3, max_length=3)


class CustomLatticeJob(BaseModel):
    """Complete custom lattice job definition.

    This is the top-level model for parsing custom lattice YAML files.

    Attributes:
        job: Job metadata and parametric configuration
        geometry: Lattice geometry definition
        mesh: Mesh configuration
        materials: Material properties dictionary
        study: Study configuration
    """
    job: Job
    geometry: Geometry
    mesh: Mesh
    materials: Dict[str, Material]
    study: Study

    @model_validator(mode='after')
    def validate_parametric_parameters(self):
        """Validate that parametric sweep parameters are valid."""
        # Check if sweep parameters reference valid geometry properties
        valid_prefixes = ['sphere.radius', 'beam.thickness']

        if self.job.parametric.sweep1:
            param = self.job.parametric.sweep1.parameter
            if not any(param.startswith(prefix) for prefix in valid_prefixes):
                raise ValueError(
                    f"Invalid parametric parameter '{param}'. "
                    f"Must be one of: {valid_prefixes}"
                )

        if self.job.parametric.sweep2:
            param = self.job.parametric.sweep2.parameter
            if not any(param.startswith(prefix) for prefix in valid_prefixes):
                raise ValueError(
                    f"Invalid parametric parameter '{param}'. "
                    f"Must be one of: {valid_prefixes}"
                )

        return self
