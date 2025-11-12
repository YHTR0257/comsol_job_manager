from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
import datetime

from .base import Base


class VASPResult(Base):
    __tablename__ = 'vasp_results'
    id = Column(Integer, primary_key=True)

    # 結果フィールド
    total_energy = Column(Float)
    band_gap = Column(Float)
    material_system_id = Column(Integer, ForeignKey('material_system.id'))
    material_system = relationship("MaterialSystem", back_populates="vasp_results")

    # calculation settings
    k_points_x = Column(Integer, nullable=True)
    k_points_y = Column(Integer, nullable=True)
    k_points_z = Column(Integer, nullable=True)
    k_points_total = Column(Integer, nullable=True)
    k_points_style = Column(String(50), nullable=True)
    nsw = Column(Integer, nullable=True)  # Number of ionic steps (NSW from INCAR)
    run_date = Column(DateTime, nullable=True)
    run_type = Column(String(50), nullable=True)
    topic = Column(String(255))
    job_num = Column(String(50))
    dir_path = Column(String(255))

    # energy fields
    final_energy = Column(Float, nullable=True)
    final_energy_per_atom = Column(Float, nullable=True)
    efermi = Column(Float, nullable=True)

    # deformation fields
    strain = Column(Float, nullable=True)
    deformation_type = Column(String(50), nullable=True)
    deformation_direction = Column(String(50), nullable=True)

    # VASPKIT elastic constants calculation fields
    calculation_type = Column(String(50), default='standard', nullable=True)
    vaspkit_version = Column(String(50), nullable=True)

    # Crystal system information
    crystal_class = Column(String(50), nullable=True)  # "m-3m"
    space_group = Column(String(50), nullable=True)  # "Fm-3m"
    crystal_system = Column(String(50), nullable=True)  # "Cubic system"
    num_independent_constants = Column(Integer, nullable=True)

    # VASPKIT settings
    dimensionality = Column(String(10), nullable=True)  # "2D" or "3D"
    num_strain_cases = Column(Integer, nullable=True)
    strain_range = Column(String(255), nullable=True)

    # Fitting precision
    fitting_precision_c44 = Column(Float, nullable=True)
    fitting_precision_c11_c12_i = Column(Float, nullable=True)
    fitting_precision_c11_c12_ii = Column(Float, nullable=True)

    # Stability
    is_mechanically_stable = Column(Boolean, nullable=True)

    # Convergence information
    is_converged = Column(Boolean, default=False)
    convergence_iteration = Column(Integer, nullable=True)

    # LOBSTER analysis results
    icobi_1st_nn = Column(Float, nullable=True)  # ICOBI value for 1st nearest neighbor
    icobi_2nd_nn = Column(Float, nullable=True)  # ICOBI value for 2nd nearest neighbor
    bond_length_1st_nn = Column(Float, nullable=True)  # Bond length for 1st NN (Angstrom)
    bond_length_2nd_nn = Column(Float, nullable=True)  # Bond length for 2nd NN (Angstrom)

    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    # Relationships
    elastic_constants = relationship(
        "ElasticConstants", uselist=False, back_populates="vasp_result"
    )
    mechanical_properties = relationship(
        "MechanicalProperties", uselist=False, back_populates="vasp_result"
    )

class ElasticConstants(Base):
    """
    Complete 6x6 elastic tensor storage.
    Supports both stiffness tensor (C_ij) and compliance tensor (S_ij).
    All values stored in GPa for stiffness, GPa^-1 for compliance.
    """
    __tablename__ = 'elastic_constants'
    id = Column(Integer, primary_key=True)
    vasp_result_id = Column(Integer, ForeignKey('vasp_results.id'))

    # Stiffness Tensor C_ij (GPa) - 21 independent components
    c11 = Column(Float, nullable=True)
    c12 = Column(Float, nullable=True)
    c13 = Column(Float, nullable=True)
    c14 = Column(Float, nullable=True)
    c15 = Column(Float, nullable=True)
    c16 = Column(Float, nullable=True)
    c22 = Column(Float, nullable=True)
    c23 = Column(Float, nullable=True)
    c24 = Column(Float, nullable=True)
    c25 = Column(Float, nullable=True)
    c26 = Column(Float, nullable=True)
    c33 = Column(Float, nullable=True)
    c34 = Column(Float, nullable=True)
    c35 = Column(Float, nullable=True)
    c36 = Column(Float, nullable=True)
    c44 = Column(Float, nullable=True)
    c45 = Column(Float, nullable=True)
    c46 = Column(Float, nullable=True)
    c55 = Column(Float, nullable=True)
    c56 = Column(Float, nullable=True)
    c66 = Column(Float, nullable=True)

    # Compliance Tensor S_ij (GPa^-1) - 21 independent components
    s11 = Column(Float, nullable=True)
    s12 = Column(Float, nullable=True)
    s13 = Column(Float, nullable=True)
    s14 = Column(Float, nullable=True)
    s15 = Column(Float, nullable=True)
    s16 = Column(Float, nullable=True)
    s22 = Column(Float, nullable=True)
    s23 = Column(Float, nullable=True)
    s24 = Column(Float, nullable=True)
    s25 = Column(Float, nullable=True)
    s26 = Column(Float, nullable=True)
    s33 = Column(Float, nullable=True)
    s34 = Column(Float, nullable=True)
    s35 = Column(Float, nullable=True)
    s36 = Column(Float, nullable=True)
    s44 = Column(Float, nullable=True)
    s45 = Column(Float, nullable=True)
    s46 = Column(Float, nullable=True)
    s55 = Column(Float, nullable=True)
    s56 = Column(Float, nullable=True)
    s66 = Column(Float, nullable=True)

    # Eigenvalues of stiffness matrix (stability analysis)
    eigenvalue_1 = Column(Float, nullable=True)
    eigenvalue_2 = Column(Float, nullable=True)
    eigenvalue_3 = Column(Float, nullable=True)
    eigenvalue_4 = Column(Float, nullable=True)
    eigenvalue_5 = Column(Float, nullable=True)
    eigenvalue_6 = Column(Float, nullable=True)

    # Relationship
    vasp_result = relationship(
        "VASPResult", back_populates="elastic_constants"
    )


