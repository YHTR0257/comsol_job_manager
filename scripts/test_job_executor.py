"""Test script for COMSOL job executor.

This script demonstrates how to execute generated COMSOL jobs from WSL.
It provides utilities for executing single jobs, verifying results,
and monitoring execution status.
"""

import sys
from pathlib import Path
import argparse

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.batch_executor import BatchExecutor, BatchExecutionError
from src.config.loader import setup_logging, get_logger

# Setup logging
setup_logging({
    'logging': {
        'level': 'INFO',
        'console': {'enabled': True}
    }
})

logger = get_logger("test_job_executor")


def verify_job_structure(job_dir: Path) -> bool:
    """Verify that job directory has required files.

    Args:
        job_dir: Path to job directory

    Returns:
        True if all required files exist, False otherwise
    """
    # run.bat is always required
    if not (job_dir / 'run.bat').exists():
        logger.error(f"  ✗ Missing: run.bat")
        return False
    logger.info(f"  ✓ Found: run.bat")

    # Either config.yml (standard lattice) or metadata.yml (custom lattice) is required
    has_config = (job_dir / 'config.yml').exists()
    has_metadata = (job_dir / 'metadata.yml').exists()

    if not (has_config or has_metadata):
        logger.error(f"  ✗ Missing: config.yml or metadata.yml")
        return False

    if has_config:
        logger.info(f"  ✓ Found: config.yml (standard lattice)")
    if has_metadata:
        logger.info(f"  ✓ Found: metadata.yml (custom lattice)")

    missing_files = []

    # Check for Java file (may have different names)
    java_files = list(job_dir.glob("*.java"))
    if not java_files:
        logger.error("  ✗ Missing: Java file (*.java)")
        missing_files.append("*.java")
    else:
        logger.info(f"  ✓ Found: {java_files[0].name}")

    # Check for results directory
    results_dir = job_dir / 'results'
    if not results_dir.exists():
        logger.warning(f"  ⚠ Results directory does not exist: {results_dir}")
        logger.info(f"    Creating results directory...")
        results_dir.mkdir(parents=True, exist_ok=True)
    else:
        logger.info(f"  ✓ Found: results/ directory")

    return len(missing_files) == 0


def check_execution_results(job_dir: Path) -> dict:
    """Check if execution generated expected output files.

    Args:
        job_dir: Path to job directory

    Returns:
        Dictionary with result status
    """
    results_dir = job_dir / 'results'
    result_status = {
        'results_dir_exists': results_dir.exists(),
        'log_file': None,
        'output_file': None,
        'error_files': [],
        'all_files': []
    }

    if not results_dir.exists():
        logger.warning("Results directory does not exist")
        return result_status

    # List all files in results directory
    all_files = list(results_dir.glob("*"))
    result_status['all_files'] = [f.name for f in all_files]

    # Check for log file
    log_file = results_dir / 'run.log'
    if log_file.exists():
        result_status['log_file'] = log_file
        logger.info(f"  ✓ Found log file: {log_file.name}")

        # Check log file size
        log_size = log_file.stat().st_size
        logger.info(f"    Log file size: {log_size:,} bytes")

        # Show last few lines if exists
        if log_size > 0:
            try:
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    if lines:
                        logger.info("    Last 5 lines of log:")
                        for line in lines[-5:]:
                            logger.info(f"      {line.rstrip()}")
            except Exception as e:
                logger.warning(f"    Could not read log file: {e}")
    else:
        logger.warning("  ✗ Log file not found")

    # Check for output mph file
    mph_files = list(results_dir.glob("*.mph"))
    if mph_files:
        result_status['output_file'] = mph_files[0]
        logger.info(f"  ✓ Found output file: {mph_files[0].name}")
        logger.info(f"    Size: {mph_files[0].stat().st_size:,} bytes")
    else:
        logger.warning("  ✗ No .mph output file found")

    # Check for error files
    error_patterns = ['*.err', 'error*.txt', '*_error.log']
    for pattern in error_patterns:
        error_files = list(results_dir.glob(pattern))
        if error_files:
            result_status['error_files'].extend(error_files)

    if result_status['error_files']:
        logger.warning(f"  ⚠ Found {len(result_status['error_files'])} error file(s)")
        for ef in result_status['error_files']:
            logger.warning(f"    {ef.name}")

    # Show all files found
    if all_files:
        logger.info(f"  All files in results/ ({len(all_files)}):")
        for f in all_files:
            logger.info(f"    - {f.name} ({f.stat().st_size:,} bytes)")

    return result_status


