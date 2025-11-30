"""Integration test for visualization workflow.

Tests the complete visualization pipeline from config loading to plot generation.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import shutil

from src.config.loader import get_config_path_for_env, load_config
from src.visualization import create_visualizer_from_config


@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for test outputs."""
    tmpdir = Path(tempfile.mkdtemp())
    yield tmpdir
    # Cleanup
    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.fixture
def sample_parametric_results():
    """Create sample parametric study results."""
    np.random.seed(42)
    df = pd.DataFrame({
        'sphere.radius': [0.15, 0.20, 0.25] * 2,
        'beam.thickness': [0.08] * 3 + [0.10] * 3,
        'C11': [100, 120, 140, 110, 130, 150],
        'C12': [40, 50, 60, 45, 55, 65],
        'C44': [30, 35, 40, 32, 37, 42],
        'poisson_ratio': [0.25, 0.28, 0.31, 0.27, 0.30, 0.33],
        'zener_ratio': [0.95, 1.05, 1.15, 1.00, 1.10, 1.20],
    })
    return df


class TestVisualizationIntegration:
    """Integration tests for visualization workflow."""

    def test_dev_config_workflow(self, temp_output_dir, sample_parametric_results):
        """Test complete workflow with dev config."""
        # Load dev config
        config_path = get_config_path_for_env('visualization', env='dev')
        config = load_config(config_path)

        # Override output directory to use temp dir
        config['visualization']['output_dir'] = str(temp_output_dir)

        # Create visualizer
        viz = create_visualizer_from_config(config)

        assert viz.output_dir == temp_output_dir
        assert viz.dpi == 300
        assert viz.fig_format == 'png'

        # Generate plots
        df = sample_parametric_results

        # 1. Elastic constants
        path1 = viz.plot_elastic_constants_comparison(
            df=df,
            param_columns=['sphere.radius', 'beam.thickness']
        )
        assert path1.exists()
        assert path1.suffix == '.png'

        # 2. Poisson vs Zener
        path2 = viz.plot_poisson_vs_zener(df=df, color_by='sphere.radius')
        assert path2.exists()

        # 3. Heatmap
        path3 = viz.plot_parameter_heatmap(
            df=df,
            param1='sphere.radius',
            param2='beam.thickness',
            value_col='C11'
        )
        assert path3.exists()

        # 4. Summary
        path4 = viz.generate_summary_report(
            df=df,
            param_columns=['sphere.radius', 'beam.thickness'],
            run_id='test_integration'
        )
        assert path4.exists()

        # Verify all files in temp dir
        output_files = list(temp_output_dir.glob('*.png'))
        assert len(output_files) == 4

    def test_prod_config_workflow(self, temp_output_dir, sample_parametric_results):
        """Test complete workflow with prod config."""
        # Load prod config
        config_path = get_config_path_for_env('visualization', env='prod')
        config = load_config(config_path)

        # Override output directory to use temp dir
        config['visualization']['output_dir'] = str(temp_output_dir)

        # Create visualizer
        viz = create_visualizer_from_config(config)

        assert viz.output_dir == temp_output_dir
        assert viz.dpi == 600
        assert viz.fig_format == 'pdf'

        # Generate one plot to verify
        df = sample_parametric_results
        path = viz.plot_poisson_vs_zener(df=df)

        assert path.exists()
        assert path.suffix == '.pdf'

    def test_csv_workflow(self, temp_output_dir, sample_parametric_results):
        """Test workflow from CSV file to plots."""
        # Save sample data to CSV
        csv_path = temp_output_dir / 'results.csv'
        sample_parametric_results.to_csv(csv_path, index=False)

        # Load config and override output dir
        config_path = get_config_path_for_env('visualization', env='dev')
        config = load_config(config_path)
        config['visualization']['output_dir'] = str(temp_output_dir / 'plots')

        # Create visualizer
        viz = create_visualizer_from_config(config)

        # Load CSV and generate plots
        df = pd.read_csv(csv_path)

        assert len(df) == 6
        assert 'sphere.radius' in df.columns

        # Generate summary report
        path = viz.generate_summary_report(
            df=df,
            param_columns=['sphere.radius', 'beam.thickness'],
            run_id='csv_test'
        )

        assert path.exists()
        assert 'csv_test' in path.name

    def test_auto_detect_parameters(self, temp_output_dir, sample_parametric_results):
        """Test auto-detection of parameter columns."""
        # Load config and override output dir
        config_path = get_config_path_for_env('visualization', env='dev')
        config = load_config(config_path)
        config['visualization']['output_dir'] = str(temp_output_dir)

        viz = create_visualizer_from_config(config)
        df = sample_parametric_results

        # Auto-detect parameter columns (columns with dots)
        param_cols = [col for col in df.columns if '.' in col]

        assert 'sphere.radius' in param_cols
        assert 'beam.thickness' in param_cols

        # Generate plot with auto-detected params
        path = viz.plot_elastic_constants_comparison(
            df=df,
            param_columns=param_cols
        )

        assert path.exists()

    def test_auto_detect_elastic_constants(self, temp_output_dir):
        """Test auto-detection of elastic constant columns."""
        # Create data with various column types
        df = pd.DataFrame({
            'param1': [1, 2, 3],
            'C11': [100, 110, 120],
            'C12': [40, 45, 50],
            'C44': [30, 35, 40],
            'other_value': [1.5, 2.0, 2.5],
        })

        # Load config and override output dir
        config_path = get_config_path_for_env('visualization', env='dev')
        config = load_config(config_path)
        config['visualization']['output_dir'] = str(temp_output_dir)

        viz = create_visualizer_from_config(config)

        # Should auto-detect C11, C12, C44
        path = viz.plot_elastic_constants_comparison(
            df=df,
            param_columns=['param1']
        )

        assert path.exists()
