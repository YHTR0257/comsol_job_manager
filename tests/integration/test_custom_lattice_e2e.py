"""End-to-end test for custom lattice job generation.

This script tests the complete pipeline:
1. Load YAML file
2. Generate parametric sweep
3. Generate Java files for each job
"""

from pathlib import Path
from src.parsers.yaml_loader import load_custom_lattice_yaml
from src.services.parametric_generator import ParametricGenerator
from src.services.job_generator import JobGenerator

def test_e2e_custom_lattice():
    """Test end-to-end job generation from YAML."""

    # 1. Load YAML
    print("=" * 80)
    print("Step 1: Loading YAML file")
    print("=" * 80)
    yaml_path = Path("/workspace/examples/custom_lattice/simple_cubic.yml")
    job = load_custom_lattice_yaml(yaml_path)
    print(f"✓ Loaded job: {job.job.name}")
    print(f"  Spheres: {len(job.geometry.spheres)}")
    print(f"  Beams: {len(job.geometry.beams)}")
    print()

    # 2. Generate parametric sweep
    print("=" * 80)
    print("Step 2: Generating parametric sweep")
    print("=" * 80)
    generator = ParametricGenerator(job)
    param_sets = generator.generate_parameter_sets()
    print(f"✓ Generated {len(param_sets)} parameter sets")

    # Show first few parameter sets
    for i, ps in enumerate(param_sets[:3], 1):
        print(f"\n  {ps.job_id}:")
        print(f"    sphere.radius: {ps.parameters['sphere.radius']}")
        print(f"    beam.thickness: {ps.parameters['beam.thickness']}")

    if len(param_sets) > 3:
        print(f"\n  ... and {len(param_sets) - 3} more")
    print()

    # 3. Generate Java files
    print("=" * 80)
    print("Step 3: Generating Java files")
    print("=" * 80)

    job_gen = JobGenerator(
        template_dir=Path("/workspace/templates"),
        output_base_dir=Path("/workspace/tests/output/custom_lattice")
    )

    # Generate first job as a test
    test_param_set = param_sets[0]
    print(f"Generating job for: {test_param_set.job_id}")
    print(f"  Parameters: {test_param_set.parameters}")

    result = job_gen.generate_custom_lattice_job(
        custom_job=job,
        param_set=test_param_set
    )

    print(f"\n✓ Generated job files:")
    print(f"  Job directory: {result['job_dir']}")
    print(f"  Java file: {result['java_file']}")
    print(f"  Batch file: {result['batch_file']}")
    print(f"  Metadata file: {result['metadata_file']}")

    # Verify files exist
    java_file = Path(result['java_file'])
    if java_file.exists():
        print(f"\n✓ Java file exists ({java_file.stat().st_size} bytes)")

        # Check for key content in Java file
        content = java_file.read_text()

        checks = [
            (f"class {test_param_set.job_id}", "Class declaration"),
            ("double[][] points", "Sphere positions array"),
            ("double[][][] lines", "Beam endpoints array"),
            ("points = new double[][]", "Sphere positions initialization"),
            ("lines = new double[][][]", "Beam endpoints initialization"),
            ("model.component().create", "COMSOL model creation"),
        ]

        print("\n  Content verification:")
        for check_str, description in checks:
            if check_str in content:
                print(f"    ✓ {description}")
            else:
                print(f"    ✗ {description} - NOT FOUND!")
    else:
        print(f"\n✗ Java file was not created!")

    print("\n" + "=" * 80)
    print("End-to-end test completed")
    print("=" * 80)

if __name__ == "__main__":
    test_e2e_custom_lattice()
