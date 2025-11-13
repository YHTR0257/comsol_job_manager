"""Test script for batch executor.

This script demonstrates and tests the BatchExecutor functionality.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services import BatchExecutor, BatchExecutionError, execute_job
from src.services import JobGenerator
from src.config.loader import setup_logging, get_logger

# Setup logging
setup_logging({
    'logging': {
        'level': 'INFO',
        'console': {'enabled': True}
    }
})

logger = get_logger("test_batch_executor")


def test_comsol_availability():
    """Test 1: Check if COMSOL is available in Windows PATH."""
    logger.info("=" * 60)
    logger.info("Test 1: COMSOL Availability Check")
    logger.info("=" * 60)

    executor = BatchExecutor()
    is_available = executor.check_comsol_available()

    if is_available:
        logger.info("✓ COMSOL is available in Windows PATH")
        return True
    else:
        logger.warning("⚠ COMSOL not found in Windows PATH")
        logger.warning("  This is expected if COMSOL is not installed")
        logger.warning("  or not added to PATH")
        return True  # Not a failure, just informational


def test_path_conversion():
    """Test 2: WSL to Windows path conversion."""
    logger.info("\n" + "=" * 60)
    logger.info("Test 2: Path Conversion")
    logger.info("=" * 60)

    executor = BatchExecutor()

    test_paths = [
        "/workspace",
        "/workspace/jobs/comsol",
        Path("/tmp/test"),
    ]

    for wsl_path in test_paths:
        try:
            windows_path = executor.convert_wsl_to_windows_path(wsl_path)
            logger.info(f"✓ {wsl_path}")
            logger.info(f"  → {windows_path}")
        except Exception as e:
            logger.error(f"✗ Failed to convert {wsl_path}: {e}")
            return False

    logger.info("✓ All path conversions successful")
    return True


def test_simple_batch_execution():
    """Test 3: Execute a simple test batch file."""
    logger.info("\n" + "=" * 60)
    logger.info("Test 3: Simple Batch Execution")
    logger.info("=" * 60)

    # Create a simple test batch file
    project_root = Path(__file__).parent.parent
    test_batch = project_root / "jobs" / "test_simple.bat"
    test_batch.parent.mkdir(parents=True, exist_ok=True)

    # Write simple batch file
    batch_content = """@echo off
echo Hello from Windows!
echo Current directory: %CD%
echo Date: %DATE%
echo Time: %TIME%
exit /b 0
"""
    with open(test_batch, 'w') as f:
        f.write(batch_content)

    logger.info(f"Created test batch file: {test_batch}")

    executor = BatchExecutor(timeout=30)

    try:
        result = executor.execute_batch(test_batch)

        logger.info(f"Exit code: {result.returncode}")
        logger.info(f"STDOUT:\n{result.stdout}")

        if result.returncode == 0:
            logger.info("✓ Simple batch execution successful")
            return True
        else:
            logger.error(f"✗ Batch returned non-zero exit code: {result.returncode}")
            return False

    except Exception as e:
        logger.error(f"✗ Batch execution failed: {e}")
        return False
    finally:
        # Cleanup
        if test_batch.exists():
            test_batch.unlink()
            logger.debug(f"Cleaned up test file: {test_batch}")


def test_job_execution_dryrun():
    """Test 4: Generate and prepare a job for execution (dry run)."""
    logger.info("\n" + "=" * 60)
    logger.info("Test 4: Job Execution Dry Run")
    logger.info("=" * 60)

    project_root = Path(__file__).parent.parent

    # Generate a test job
    generator = JobGenerator(
        template_dir=project_root / "templates",
        output_base_dir=project_root / "jobs" / "comsol"
    )

    params = {
        'lattice_constant': 1.0,
        'sphere_radius_ratio': 0.15,
        'bond_radius_ratio': 0.08,
        'num_cells': 2,  # Smaller for test
        'file_name': 'test_batch_exec',
    }

    try:
        result = generator.generate_job(params, comsol_command="comsol")
        job_dir = result['job_dir']
        batch_file = result['batch_file']

        logger.info(f"✓ Generated test job: {job_dir.name}")
        logger.info(f"  Batch file: {batch_file}")

        # Check if batch file exists
        if not batch_file.exists():
            logger.error(f"✗ Batch file not found: {batch_file}")
            return False

        logger.info("✓ Batch file exists and is ready for execution")

        # Show what would be executed
        executor = BatchExecutor()
        windows_path = executor.convert_wsl_to_windows_path(batch_file)
        logger.info(f"  Windows path: {windows_path}")

        logger.info("\n  Note: Actual COMSOL execution is skipped in dry run")
        logger.info("  To execute, run:")
        logger.info(f"    python -c \"from src.services import execute_job; execute_job('{job_dir}')\"")

        return True

    except Exception as e:
        logger.error(f"✗ Job generation failed: {e}")
        return False


def test_convenience_function():
    """Test 5: Test execute_job convenience function."""
    logger.info("\n" + "=" * 60)
    logger.info("Test 5: Convenience Function")
    logger.info("=" * 60)

    # Create a mock job directory with a simple batch file
    project_root = Path(__file__).parent.parent
    mock_job_dir = project_root / "jobs" / "test_mock_job"
    mock_job_dir.mkdir(parents=True, exist_ok=True)

    batch_file = mock_job_dir / "run.bat"
    batch_content = """@echo off
echo Mock COMSOL job execution
echo Job directory: %CD%
timeout /t 2 /nobreak > nul
echo Simulation complete (mock)
exit /b 0
"""
    with open(batch_file, 'w') as f:
        f.write(batch_content)

    logger.info(f"Created mock job at: {mock_job_dir}")

    try:
        result = execute_job(mock_job_dir, timeout=30)

        logger.info(f"Exit code: {result.returncode}")
        logger.info(f"Output:\n{result.stdout}")

        if result.returncode == 0:
            logger.info("✓ Convenience function works correctly")
            return True
        else:
            logger.error(f"✗ Non-zero exit code: {result.returncode}")
            return False

    except Exception as e:
        logger.error(f"✗ Execution failed: {e}")
        return False
    finally:
        # Cleanup
        if batch_file.exists():
            batch_file.unlink()
        if mock_job_dir.exists():
            mock_job_dir.rmdir()
        logger.debug("Cleaned up mock job directory")


def main():
    """Run all tests."""
    logger.info("Starting BatchExecutor tests...\n")

    tests = [
        ("COMSOL Availability", test_comsol_availability),
        ("Path Conversion", test_path_conversion),
        ("Simple Batch Execution", test_simple_batch_execution),
        ("Job Execution Dry Run", test_job_execution_dryrun),
        ("Convenience Function", test_convenience_function),
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