class MechanicalProperties(Base):
    """
    Mechanical properties calculated from elastic constants.
    Stores Voigt-Reuss-Hill averages, anisotropic properties, and physical parameters.
    """
    __tablename__ = 'mechanical_properties'
    id = Column(Integer, primary_key=True)
    vasp_result_id = Column(Integer, ForeignKey('vasp_results.id'))

    # === Voigt-Reuss-Hill Averages (GPa) ===
    bulk_modulus_voigt = Column(Float, nullable=True)
    bulk_modulus_reuss = Column(Float, nullable=True)
    bulk_modulus_hill = Column(Float, nullable=True)

    youngs_modulus_voigt = Column(Float, nullable=True)
    youngs_modulus_reuss = Column(Float, nullable=True)
    youngs_modulus_hill = Column(Float, nullable=True)

    shear_modulus_voigt = Column(Float, nullable=True)
    shear_modulus_reuss = Column(Float, nullable=True)
    shear_modulus_hill = Column(Float, nullable=True)

    poissons_ratio_voigt = Column(Float, nullable=True)
    poissons_ratio_reuss = Column(Float, nullable=True)
    poissons_ratio_hill = Column(Float, nullable=True)

    # === Pugh's Ratio (B/G) - dimensionless ===
    pugh_ratio_voigt = Column(Float, nullable=True)
    pugh_ratio_reuss = Column(Float, nullable=True)
    pugh_ratio_hill = Column(Float, nullable=True)

    # === Vickers Hardness (GPa) ===
    vickers_hardness_chen_voigt = Column(Float, nullable=True)
    vickers_hardness_chen_reuss = Column(Float, nullable=True)
    vickers_hardness_chen_hill = Column(Float, nullable=True)

    vickers_hardness_tian_voigt = Column(Float, nullable=True)
    vickers_hardness_tian_reuss = Column(Float, nullable=True)
    vickers_hardness_tian_hill = Column(Float, nullable=True)

    # === P-wave Modulus (GPa) ===
    p_wave_modulus_voigt = Column(Float, nullable=True)
    p_wave_modulus_reuss = Column(Float, nullable=True)
    p_wave_modulus_hill = Column(Float, nullable=True)

    # === Anisotropic Properties - Bulk Modulus ===
    bulk_modulus_min = Column(Float, nullable=True)
    bulk_modulus_max = Column(Float, nullable=True)
    bulk_modulus_anisotropy = Column(Float, nullable=True)

    # === Anisotropic Properties - Young's Modulus ===
    youngs_modulus_min = Column(Float, nullable=True)
    youngs_modulus_max = Column(Float, nullable=True)
    youngs_modulus_anisotropy = Column(Float, nullable=True)

    # === Anisotropic Properties - Shear Modulus ===
    shear_modulus_min = Column(Float, nullable=True)
    shear_modulus_max = Column(Float, nullable=True)
    shear_modulus_anisotropy = Column(Float, nullable=True)

    # === Anisotropic Properties - Poisson's Ratio ===
    poissons_ratio_min = Column(Float, nullable=True)
    poissons_ratio_max = Column(Float, nullable=True)
    poissons_ratio_anisotropy = Column(Float, nullable=True)

    # === Anisotropic Properties - Linear Compressibility ===
    linear_compressibility_min = Column(Float, nullable=True)
    linear_compressibility_max = Column(Float, nullable=True)
    linear_compressibility_anisotropy = Column(Float, nullable=True)

    # === Physical Properties ===
    cauchy_pressure = Column(Float, nullable=True)  # GPa
    kleinman_parameter = Column(Float, nullable=True)  # dimensionless
    universal_elastic_anisotropy = Column(Float, nullable=True)  # dimensionless
    chung_buessem_anisotropy = Column(Float, nullable=True)  # dimensionless
    isotropic_poissons_ratio = Column(Float, nullable=True)  # dimensionless

    # === Wave Velocities (m/s) ===
    longitudinal_wave_velocity = Column(Float, nullable=True)
    transverse_wave_velocity = Column(Float, nullable=True)
    average_wave_velocity = Column(Float, nullable=True)

    # === Debye Temperature (K) ===
    debye_temperature = Column(Float, nullable=True)

    # Relationship
    vasp_result = relationship(
        "VASPResult", back_populates="mechanical_properties"
    )