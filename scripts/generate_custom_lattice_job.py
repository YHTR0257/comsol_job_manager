#!/usr/bin/env python3
"""Generate COMSOL jobs from custom lattice YAML definitions.

This script provides a CLI interface to generate COMSOL simulation jobs
from custom lattice YAML files. It supports parametric studies with
automatic job generation for all parameter combinations.

Usage:
    python scripts/generate_custom_lattice_job.py -i lattice.yml
    python scripts/generate_custom_lattice_job.py -i lattice.yml -o jobs/comsol
    python scripts/generate_custom_lattice_job.py -i lattice.yml --run-id my_run
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.parsers import load_custom_lattice_yaml, YAMLParseError
from src.services.job_generator import JobGenerator
from src.services.parametric_generator import get_parameter_summary


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description='Generate COMSOL jobs from custom lattice YAML definitions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate jobs from YAML file
  python scripts/generate_custom_lattice_job.py -i my_lattice.yml

  # Specify output directory
  python scripts/generate_custom_lattice_job.py -i my_lattice.yml -o jobs/custom

  # Specify run ID for easy identification
  python scripts/generate_custom_lattice_job.py -i my_lattice.yml --run-id test_run_01

  # Skip geometry validation (not recommended)
  python scripts/generate_custom_lattice_job.py -i my_lattice.yml --no-validate

  # Skip confirmation for batch generation
  python scripts/generate_custom_lattice_job.py -i my_lattice.yml -y
        """
    )

    parser.add_argument(
        '-i', '--input',
        type=Path,
        required=True,
        help='Path to custom lattice YAML file'
    )

    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=Path('jobs/comsol'),
        help='Base output directory for jobs (default: jobs/comsol)'
    )

    parser.add_argument(
        '-t', '--template-dir',
        type=Path,
        default=Path('templates'),
        help='Directory containing Jinja2 templates (default: templates)'
    )

    parser.add_argument(
        '--run-id',
        type=str,
        default=None,
        help='Custom run ID (auto-generated if not specified)'
    )

    parser.add_argument(
        '--no-validate',
        action='store_true',
        help='Skip geometry validation (not recommended)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '-y', '--yes',
        action='store_true',
        help='Skip confirmation prompts'
    )

    parser.add_argument(
        '--num-cores',
        type=int,
        default=4,
        help='Number of CPU cores to use for COMSOL batch jobs (default: 4)'
    )

    args = parser.parse_args()

    # Print header
    print("=" * 70)
    print("Custom Lattice Job Generator")
    print("=" * 70)
    print()

    # Validate input file exists
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}")
        return 1

    # Load and validate YAML
    print(f"Loading custom lattice definition: {args.input}")
    try:
        custom_job = load_custom_lattice_yaml(
            args.input,
            validate_geometry=not args.no_validate,
            strict=False
        )
        print("✓ YAML loaded and validated successfully")
    except YAMLParseError as e:
        print(f"✗ YAML validation failed:")
        print(f"  {e}")
        return 1
    except Exception as e:
        print(f"✗ Failed to load YAML:")
        print(f"  {e}")
        return 1

    print()

    # Display job information
    print("Job Information:")
    print(f"  Name: {custom_job.job.name}")
    print(f"  Description: {custom_job.job.description}")
    print(f"  Geometry: {len(custom_job.geometry.spheres)} spheres, "
          f"{len(custom_job.geometry.beams)} beams")
    print()

    # Display parametric study information
    from src.services.parametric_generator import ParametricGenerator
    generator = ParametricGenerator(custom_job)
    sweep_info = generator.get_sweep_info()

    if sweep_info['num_sweeps'] > 0:
        print("Parametric Study:")
        print(f"  Number of sweeps: {sweep_info['num_sweeps']}")
        print(f"  Total jobs to generate: {sweep_info['total_jobs']}")
        for i, dim in enumerate(sweep_info['sweep_dimensions'], 1):
            print(f"  Sweep {i}: {dim['parameter']} "
                  f"({dim['num_values']} values)")
    else:
        print("Single job (no parametric sweeps)")

    print()

    # Ask for confirmation if many jobs (unless --yes flag is set)
    if sweep_info['total_jobs'] > 10 and not args.yes:
        response = input(f"Generate {sweep_info['total_jobs']} jobs? [y/N]: ")
        if response.lower() not in ['y', 'yes']:
            print("Cancelled.")
            return 0

    # Create job generator
    try:
        job_gen = JobGenerator(
            template_dir=args.template_dir,
            output_base_dir=args.output,
            num_cores=args.num_cores
        )
    except Exception as e:
        print(f"✗ Failed to initialize job generator:")
        print(f"  {e}")
        return 1

    # Generate jobs
    print("Generating jobs...")
    try:
        result = job_gen.generate_parametric_study_jobs(
            custom_job,
            run_id=args.run_id
        )
    except Exception as e:
        print(f"✗ Job generation failed:")
        print(f"  {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

    print(f"✓ Successfully generated {result['total_jobs']} jobs")
    if result.get('skipped_jobs', 0) > 0:
        print(f"⚠ Skipped {result['skipped_jobs']} jobs due to validation errors")
    print()

    # Display results
    print("Results:")
    print(f"  Run ID: {result['run_id']}")
    print(f"  Run directory: {result['run_dir']}")
    print(f"  Jobs generated: {result['total_jobs']}")
    if result.get('skipped_jobs', 0) > 0:
        print(f"  Jobs skipped: {result['skipped_jobs']}")
        print(f"  (See {result['run_dir']}/metadata.yml for details)")
    print()

    # Show next steps
    print("Next steps:")
    print(f"  1. Review generated jobs in: {result['run_dir']}")
    print(f"  2. Execute jobs using:")
    print(f"     python scripts/execute_comsol_job.py -j {result['run_dir']}")
    print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
