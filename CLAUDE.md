# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the ESP (Electronic Structure Properties) project - a materials science research tool that combines COMSOL Multiphysics automation for lattice structure optimization with VASP/VASPKIT data analysis. The project is written primarily in Python with Japanese documentation.

**Core Purpose:**
- Automate COMSOL Multiphysics simulations for lattice structure shape optimization
- Support custom lattice structures with parametric studies
- Load and analyze VASP (Vienna Ab initio Simulation Package) calculation results
- Store elastic properties, mechanical properties, and calculation metadata in PostgreSQL
- Support materials science research workflows (k-point convergence analysis, elastic tensor calculations)

## Development Commands

### Custom Lattice Job Generation (Recommended)

```bash
# Generate jobs from custom lattice YAML definition
python scripts/generate_custom_lattice_job.py -i templates/lattice_setting/fcc.yml

# Generate with specific output directory
python scripts/generate_custom_lattice_job.py -i templates/lattice_setting/simple_cubic.yml -o jobs/comsol

# Generate with custom run ID
python scripts/generate_custom_lattice_job.py -i templates/lattice_setting/fcc.yml --run-id test_run_01

# Generate with 8 cores and skip .mph file saving
python scripts/generate_custom_lattice_job.py -i templates/lattice_setting/fcc.yml --num-cores 8 --no-save-mph

# Skip confirmation for batch generation
python scripts/generate_custom_lattice_job.py -i templates/lattice_setting/fcc.yml -y
```

Available lattice settings:
- `templates/lattice_setting/fcc.yml` - Face-Centered Cubic structure
- `templates/lattice_setting/simple_cubic.yml` - Simple Cubic structure
- `templates/lattice_setting/mimetic_Al.yml` - Mimetic Aluminum structure
- `templates/lattice_setting/mimetic_Cu.yml` - Mimetic Copper structure

### Job Execution

```bash
# Execute jobs from a run directory
python scripts/execute_comsol_job.py -j jobs/comsol/run_YYYYMMDD_HHMMSS

# Execute with custom timeout (2 hours)
python scripts/execute_comsol_job.py -j jobs/comsol/run_YYYYMMDD_HHMMSS -t 7200

# Execute specific job within a run
python scripts/execute_comsol_job.py -j jobs/comsol/run_YYYYMMDD_HHMMSS/job_001
```

### Legacy: Simple Job Generation

```bash
# Generate a single COMSOL job (legacy method)
python -c "
from src.services import JobGenerator
from pathlib import Path

generator = JobGenerator(
    template_dir=Path('templates'),
    output_base_dir=Path('jobs/comsol')
)

params = {
    'lattice_constant': 1.0,
    'sphere_radius_ratio': 0.15,
    'bond_radius_ratio': 0.08,
    'num_cells': 3,
    'poisson_ratio': 0.3,
}

result = generator.generate_job(params)
print(f'Generated: {result[\"job_dir\"]}')
"

# Run job generation test suite
python scripts/test_job_generator.py
```

### Database Management

```bash
# Start development environment (PostgreSQL dev + test databases)
docker compose -f docker-compose.dev.yml up -d

# Start production environment
docker compose -f docker-compose.prod.yml up -d

# Access development database
# Connection string: postgresql://esp_user:esp_password@localhost:5432/esp_dev

# Access test database
# Connection string: postgresql://esp_user:esp_password@localhost:5433/esp_test
```

### Testing

```bash
# Run all tests (when pytest is configured)
pytest tests/

# Run specific test file
pytest tests/unit/test_job_generator.py

# Run with verbose output
pytest -v tests/

# Run custom lattice tests
pytest tests/unit/test_custom_lattice_job_generation.py
pytest tests/unit/test_geometry_validator.py
pytest tests/unit/test_parametric_generator.py
```

### Environment Setup

```bash
# Set environment in .env file
ENV=development  # or production

# The config system automatically maps:
# development/dev -> configs/dev/
# production/prod -> configs/prod/
```

## Architecture

### Core System Flow

```
WSL/Linux Environment → Job Generation → Windows COMSOL Execution
                     ↓
              PostgreSQL Database
                     ↓
         Result Analysis & Storage
```

### Custom Lattice Workflow

```
YAML Definition → Parser → Geometry Builder → Validator
                                                  ↓
                            Job Generator ← Template (Jinja2)
                                  ↓
                            Batch Executor → Windows COMSOL
                                  ↓
                         Result Visualization
```

### Key Components

**Configuration System** (`src/config/loader.py`)
- Environment-aware config loading from `configs/{dev,prod}/*.yml`
- Supports placeholder interpolation with `${key.path}` syntax
- Centralized logging setup with console and rotating file handlers
- Project logger name: `"esp"`

