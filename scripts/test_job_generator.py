"""Test script for COMSOL job generator.

This script demonstrates how to use the JobGenerator to create simulation jobs.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.job_generator import JobGenerator, validate_parameters
from src.config.loader import setup_logging, get_logger

# Setup logging
setup_logging({
    'logging': {
        'level': 'INFO',
        'console': {'enabled': True}
    }
})

logger = get_logger("test_job_generator")


def test_basic_job_generation():
    """Test basic job generation with minimal parameters."""
    logger.info("=" * 60)
    logger.info("Test 1: Basic job generation")
    logger.info("=" * 60)

    # Setup paths
    project_root = Path(__file__).parent.parent
    template_dir = project_root / "templates"
    output_dir = project_root / "jobs" / "comsol"

    # Create job generator
    generator = JobGenerator(
        template_dir=template_dir,
        output_base_dir=output_dir
    )

    # Define test parameters
    params = {
        'lattice_constant': 1.0,        # lconst in mm
        'sphere_radius_ratio': 0.15,    # rs = 15% of lconst
        'bond_radius_ratio': 0.08,      # rb = 8% of lconst
        'num_cells': 3,                 # 3x3x3 unit cells
        'shift': 0.0,                   # no shift
        'poisson_ratio': 0.3,           # Poisson's ratio
        'delta': 0.001,                 # delta for strain
        'dstep': '"range(0,0.0002,0.001)"',  # displacement steps
        'lattice_type': 'FCC',          # Face-centered cubic
        'file_name': 'test_fcc_lattice',
        'd_min': 0.0,
        'd_max': 1.5,
    }

    # Validate parameters
    try:
        validate_parameters(params)
        logger.info("✓ Parameters validated successfully")
    except ValueError as e:
        logger.error(f"✗ Parameter validation failed: {e}")
        return False

    # Generate job
    try:
        result = generator.generate_job(
            params=params,
            job_id=None  # Auto-generate
        )

        logger.info("✓ Job generated successfully!")
        logger.info(f"  Job directory: {result['job_dir']}")
        logger.info(f"  Java file: {result['java_file'].name}")
        logger.info(f"  Batch file: {result['batch_file'].name}")
        logger.info(f"  Config file: {result['config_file'].name}")

        # Verify files exist
        for key, path in result.items():
            if not path.exists():
                logger.error(f"✗ Generated file not found: {path}")
                return False

        logger.info("✓ All generated files verified")
        return True

    except Exception as e:
        logger.error(f"✗ Job generation failed: {e}", exc_info=True)
        return False


def test_parametric_sweep():
    """Test generating multiple jobs for parametric sweep."""
    logger.info("\n" + "=" * 60)
    logger.info("Test 2: Parametric sweep generation")
    logger.info("=" * 60)

    project_root = Path(__file__).parent.parent
    template_dir = project_root / "templates"
    output_dir = project_root / "jobs" / "comsol"

    generator = JobGenerator(
        template_dir=template_dir,
        output_base_dir=output_dir
    )

    # Define parameter sweep
    sphere_radii = [0.10, 0.15, 0.20]
    bond_radii = [0.05, 0.08, 0.10]

    logger.info(f"Generating {len(sphere_radii) * len(bond_radii)} jobs...")

    jobs_generated = []

    for rs in sphere_radii:
        for rb in bond_radii:
            params = {
                'lattice_constant': 1.0,
                'sphere_radius_ratio': rs,
                'bond_radius_ratio': rb,
                'num_cells': 3,
                'poisson_ratio': 0.3,
                'delta': 0.001,
                'dstep': '"range(0,0.0002,0.001)"',
                'file_name': f'fcc_rs{int(rs*100)}_rb{int(rb*100)}',
            }

            try:
                result = generator.generate_job(
                    params=params
                )
                jobs_generated.append(result)
                logger.info(f"  ✓ Generated job: rs={rs:.2f}, rb={rb:.2f}")

            except Exception as e:
                logger.error(f"  ✗ Failed for rs={rs:.2f}, rb={rb:.2f}: {e}")
                return False

    logger.info(f"✓ Successfully generated {len(jobs_generated)} jobs")
    return True


def test_parameter_validation():
    """Test parameter validation."""
    logger.info("\n" + "=" * 60)
    logger.info("Test 3: Parameter validation")
    logger.info("=" * 60)

    # Test valid parameters
    valid_params = {
        'lattice_constant': 1.0,
        'sphere_radius_ratio': 0.15,
        'bond_radius_ratio': 0.08,
    }

    try:
        validate_parameters(valid_params)
        logger.info("✓ Valid parameters accepted")
    except ValueError as e:
        logger.error(f"✗ Valid parameters rejected: {e}")
        return False

    # Test invalid parameters
    invalid_cases = [
        ({'sphere_radius_ratio': 0.6}, "sphere_radius_ratio too large"),
        ({'lattice_constant': 1.0, 'poisson_ratio': 0.6}, "poisson_ratio out of range"),
        ({'bond_radius_ratio': -0.1}, "negative bond_radius_ratio"),
    ]

    for params, description in invalid_cases:
        params['lattice_constant'] = 1.0  # Add required param
        try:
            validate_parameters(params)
            logger.error(f"✗ Invalid parameters accepted: {description}")
            return False
        except ValueError:
            logger.info(f"✓ Invalid parameters rejected: {description}")

    logger.info("✓ All validation tests passed")
    return True


def main():
    """Run all tests."""
    logger.info("Starting JobGenerator tests...\n")

    tests = [
        ("Parameter Validation", test_parameter_validation),
        ("Basic Job Generation", test_basic_job_generation),
        ("Parametric Sweep", test_parametric_sweep),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            logger.error(f"Test '{test_name}' crashed: {e}", exc_info=True)
            results.append((test_name, False))

    # Print summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_name, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        logger.info(f"{status}: {test_name}")

    logger.info("=" * 60)
    logger.info(f"Results: {passed}/{total} tests passed")

    if passed == total:
        logger.info("✓ All tests passed!")
        return 0
    else:
        logger.error(f"✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
