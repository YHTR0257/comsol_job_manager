"""Material system model for the ESP project."""

from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin


class MaterialSystem(Base, TimestampMixin):
    """Model for material systems (compositions and structures)."""

    __tablename__ = 'material_system'

    id = Column(Integer, primary_key=True)

    # Basic material information
    name = Column(String(255), nullable=False, index=True)
    formula = Column(String(100), nullable=False, index=True)
    crystal_system = Column(String(50), nullable=True)
    space_group = Column(String(50), nullable=True)

    # Structure information
    lattice_a = Column(Float, nullable=True)
    lattice_b = Column(Float, nullable=True)
    lattice_c = Column(Float, nullable=True)
    lattice_alpha = Column(Float, nullable=True)
    lattice_beta = Column(Float, nullable=True)
    lattice_gamma = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)

    # Composition
    composition = Column(Text, nullable=True)  # JSON or string representation
    num_atoms = Column(Integer, nullable=True)

    # Metadata
    source = Column(String(100), nullable=True)  # e.g., "experimental", "dft", "database"
    notes = Column(Text, nullable=True)

    # Relationships
    vasp_results = relationship("VASPResult", back_populates="material_system")

    def __repr__(self):
        return f"<MaterialSystem(id={self.id}, formula='{self.formula}', name='{self.name}')>"