**Database Layer** (`src/data/db.py`)
- SQLAlchemy 2.0 style with connection pooling
- `DatabaseManager` class for session management
- Context manager pattern: `with session_scope() as session:`
- Global instance accessible via `get_db_manager()` and `get_session()`
- Auto-detects SQLite vs PostgreSQL and configures appropriately

**Data Models** (`src/data/models/`)
- `Base`: SQLAlchemy declarative base with `TimestampMixin`
- `MaterialSystem`: Material composition, lattice parameters, crystal structure
- `VASPResult`: DFT calculation results, k-points, convergence, elastic constants
- `ElasticConstants`: Full 6x6 stiffness (C_ij) and compliance (S_ij) tensors
- `MechanicalProperties`: Voigt-Reuss-Hill averages, anisotropy, wave velocities, Debye temperature
- `CustomLatticeJob`: Custom lattice structure definition from YAML

**VASP Data Loading** (`src/data/vasp.py`)
- Parse POSCAR files → pymatgen Structure objects
- Parse KPOINTS files → k-point grid information
- Parse ELASTIC_TENSOR files → 6x6 elastic tensor + individual constants
- Analyze k-point convergence from CSV data
- Returns `VASPCalculation` dataclass

**Parquet Feature Loading** (`src/data/parquet_loader.py`)
- Load feature matrices from Parquet files (replaces NPZ format)
- Support for multiple feature sets with prefixes (e.g., `flatten_`, `shape_`)
- Convert legacy NPZ files to Parquet
- Returns (ids, X) or (ids, X, feature_names)

### COMSOL Automation Components

**Job Generator** (`src/services/job_generator.py`)
- Generate Java/Batch/Config files from Jinja2 templates
- Supports two generation modes:
  - Legacy: Simple job generation (`generate_job()`)
  - Custom Lattice: Advanced geometry-based generation (`generate_custom_lattice_job()`, `generate_parametric_study_jobs()`)
- Job ID format: `job_YYYYMMDD_HHMMSS` (legacy) or `run_YYYYMMDD_HHMMSS/job_NNN` (custom lattice)
- Output directory: `jobs/comsol/job_YYYYMMDD_HHMMSS/` or `jobs/comsol/run_YYYYMMDD_HHMMSS/job_NNN/`
- Templates:
  - `templates/simulation.java.j2` (legacy)
  - `templates/custom_lattice.java.j2` (custom lattice)
  - `templates/run.bat.j2` (batch execution)
- Custom Jinja2 delimiters to avoid conflicts with Java code: `<% %>`, `<< >>`, `<# #>`
- Assumes `comsol` command is in Windows PATH

**Geometry Builder** (`src/services/geometry_builder.py`)
- Build custom lattice geometry from YAML definitions
- Apply parametric transformations to spheres and beams
- Generate geometry data for COMSOL templates
- Support for sphere radius ratios and beam thickness ratios

**Parametric Generator** (`src/services/parametric_generator.py`)
- Generate parameter sets for parametric studies
- Support for range, linspace, and logspace sweeps
- Multi-dimensional parameter sweeps with Cartesian product
- Job ID generation for parametric runs

**Geometry Validator** (`src/validators/geometry_validator.py`)
- Validate custom lattice geometries before job generation
- Check for sphere overlaps
- Verify beam-sphere connections
- Ensure beam thickness < sphere radius
- Minimum difference check (0.01mm) to prevent COMSOL geometry errors

**Template Validator** (`src/validators/template_validator.py`)
- Validate generated Java code from Jinja2 templates
- Check for unrendered template variables
- Detect Java syntax errors
- Prevent common template mistakes

**YAML Parser** (`src/parsers/yaml_loader.py`)
- Load and validate custom lattice YAML definitions
- Parse geometry, materials, mesh, and study configurations
- Validate parametric sweep definitions
- Support for strict and lenient validation modes

**Batch Executor** (`src/services/batch_executor.py`)
- Execute Windows batch files from WSL via cmd.exe
- Auto-detects WSL environment
- WSL ↔ Windows path conversion with `wslpath`
- Synchronous and asynchronous execution modes
- Timeout management and error handling
- `execute_job()` convenience function for quick execution

**Parametric Study Visualizer** (`src/visualization/parametric_study_visualizer.py`)
- Visualize results from parametric studies
- Generate plots for parameter sweeps
- Support for 1D, 2D, and multi-dimensional data
- Export plots in various formats (PNG, SVG, PDF)

**Result Analyzer** (`src/services/result_analyzer.py`) (Planned)
- Parse kirchhoff.txt and maxmises.txt
- Calculate stiffness matrices and elastic constants
- Evaluate objective functions for optimization

**Optuna Optimizer** (`src/optimizers/optuna_optimizer.py`) (Planned)
- Bayesian optimization for lattice structure parameters
- Integration with job generation → execution → analysis pipeline

## Coding Standards

