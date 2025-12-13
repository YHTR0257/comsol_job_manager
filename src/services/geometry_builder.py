"""Geometry builder for custom lattice structures.

This module builds complete geometry data from YAML definitions,
applying parametric parameters and calculating beam endpoints.

Design based on: docs/feature/FU01_custom_lattice.md v2.0
"""

from typing import List, Tuple, Dict
from dataclasses import dataclass
import copy

from ..data.models.custom_lattice import (
    CustomLatticeJob,
    Geometry,
    Sphere,
    Beam
)
from .parametric_generator import ParameterSet


@dataclass
class SphereData:
    """Template-ready sphere data.

    Attributes:
        id: Sphere ID (1-indexed as in YAML)
        position: Absolute position [x, y, z] in mm
        radius: Radius in mm
    """
    id: int
    position: List[float]
    radius: float


@dataclass
class BeamData:
    """Template-ready beam data.

    Attributes:
        id: Beam ID (1-indexed as in YAML)
        endpoint1_index: Index in points array (0-indexed)
        endpoint2_index: Index in points array (0-indexed)
        thickness: Thickness/diameter in mm
    """
    id: int
    endpoint1_index: int
    endpoint2_index: int
    thickness: float


@dataclass
class GeometryData:
    """Complete geometry data for Jinja2 template.

    Attributes:
        spheres: List of sphere data
        beams: List of beam data
        lattice_constant: Lattice constant in mm
        unit_cell_size: Unit cell dimensions [Lx, Ly, Lz] in mm
    """
    spheres: List[SphereData]
    beams: List[BeamData]
    lattice_constant: float
    unit_cell_size: List[float]


class GeometryBuilder:
    """Builds geometry data from job definition and parameters.

    This class is responsible for:
    1. Applying parametric parameters to geometry
    2. Calculating beam endpoint indices
    3. Preparing data for Jinja2 template
    """

    def build_geometry_data(
        self,
        job: CustomLatticeJob,
        param_set: ParameterSet
    ) -> GeometryData:
        """Build complete geometry data for one parameter set.

        Args:
            job: Base job definition
            param_set: Parameter set to apply

        Returns:
            GeometryData ready for Jinja2 template

        Example:
            >>> builder = GeometryBuilder()
            >>> geometry_data = builder.build_geometry_data(job, param_set)
            >>> # geometry_data.spheres contains SphereData objects
            >>> # geometry_data.beams contains BeamData objects
        """
        # Apply parametric parameters to geometry
        geometry = self.apply_parametric_parameters(
            job.geometry,
            param_set
        )

        # Build sphere data
        sphere_data_list = []
        for sphere in geometry.spheres:
            sphere_data_list.append(SphereData(
                id=sphere.id,
                position=sphere.position.copy(),
                radius=sphere.radius
            ))

        # Build beam data with endpoint indices
        beam_data_list = []
        for beam in geometry.beams:
            endpoint1_idx, endpoint2_idx = self.calculate_beam_endpoints(
                beam,
                geometry.spheres
            )
            beam_data_list.append(BeamData(
                id=beam.id,
                endpoint1_index=endpoint1_idx,
                endpoint2_index=endpoint2_idx,
                thickness=beam.thickness
            ))

        return GeometryData(
            spheres=sphere_data_list,
            beams=beam_data_list,
            lattice_constant=geometry.lattice_constant,
            unit_cell_size=job.job.unit_cell_size.copy()
        )

    def apply_parametric_parameters(
        self,
        geometry: Geometry,
        param_set: ParameterSet
    ) -> Geometry:
        """Apply parametric parameters to geometry.

        Application order:
        1. Global parameters (sphere.radius, beam.thickness) applied to all
        2. Specific parameters (sphere.0.radius, beam.3.thickness) override

        Args:
            geometry: Base geometry definition
            param_set: Parameter set with values to apply

        Returns:
            New Geometry object with parameters applied
        """
        # Deep copy to avoid modifying original
        new_geometry = copy.deepcopy(geometry)

        # Step 1: Apply global parameters first
        if 'sphere.radius' in param_set.parameters:
            radius = param_set.parameters['sphere.radius']
            for sphere in new_geometry.spheres:
                sphere.radius = radius

        if 'beam.thickness' in param_set.parameters:
            thickness = param_set.parameters['beam.thickness']
            for beam in new_geometry.beams:
                beam.thickness = thickness

        # Step 2: Apply specific parameters (override globals)
        for param_name, param_value in param_set.parameters.items():
            # Parse sphere.{index}.radius
            if param_name.startswith('sphere.') and param_name.count('.') == 2:
                parts = param_name.split('.')
                index = int(parts[1])
                field = parts[2]

                if field == 'radius' and 0 <= index < len(new_geometry.spheres):
                    new_geometry.spheres[index].radius = param_value

            # Parse beam.{index}.thickness
            elif param_name.startswith('beam.') and param_name.count('.') == 2:
                parts = param_name.split('.')
                index = int(parts[1])
                field = parts[2]

                if field == 'thickness' and 0 <= index < len(new_geometry.beams):
                    new_geometry.beams[index].thickness = param_value

        return new_geometry

    def calculate_beam_endpoints(
        self,
        beam: Beam,
        spheres: List[Sphere]
    ) -> Tuple[int, int]:
        """Calculate beam endpoint indices from sphere IDs.

        Args:
            beam: Beam with endpoint sphere IDs (1-indexed)
            spheres: List of spheres

        Returns:
            Tuple of (endpoint1_index, endpoint2_index) as 0-indexed positions

        Raises:
            ValueError: If sphere IDs not found

        Example:
            >>> beam = Beam(id=1, endpoints=[1, 3], thickness=0.5)
            >>> spheres = [Sphere(id=1, ...), Sphere(id=2, ...), Sphere(id=3, ...)]
            >>> calculate_beam_endpoints(beam, spheres)
            (0, 2)  # sphere id=1 is at index 0, sphere id=3 is at index 2
        """
        sphere1_id, sphere2_id = beam.endpoints

        # Find sphere indices (0-indexed)
        sphere1_idx = None
        sphere2_idx = None

        for idx, sphere in enumerate(spheres):
            if sphere.id == sphere1_id:
                sphere1_idx = idx
            if sphere.id == sphere2_id:
                sphere2_idx = idx

        if sphere1_idx is None:
            raise ValueError(
                f"Beam {beam.id}: sphere {sphere1_id} not found in sphere list"
            )
        if sphere2_idx is None:
            raise ValueError(
                f"Beam {beam.id}: sphere {sphere2_id} not found in sphere list"
            )

        return sphere1_idx, sphere2_idx

    def scale_position(
        self,
        position: List[float],
        lattice_constant: float,
        is_relative: bool = False
    ) -> List[float]:
        """Scale position coordinates.

        Args:
            position: Position [x, y, z]
            lattice_constant: Lattice constant in mm
            is_relative: If True, position is relative (0-1), otherwise absolute

        Returns:
            Absolute position in mm

        Example:
            >>> scale_position([0.5, 0.5, 0.5], 15.0, is_relative=True)
            [7.5, 7.5, 7.5]
            >>> scale_position([7.5, 7.5, 7.5], 15.0, is_relative=False)
            [7.5, 7.5, 7.5]
        """
        if is_relative:
            return [pos * lattice_constant for pos in position]
        else:
            # Already absolute coordinates
            return position.copy()
