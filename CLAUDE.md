# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the ESP (Electronic Structure Properties) project - a materials science research tool that combines COMSOL Multiphysics automation for lattice structure optimization with VASP/VASPKIT data analysis. The project is written primarily in Python with Japanese documentation.

**Core Purpose:**
- Automate COMSOL Multiphysics simulations for lattice structure shape optimization
- Load and analyze VASP (Vienna Ab initio Simulation Package) calculation results
- Store elastic properties, mechanical properties, and calculation metadata in PostgreSQL
- Support materials science research workflows (k-point convergence analysis, elastic tensor calculations)

## Development Commands

### Job Generation

```bash
# Generate a single COMSOL job
python -c "
from src.services import JobGenerator
from pathlib import Path

generator = JobGenerator(
    template_dir=Path('templates'),
    output_base_dir=Path('jobs/comsol'),
    reference_java_path=Path('tmp/ref/hosoda_ref.java')
)

params = {
    'lattice_constant': 1.0,
    'sphere_radius_ratio': 0.15,
    'bond_radius_ratio': 0.08,
    'num_cells': 3,
    'poisson_ratio': 0.3,
}

result = generator.generate_job(params, comsol_command='comsol')
print(f'Generated: {result[\"job_dir\"]}')
"

# Run test suite
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
```

**Note:** Test infrastructure is not yet implemented. Tests should be placed in `tests/unit/` and use pytest.

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

### COMSOL Automation Components (Planned)

**Job Generator** (`src/services/job_generator.py`)
- Generate Java/Batch/Config files from reference Java implementation
- Job ID format: `job_YYYYMMDD_HHMMSS`
- Output directory: `jobs/comsol/job_YYYYMMDD_HHMMSS/`
- Uses `tmp/ref/hosoda_ref.java` as template base
- Batch file generated from Jinja2 template (`templates/run.bat.j2`)
- Assumes `comsol` command is in Windows PATH

**Batch Executor** (`src/services/batch_executor.py`)
- Execute Windows batch files from WSL via cmd.exe
- Synchronous execution with timeout management
- WSL ↔ Windows path conversion

**Result Analyzer** (`src/services/result_analyzer.py`)
- Parse kirchhoff.txt and maxmises.txt
- Calculate stiffness matrices and elastic constants
- Evaluate objective functions for optimization

**Optuna Optimizer** (`src/optimizers/optuna_optimizer.py`)
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

## Important Dependencies

**Core:** numpy<2.0 (PyTorch compatibility), pandas>=2.0, pyyaml, python-dotenv
**Database:** SQLAlchemy>=2.0, psycopg2-binary
**Materials Science:** pymatgen>=2024.8.1
**ML/Optimization:** scikit-learn, scipy, lightgbm>=4.0.0, optuna
**Testing:** pytest, jupyter lab, matplotlib, seaborn

## Database Schema Notes

- `material_system`: Basic material info, lattice parameters, composition
- `vasp_results`: Complete DFT calculation metadata (k-points, NSW, strain, convergence, LOBSTER results)
- `elastic_constants`: Full 6x6 tensors (C_ij and S_ij) with eigenvalues
- `mechanical_properties`: Derived properties (moduli, hardness, anisotropy, wave velocities, Debye temperature)

All models inherit from `Base` and use `TimestampMixin` for automatic `created_at`/`updated_at` tracking.

## File System Structure

- `src/config/`: Configuration loading and logging setup
- `src/data/`: Database connection, models, data loading utilities
- `src/services/`: COMSOL job management (job_generator, batch_executor, result_analyzer)
- `templates/`: Jinja2 templates (run.bat.j2 for batch file generation)
- `src/optimizers/`: Optimization algorithms (base classes and Optuna implementation)
- `src/parsers/`: Result file parsers (kirchhoff, maxmises)
- `src/utils/`: Utility functions (path conversion, logging helpers)
- `docs/`: Design documents (project_design.md, database.md, user_guide.md)
- `docker/`: Docker configurations and requirements.txt
- `configs/dev/` and `configs/prod/`: Environment-specific YAML configs
- `jobs/comsol/job_YYYYMMDD_HHMMSS/`: Job working directories with results
- `tests/unit/`: Unit tests (pytest)

## Development Principles

**KISS:** Avoid over-engineering. This is a research tool, not production software.

**YAGNI:** Don't implement features until they're needed.

**DRY:** Common functionality goes in `src/utils/`.

**Separation of Concerns:**
- Configuration: `src/config/`
- Data access: `src/data/`
- Business logic: `src/services/` and `src/optimizers/`
- I/O parsing: `src/parsers/`

**Error Handling:**
- Fatal errors (DB connection failure, missing templates): Fail immediately
- Recoverable errors (job timeout, convergence failure): Log and continue
- Use logging extensively with appropriate levels (DEBUG, INFO, WARNING, ERROR)

## Context Notes

- Documentation is primarily in Japanese but code/docstrings should be in English
- The project combines two domains: COMSOL lattice optimization + VASP materials analysis
- WSL-Windows integration is critical for COMSOL automation (runs on Windows)
- Database schema is comprehensive for materials science (elastic tensors, mechanical properties, VASPKIT/LOBSTER integration)
- Sequential execution model (no job queue) - one simulation at a time
- Development uses Docker for PostgreSQL, but Python runs on host