**Style:** PEP 8 compliant, 79 character line length, 4 space indentation

**Docstrings:** Google Style with triple double quotes
```python
def function_name(arg1: str, arg2: int) -> bool:
    """Short description.

    Longer description if needed.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ValueError: When invalid input
    """
```

**Naming Conventions:**
- Files/modules/functions/variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`

**Type Hints:** Use where applicable, especially for public APIs

**Git Workflow:** GitHub Flow with Conventional Commits
- Format: `<type>(<scope>): <description>`
- Types: feat, fix, docs, style, refactor, test, chore
- Feature branches from main, PRs for code review

## Key Design Patterns

**Environment Configuration:**
```python
from src.config.loader import (
    get_current_env,
    get_config_path_for_env,
    load_config,
    setup_logging,
    get_logger
)

# Get config for current environment
config_path = get_config_path_for_env('training')  # or 'elf_features'
cfg = load_config(config_path)

# Setup logging from config
logger = setup_logging(cfg)
# Or get child logger
logger = get_logger('my_module')
```

**Database Operations:**
```python
from src.data.db import session_scope, init_db
from src.data.models import MaterialSystem, VASPResult

# Initialize database (usually done once at startup)
db_manager = init_db(create_tables=True)

# Use context manager for transactions
with session_scope() as session:
    material = MaterialSystem(
        name='Aluminum',
        formula='Al',
        crystal_system='FCC'
    )
    session.add(material)
    # Auto-commits on success, rolls back on exception
```

**VASP Data Loading:**
```python
from src.data.vasp import load_vasp_calculation, load_elastic_constants_csv, analyze_kpoint_convergence

# Load from calculation directory
calc = load_vasp_calculation('path/to/vasp/calc')
print(calc.structure)  # pymatgen Structure
print(calc.elastic_constants)  # {'c11': ..., 'c12': ..., 'c44': ...}

# Load k-point convergence study
df = load_elastic_constants_csv('convergence.csv')
analysis = analyze_kpoint_convergence(df)
```

**Feature Loading:**
```python
from src.data.parquet_loader import load_features_from_parquet, load_multiple_feature_sets

# Load all features
ids, X = load_features_from_parquet('features.parquet')

# Load specific feature set
ids, X = load_features_from_parquet('features.parquet', feature_prefix='shape_')

# Load all feature sets at once
data = load_multiple_feature_sets('features.parquet')
X_flatten = data['flatten']
X_shape = data['shape']
```

**Custom Lattice Job Generation:**
```python
from pathlib import Path
from src.parsers import load_custom_lattice_yaml
from src.services import JobGenerator

# Load YAML definition
custom_job = load_custom_lattice_yaml(
    Path('templates/lattice_setting/fcc.yml'),
    validate_geometry=True
)

# Create job generator
generator = JobGenerator(
    template_dir=Path('templates'),
    output_base_dir=Path('jobs/comsol'),
    num_cores=4,
    save_mph=True
)

# Generate parametric study jobs
result = generator.generate_parametric_study_jobs(custom_job)
print(f"Generated {result['total_jobs']} jobs in {result['run_dir']}")
```

**WSL-Windows Path Conversion:**
```python
from src.utils import detect_wsl, wsl_to_windows_path, windows_to_wsl_path

# Check if running in WSL
if detect_wsl():
    print("Running in WSL environment")

# Convert WSL path to Windows path
wsl_path = '/home/user/project/data.txt'
windows_path = wsl_to_windows_path(wsl_path)
# Result: 'C:\\Users\\user\\project\\data.txt' or '\\wsl.localhost\...'

# Convert Windows path to WSL path
windows_path = 'C:\\Users\\user\\data.txt'
wsl_path = windows_to_wsl_path(windows_path)
# Result: '/mnt/c/Users/user/data.txt'

