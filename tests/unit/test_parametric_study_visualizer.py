"""Unit tests for parametric study visualizer."""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import shutil

from src.visualization.parametric_study_visualizer import (
    ParametricStudyVisualizer,
    create_visualizer_from_config,
)


@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for test outputs."""
    tmpdir = Path(tempfile.mkdtemp())
    yield tmpdir
    # Cleanup
    shutil.rmtree(tmpdir)


@pytest.fixture
def sample_results_df():
    """Create sample parametric study results DataFrame."""
    np.random.seed(42)
    data = {
        'sphere.radius': [0.15, 0.15, 0.20, 0.20, 0.25, 0.25],
        'beam.thickness': [0.08, 0.10, 0.08, 0.10, 0.08, 0.10],
        'C11': [100, 110, 120, 130, 140, 150],
        'C12': [40, 45, 50, 55, 60, 65],
        'C44': [30, 32, 35, 37, 40, 42],
        'poisson_ratio': [0.25, 0.27, 0.28, 0.30, 0.31, 0.33],
        'zener_ratio': [0.95, 1.00, 1.05, 1.10, 1.15, 1.20],
    }
    return pd.DataFrame(data)


class TestParametricStudyVisualizer:
    """Test ParametricStudyVisualizer class."""

    def test_initialization(self, temp_output_dir):
        """Test visualizer initialization."""
        viz = ParametricStudyVisualizer(
            output_dir=temp_output_dir,
            dpi=300,
            fig_format='png',
            style='default'
        )

        assert viz.output_dir == temp_output_dir
        assert viz.dpi == 300
        assert viz.fig_format == 'png'
        assert temp_output_dir.exists()

    def test_plot_elastic_constants_comparison(self, temp_output_dir, sample_results_df):
        """Test elastic constants comparison plot."""
        viz = ParametricStudyVisualizer(output_dir=temp_output_dir)

        output_path = viz.plot_elastic_constants_comparison(
            df=sample_results_df,
            param_columns=['sphere.radius', 'beam.thickness']
        )

        assert output_path.exists()
        assert output_path.suffix == '.png'
        assert 'elastic_constants_comparison' in output_path.name

    def test_plot_elastic_constants_with_custom_columns(self, temp_output_dir, sample_results_df):
        """Test elastic constants plot with custom column selection."""
        viz = ParametricStudyVisualizer(output_dir=temp_output_dir)

        output_path = viz.plot_elastic_constants_comparison(
            df=sample_results_df,
            param_columns=['sphere.radius'],
            elastic_columns=['C11', 'C12']
        )

        assert output_path.exists()

    def test_plot_poisson_vs_zener(self, temp_output_dir, sample_results_df):
        """Test Poisson vs Zener ratio plot."""
        viz = ParametricStudyVisualizer(output_dir=temp_output_dir)

        output_path = viz.plot_poisson_vs_zener(
            df=sample_results_df
        )

        assert output_path.exists()
        assert output_path.suffix == '.png'
        assert 'poisson_vs_zener' in output_path.name

    def test_plot_poisson_vs_zener_with_color(self, temp_output_dir, sample_results_df):
        """Test Poisson vs Zener plot with color coding."""
        viz = ParametricStudyVisualizer(output_dir=temp_output_dir)

        output_path = viz.plot_poisson_vs_zener(
            df=sample_results_df,
            color_by='sphere.radius'
        )

        assert output_path.exists()

    def test_plot_parameter_heatmap(self, temp_output_dir, sample_results_df):
        """Test parameter heatmap plot."""
        viz = ParametricStudyVisualizer(output_dir=temp_output_dir)

        output_path = viz.plot_parameter_heatmap(
            df=sample_results_df,
            param1='sphere.radius',
            param2='beam.thickness',
            value_col='C11'
        )

        assert output_path.exists()
        assert output_path.suffix == '.png'
        assert 'heatmap' in output_path.name

    def test_generate_summary_report(self, temp_output_dir, sample_results_df):
        """Test summary report generation."""
        viz = ParametricStudyVisualizer(output_dir=temp_output_dir)

        output_path = viz.generate_summary_report(
            df=sample_results_df,
            param_columns=['sphere.radius', 'beam.thickness'],
            run_id='test_run_001'
        )

        assert output_path.exists()
        assert output_path.suffix == '.png'
        assert 'summary_report' in output_path.name
        assert 'test_run_001' in output_path.name

    def test_custom_filename(self, temp_output_dir, sample_results_df):
        """Test custom filename specification."""
        viz = ParametricStudyVisualizer(output_dir=temp_output_dir)

        output_path = viz.plot_poisson_vs_zener(
            df=sample_results_df,
            filename='my_custom_plot'
        )

        assert output_path.exists()
        assert output_path.name == 'my_custom_plot.png'

    def test_pdf_format(self, temp_output_dir, sample_results_df):
        """Test PDF format output."""
        viz = ParametricStudyVisualizer(
            output_dir=temp_output_dir,
            fig_format='pdf'
        )

        output_path = viz.plot_poisson_vs_zener(df=sample_results_df)

        assert output_path.exists()
        assert output_path.suffix == '.pdf'

    def test_auto_detect_elastic_constants(self, temp_output_dir):
        """Test auto-detection of elastic constant columns."""
        df = pd.DataFrame({
            'param1': [1, 2, 3],
            'C11': [100, 110, 120],
            'C12': [40, 45, 50],
            'C44': [30, 35, 40],
            'other_col': [1, 2, 3]
        })

        viz = ParametricStudyVisualizer(output_dir=temp_output_dir)

        output_path = viz.plot_elastic_constants_comparison(
            df=df,
            param_columns=['param1']
        )

        assert output_path.exists()


class TestCreateVisualizerFromConfig:
    """Test configuration-based visualizer creation."""

    def test_create_from_dict_config(self, temp_output_dir):
        """Test creating visualizer from dictionary config."""
        config = {
            'visualization': {
                'output_dir': str(temp_output_dir),
                'dpi': 600,
                'format': 'pdf',
                'style': 'default'
            }
        }

        viz = create_visualizer_from_config(config)

        assert viz.output_dir == temp_output_dir
        assert viz.dpi == 600
        assert viz.fig_format == 'pdf'

    def test_create_from_flat_config(self, temp_output_dir):
        """Test creating visualizer from flat config (no 'visualization' key)."""
        config = {
            'output_dir': str(temp_output_dir),
            'dpi': 300,
            'format': 'png'
        }

        viz = create_visualizer_from_config(config)

        assert viz.output_dir == temp_output_dir
        assert viz.dpi == 300

    def test_create_with_defaults(self, temp_output_dir):
        """Test creating visualizer with default values."""
        config = {
            'visualization': {
                'output_dir': str(temp_output_dir)
            }
        }

        viz = create_visualizer_from_config(config)

        assert viz.dpi == 300
        assert viz.fig_format == 'png'


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_dataframe(self, temp_output_dir):
        """Test handling of empty DataFrame."""
        viz = ParametricStudyVisualizer(output_dir=temp_output_dir)
        df = pd.DataFrame()

        with pytest.raises((ValueError, KeyError)):
            viz.plot_elastic_constants_comparison(
                df=df,
                param_columns=['param1']
            )

    def test_missing_columns(self, temp_output_dir, sample_results_df):
        """Test error when required columns are missing."""
        viz = ParametricStudyVisualizer(output_dir=temp_output_dir)

        with pytest.raises(KeyError):
            viz.plot_elastic_constants_comparison(
                df=sample_results_df,
                param_columns=['nonexistent_column']
            )

    def test_no_elastic_constants(self, temp_output_dir):
        """Test error when no elastic constants are found."""
        viz = ParametricStudyVisualizer(output_dir=temp_output_dir)
        df = pd.DataFrame({
            'param1': [1, 2, 3],
            'value': [10, 20, 30]
        })

        with pytest.raises(ValueError, match="No elastic constant columns found"):
            viz.plot_elastic_constants_comparison(
                df=df,
                param_columns=['param1']
            )