def execute_single_job(job_dir: Path, timeout: int = 3600,
                       check_comsol: bool = True) -> bool:
    """Execute a single COMSOL job.

    Args:
        job_dir: Path to job directory
        timeout: Execution timeout in seconds
        check_comsol: Whether to check COMSOL availability first

    Returns:
        True if execution succeeded, False otherwise
    """
    logger.info("=" * 60)
    logger.info(f"Executing job: {job_dir.name}")
    logger.info("=" * 60)

    # Verify job structure
    logger.info("Verifying job structure...")
    if not verify_job_structure(job_dir):
        logger.error("Job structure verification failed")
        return False

    # Initialize executor
    executor = BatchExecutor(timeout=timeout)

    # Check COMSOL availability
    if check_comsol:
        logger.info("Checking COMSOL availability...")
        if executor.check_comsol_available():
            logger.info("  ✓ COMSOL is available")
        else:
            logger.warning("  ⚠ COMSOL not found in PATH")
            logger.warning("    Execution may fail if COMSOL is not configured")

    # Execute batch file
    batch_file = job_dir / "run.bat"
    logger.info(f"Executing: {batch_file}")
    logger.info(f"Timeout: {timeout}s ({timeout/60:.1f} minutes)")

    try:
        result = executor.execute_batch(batch_file, timeout=timeout)

        logger.info("=" * 60)
        logger.info("Execution completed")
        logger.info("=" * 60)
        logger.info(f"Exit code: {result.returncode}")

        # Show stdout if available
        if result.stdout:
            logger.info("STDOUT:")
            for line in result.stdout.splitlines()[:50]:  # First 50 lines
                logger.info(f"  {line}")
            if len(result.stdout.splitlines()) > 50:
                logger.info(f"  ... ({len(result.stdout.splitlines()) - 50} more lines)")

        # Show stderr if available
        if result.stderr:
            logger.warning("STDERR:")
            for line in result.stderr.splitlines()[:50]:  # First 50 lines
                logger.warning(f"  {line}")
            if len(result.stderr.splitlines()) > 50:
                logger.warning(f"  ... ({len(result.stderr.splitlines()) - 50} more lines)")

        # Check results
        logger.info("=" * 60)
        logger.info("Checking execution results...")
        logger.info("=" * 60)
        result_status = check_execution_results(job_dir)

        # Determine success
        success = (
            result.returncode == 0 and
            result_status['log_file'] is not None
        )

        if success:
            logger.info("✓ Job execution completed successfully")
        else:
            logger.error("✗ Job execution failed or incomplete")

        return success

    except subprocess.TimeoutExpired:
        logger.error(f"✗ Execution timed out after {timeout}s")
        logger.info("Checking partial results...")
        check_execution_results(job_dir)
        return False

    except BatchExecutionError as e:
        logger.error(f"✗ Batch execution error: {e}")
        return False

    except Exception as e:
        logger.error(f"✗ Unexpected error: {e}", exc_info=True)
        return False