# Use in batch executor (automatically converts paths)
from src.services import BatchExecutor
executor = BatchExecutor()
executor.execute_batch('/path/to/script.bat')
```

## Important Dependencies

**Core:** numpy<2.0 (PyTorch compatibility), pandas>=2.0, pyyaml, python-dotenv
**Database:** SQLAlchemy>=2.0, psycopg2-binary
**Materials Science:** pymatgen>=2024.8.1
**ML/Optimization:** scikit-learn, scipy, lightgbm>=4.0.0, optuna
**Template:** Jinja2
**Visualization:** matplotlib, seaborn
**Testing:** pytest, jupyter lab

## Database Schema Notes

- `material_system`: Basic material info, lattice parameters, composition
- `vasp_results`: Complete DFT calculation metadata (k-points, NSW, strain, convergence, LOBSTER results)
- `elastic_constants`: Full 6x6 tensors (C_ij and S_ij) with eigenvalues
- `mechanical_properties`: Derived properties (moduli, hardness, anisotropy, wave velocities, Debye temperature)

All models inherit from `Base` and use `TimestampMixin` for automatic `created_at`/`updated_at` tracking.

## File System Structure

- `src/config/`: Configuration loading and logging setup
- `src/data/`: Database connection, models, data loading utilities
  - `src/data/models/custom_lattice.py`: Custom lattice structure data models
- `src/services/`: COMSOL job management
  - `job_generator.py`: Job generation from templates
  - `batch_executor.py`: Windows batch execution from WSL
  - `geometry_builder.py`: Custom lattice geometry construction
  - `parametric_generator.py`: Parametric study generation
- `src/validators/`: Input validation
  - `geometry_validator.py`: Validate custom lattice geometries
  - `template_validator.py`: Validate generated Java code
- `src/parsers/`: Input file parsers
  - `yaml_loader.py`: Load and validate custom lattice YAML
- `src/visualization/`: Result visualization
  - `parametric_study_visualizer.py`: Parametric study plots
- `templates/`: Jinja2 templates
  - `simulation.java.j2`: Legacy Java template
  - `custom_lattice.java.j2`: Custom lattice Java template
  - `run.bat.j2`: Batch execution template
  - `lattice_setting/`: Predefined lattice structure YAML files
- `src/optimizers/`: Optimization algorithms (base classes and Optuna implementation)
- `src/utils/`: Utility functions (path_utils for WSL-Windows path conversion)
- `scripts/`: CLI scripts
  - `generate_custom_lattice_job.py`: Generate jobs from YAML
  - `execute_comsol_job.py`: Execute COMSOL jobs
  - `test_job_generator.py`: Test job generation
  - `visualize_parametric_study.py`: Visualize parametric study results
- `docs/`: Design documents (project_design.md, database.md, user_guide.md)
- `docker/`: Docker configurations and requirements.txt
- `configs/dev/` and `configs/prod/`: Environment-specific YAML configs
- `jobs/comsol/`: Job working directories
  - `job_YYYYMMDD_HHMMSS/`: Legacy job directory
  - `run_YYYYMMDD_HHMMSS/job_NNN/`: Custom lattice job directory
- `tests/unit/`: Unit tests (pytest)
- `tests/integration/`: Integration tests

## Development Principles

**KISS:** Avoid over-engineering. This is a research tool, not production software.

**YAGNI:** Don't implement features until they're needed.

**DRY:** Common functionality goes in `src/utils/`.

**Separation of Concerns:**
- Configuration: `src/config/`
- Data access: `src/data/`
- Business logic: `src/services/` and `src/optimizers/`
- I/O parsing: `src/parsers/`
- Validation: `src/validators/`
- Visualization: `src/visualization/`

**Error Handling:**
- Fatal errors (DB connection failure, missing templates): Fail immediately
- Recoverable errors (job timeout, convergence failure): Log and continue
- Validation errors: Report detailed messages with element IDs
- Use logging extensively with appropriate levels (DEBUG, INFO, WARNING, ERROR)

## Context Notes

- Documentation is primarily in Japanese but code/docstrings should be in English
- The project combines two domains: COMSOL lattice optimization + VASP materials analysis
- **WSL-Windows integration is critical**: Python runs in WSL, COMSOL runs on Windows
  - `BatchExecutor` auto-detects WSL environment
  - Uses `cmd.exe` to execute Windows batch files
  - Path conversion via `wslpath` (WSL → Windows)
  - In non-WSL environments (pure Linux/Docker), batch execution logs warnings
- Custom lattice workflow uses YAML definitions for flexible geometry specification
- Parametric studies generate multiple jobs with parameter sweeps
- Geometry validation prevents COMSOL errors by checking sphere overlaps and beam connections
- Template validation ensures generated Java code is syntactically correct
- Database schema is comprehensive for materials science (elastic tensors, mechanical properties, VASPKIT/LOBSTER integration)
- Sequential execution model (no job queue) - one simulation at a time
- Development uses Docker for PostgreSQL, but Python runs on host

## Recent Changes (2025)

- **Custom Lattice System**: Complete implementation of custom lattice structure support
  - YAML-based geometry definitions with sphere and beam primitives
  - Parametric study generation with multi-dimensional sweeps
  - Geometry validation to prevent overlaps and disconnections
  - Template validation for generated Java code
- **New Components**:
  - `GeometryBuilder`: Build geometry from YAML definitions
  - `ParametricGenerator`: Generate parameter sets for sweeps
  - `GeometryValidator`: Validate custom lattice geometries
  - `TemplateValidator`: Validate generated Java templates
  - `ParametricStudyVisualizer`: Visualize parametric study results
- **Templates**: New `custom_lattice.java.j2` with custom Jinja2 delimiters
- **Scripts**: New CLI tool `generate_custom_lattice_job.py` for easy job generation
- **Tests**: Comprehensive test suite for custom lattice features