def list_available_jobs(base_dir: Path) -> list[Path]:
    """List all available job directories.

    Args:
        base_dir: Base directory containing job folders

    Returns:
        List of job directory paths
    """
    if not base_dir.exists():
        logger.warning(f"Base directory does not exist: {base_dir}")
        return []

    # Find all job_* directories
    job_dirs = sorted(
        [d for d in base_dir.glob("job_*") if d.is_dir()],
        reverse=True  # Most recent first
    )

    return job_dirs


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Execute COMSOL jobs from WSL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Execute specific job (standard lattice)
  python scripts/test_job_executor.py -j jobs/comsol/job_20251119_161230

  # Execute custom lattice job
  python scripts/test_job_executor.py -j jobs/comsol/run_20251130_120000/job_001

  # Execute entire custom lattice run (all jobs in run directory)
  python scripts/test_job_executor.py -j jobs/comsol/run_20251130_120000

  # Execute with custom timeout (2 hours)
  python scripts/test_job_executor.py -j jobs/comsol/job_20251119_161230 -t 7200

  # List available jobs
  python scripts/test_job_executor.py -l

  # Execute most recent job
  python scripts/test_job_executor.py --latest
        """
    )

    parser.add_argument(
        '-j', '--job-dir',
        type=str,
        help='Path to job directory to execute'
    )
    parser.add_argument(
        '-t', '--timeout',
        type=int,
        default=3600,
        help='Execution timeout in seconds (default: 3600 = 1 hour)'
    )
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List available jobs in jobs/comsol/'
    )
    parser.add_argument(
        '--latest',
        action='store_true',
        help='Execute the most recent job'
    )
    parser.add_argument(
        '--no-check-comsol',
        action='store_true',
        help='Skip COMSOL availability check'
    )

    args = parser.parse_args()

    # Determine base directory
    project_root = Path(__file__).parent.parent
    jobs_base_dir = project_root / "jobs" / "comsol"

    # List jobs mode
    if args.list:
        logger.info("=" * 60)
        logger.info("Available COMSOL jobs")
        logger.info("=" * 60)

        job_dirs = list_available_jobs(jobs_base_dir)

        if not job_dirs:
            logger.info("No jobs found")
            return 0

        for i, job_dir in enumerate(job_dirs, 1):
            # Check if job has been executed
            results_dir = job_dir / "results"
            has_results = results_dir.exists() and any(results_dir.iterdir())

            status = "✓ (executed)" if has_results else "○ (not executed)"
            logger.info(f"{i:2d}. {job_dir.name:30s} {status}")

        logger.info("=" * 60)
        logger.info(f"Total: {len(job_dirs)} jobs")
        return 0

    # Determine job directory
    job_dir = None
    if args.latest:
        logger.info("Finding most recent job...")
        job_dirs = list_available_jobs(jobs_base_dir)
        if job_dirs:
            job_dir = job_dirs[0]
            logger.info(f"Selected: {job_dir.name}")
        else:
            logger.error("No jobs found")
            return 1
    elif args.job_dir:
        job_dir = Path(args.job_dir)
    else:
        parser.print_help()
        return 1

    # Verify job directory exists
    if not job_dir.exists():
        logger.error(f"Job directory does not exist: {job_dir}")
        return 1

    # Check if this is a run directory (contains multiple jobs)
    # or a single job directory
    sub_jobs = sorted([d for d in job_dir.glob("job_*") if d.is_dir()])

    if sub_jobs:
        # This is a run directory with multiple jobs
        logger.info(f"Detected run directory with {len(sub_jobs)} jobs")
        logger.info("=" * 60)

        successes = 0
        failures = 0

        for i, sub_job in enumerate(sub_jobs, 1):
            logger.info(f"\nExecuting job {i}/{len(sub_jobs)}: {sub_job.name}")
            success = execute_single_job(
                job_dir=sub_job,
                timeout=args.timeout,
                check_comsol=not args.no_check_comsol
            )

            if success:
                successes += 1
            else:
                failures += 1

            logger.info("")

        # Summary
        logger.info("=" * 60)
        logger.info("Run Summary")
        logger.info("=" * 60)
        logger.info(f"Total jobs: {len(sub_jobs)}")
        logger.info(f"Successful: {successes}")
        logger.info(f"Failed: {failures}")
        logger.info("=" * 60)

        return 0 if failures == 0 else 1
    else:
        # Single job directory
        success = execute_single_job(
            job_dir=job_dir,
            timeout=args.timeout,
            check_comsol=not args.no_check_comsol
        )

        return 0 if success else 1


if __name__ == "__main__":
    import subprocess  # Need this for TimeoutExpired
    sys.exit(main())
