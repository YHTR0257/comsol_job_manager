"""Visualization utilities for parametric study results.

This module provides visualization capabilities for analyzing COMSOL simulation
results from parametric studies of custom lattice structures.

Key Features:
- Elastic constants comparison across parameter combinations
- Poisson ratio vs Zener ratio scatter plots
- Support for multiple parametric sweeps
- Configurable output paths and formats
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


logger = logging.getLogger(__name__)


class ParametricStudyVisualizer:
    """Visualize results from parametric studies of lattice structures.

    This class handles visualization of mechanical properties derived from
    COMSOL simulations, focusing on elastic constants and their relationships.

    Attributes:
        output_dir: Directory where plots will be saved
        dpi: Resolution for saved figures
        fig_format: File format for saved figures (png, pdf, svg)
        style: Matplotlib style to use
    """

    def __init__(
        self,
        output_dir: Path,
        dpi: int = 300,
        fig_format: str = 'png',
        style: str = 'seaborn-v0_8-darkgrid'
    ):
        """Initialize the visualizer.

        Args:
            output_dir: Directory to save visualization outputs
            dpi: Resolution for saved figures
            fig_format: File format (png, pdf, svg)
            style: Matplotlib style name
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.dpi = dpi
        self.fig_format = fig_format
        self.style = style

        # Set style
        try:
            plt.style.use(style)
        except Exception as e:
            logger.warning(f"Could not set style '{style}': {e}")
            plt.style.use('default')

    def plot_elastic_constants_comparison(
        self,
        df: pd.DataFrame,
        param_columns: List[str],
        elastic_columns: Optional[List[str]] = None,
        filename: Optional[str] = None
    ) -> Path:
        """Plot elastic constants vs parametric sweep parameters.

        Creates a multi-panel plot showing how each elastic constant varies
        with the swept parameters. Useful for understanding parameter
        sensitivity and optimization.

        Args:
            df: DataFrame with columns for parameters and elastic constants
            param_columns: List of parameter column names to plot on x-axis
            elastic_columns: List of elastic constant columns to plot.
                If None, uses all columns starting with 'C' or 'c'
            filename: Output filename (without extension). If None, auto-generated

        Returns:
            Path to saved figure

        Example:
            >>> df = pd.DataFrame({
            ...     'sphere.radius': [0.15, 0.20, 0.25],
            ...     'beam.thickness': [0.08, 0.10, 0.12],
            ...     'C11': [100, 120, 140],
            ...     'C12': [40, 50, 60],
            ...     'C44': [30, 35, 40]
            ... })
            >>> viz.plot_elastic_constants_comparison(
            ...     df,
            ...     param_columns=['sphere.radius', 'beam.thickness']
            ... )
        """
        if elastic_columns is None:
            # Auto-detect elastic constant columns (C11, C12, C44, etc.)
            elastic_columns = [
                col for col in df.columns
                if col.startswith(('C', 'c')) and col[1:].replace('.', '').isdigit()
            ]

        if not elastic_columns:
            raise ValueError("No elastic constant columns found in DataFrame")

        n_params = len(param_columns)
        n_elastic = len(elastic_columns)

        # Create figure with subplots
        fig, axes = plt.subplots(
            n_elastic, n_params,
            figsize=(5 * n_params, 4 * n_elastic),
            squeeze=False
        )

        for i, elastic_col in enumerate(elastic_columns):
            for j, param_col in enumerate(param_columns):
                ax = axes[i, j]

                # Scatter plot with connecting lines if data is sorted
                ax.plot(
                    df[param_col],
                    df[elastic_col],
                    marker='o',
                    linestyle='-',
                    linewidth=2,
                    markersize=8,
                    alpha=0.7
                )

                ax.set_xlabel(param_col, fontsize=12)
                ax.set_ylabel(f'{elastic_col} (GPa)', fontsize=12)
                ax.grid(True, alpha=0.3)

                # Add title to top row
                if i == 0:
                    ax.set_title(f'{param_col} vs Elastic Constants', fontsize=14)

        plt.tight_layout()

        # Generate filename
        if filename is None:
            filename = 'elastic_constants_comparison'

        output_path = self.output_dir / f'{filename}.{self.fig_format}'
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()

        logger.info(f"Saved elastic constants comparison plot to {output_path}")
        return output_path

    def plot_poisson_vs_zener(
        self,
        df: pd.DataFrame,
        poisson_col: str = 'poisson_ratio',
        zener_col: str = 'zener_ratio',
        color_by: Optional[str] = None,
        filename: Optional[str] = None
    ) -> Path:
        """Plot Poisson ratio vs Zener anisotropy ratio.

        Creates a scatter plot showing the relationship between Poisson's ratio
        (measure of lateral strain) and Zener ratio (measure of elastic anisotropy).

        The Zener ratio A = 2*C44/(C11-C12) indicates elastic anisotropy:
        - A = 1: Isotropic material
        - A ≠ 1: Anisotropic material

        Args:
            df: DataFrame containing Poisson ratio and Zener ratio
            poisson_col: Column name for Poisson ratio
            zener_col: Column name for Zener ratio
            color_by: Optional column name to color points by (e.g., parameter value)
            filename: Output filename (without extension). If None, auto-generated

        Returns:
            Path to saved figure

        Example:
            >>> df = pd.DataFrame({
            ...     'poisson_ratio': [0.25, 0.28, 0.32],
            ...     'zener_ratio': [0.95, 1.05, 1.15],
            ...     'sphere.radius': [0.15, 0.20, 0.25]
            ... })
            >>> viz.plot_poisson_vs_zener(
            ...     df,
            ...     color_by='sphere.radius'
            ... )
        """
        fig, ax = plt.subplots(figsize=(10, 8))

        if color_by is not None and color_by in df.columns:
            # Color by parameter value
            scatter = ax.scatter(
                df[poisson_col],
                df[zener_col],
                c=df[color_by],
                s=100,
                alpha=0.7,
                cmap='viridis',
                edgecolors='black',
                linewidth=1.5
            )

            # Add colorbar
            cbar = plt.colorbar(scatter, ax=ax)
            cbar.set_label(color_by, fontsize=12)
        else:
            # Simple scatter plot
            ax.scatter(
                df[poisson_col],
                df[zener_col],
                s=100,
                alpha=0.7,
                color='steelblue',
                edgecolors='black',
                linewidth=1.5
            )

        # Add reference line for isotropic material (Zener = 1)
        ax.axhline(y=1.0, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Isotropic (A=1)')

        # Labels and title
        ax.set_xlabel('Poisson Ratio (ν)', fontsize=14)
        ax.set_ylabel('Zener Ratio (A = 2C₄₄/(C₁₁-C₁₂))', fontsize=14)
        ax.set_title('Poisson Ratio vs Zener Anisotropy Ratio', fontsize=16, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=12)

        plt.tight_layout()

        # Generate filename
        if filename is None:
            filename = 'poisson_vs_zener'

        output_path = self.output_dir / f'{filename}.{self.fig_format}'
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()

        logger.info(f"Saved Poisson vs Zener plot to {output_path}")
        return output_path

    def plot_parameter_heatmap(
        self,
        df: pd.DataFrame,
        param1: str,
        param2: str,
        value_col: str,
        filename: Optional[str] = None
    ) -> Path:
        """Plot heatmap of a property vs two swept parameters.

        Creates a 2D heatmap showing how a property (e.g., elastic constant,
        Poisson ratio) varies with two parameters. Useful for identifying
        optimal parameter combinations.

        Args:
            df: DataFrame with parameter and value columns
            param1: First parameter column name (x-axis)
            param2: Second parameter column name (y-axis)
            value_col: Column to visualize as heatmap colors
            filename: Output filename (without extension). If None, auto-generated

        Returns:
            Path to saved figure

        Example:
            >>> df = pd.DataFrame({
            ...     'sphere.radius': [0.15, 0.15, 0.20, 0.20],
            ...     'beam.thickness': [0.08, 0.10, 0.08, 0.10],
            ...     'C11': [100, 110, 120, 130]
            ... })
            >>> viz.plot_parameter_heatmap(
            ...     df,
            ...     'sphere.radius',
            ...     'beam.thickness',
            ...     'C11'
            ... )
        """
        # Pivot data for heatmap
        pivot_data = df.pivot(index=param2, columns=param1, values=value_col)

        fig, ax = plt.subplots(figsize=(10, 8))

        sns.heatmap(
            pivot_data,
            annot=True,
            fmt='.2f',
            cmap='YlOrRd',
            ax=ax,
            cbar_kws={'label': value_col}
        )

        ax.set_xlabel(param1, fontsize=14)
        ax.set_ylabel(param2, fontsize=14)
        ax.set_title(f'{value_col} vs {param1} and {param2}', fontsize=16, fontweight='bold')

        plt.tight_layout()

        # Generate filename
        if filename is None:
            filename = f'heatmap_{value_col}_{param1}_{param2}'.replace('.', '_')

        output_path = self.output_dir / f'{filename}.{self.fig_format}'
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()

        logger.info(f"Saved parameter heatmap to {output_path}")
        return output_path

    def generate_summary_report(
        self,
        df: pd.DataFrame,
        param_columns: List[str],
        run_id: str,
        filename: Optional[str] = None
    ) -> Path:
        """Generate a comprehensive visualization summary report.

        Creates multiple plots in a single multi-panel figure showing:
        1. Elastic constants comparison
        2. Poisson vs Zener ratio
        3. Parameter distributions

        Args:
            df: DataFrame with all results
            param_columns: List of parameter column names
            run_id: Run identifier for the report
            filename: Output filename (without extension). If None, auto-generated

        Returns:
            Path to saved figure
        """
        # Auto-detect elastic constants
        elastic_columns = [
            col for col in df.columns
            if col.startswith(('C', 'c')) and col[1:].replace('.', '').isdigit()
        ]

        # Create figure with multiple subplots
        n_plots = 2 + len(param_columns)
        fig = plt.figure(figsize=(15, 5 * ((n_plots + 1) // 2)))

        # 1. Elastic constants bar chart
        ax1 = plt.subplot(2, 2, 1)
        if elastic_columns:
            df[elastic_columns].mean().plot(kind='bar', ax=ax1, color='steelblue')
            ax1.set_title('Average Elastic Constants', fontsize=14, fontweight='bold')
            ax1.set_ylabel('Value (GPa)', fontsize=12)
            ax1.grid(True, alpha=0.3, axis='y')

        # 2. Poisson vs Zener (if available)
        ax2 = plt.subplot(2, 2, 2)
        if 'poisson_ratio' in df.columns and 'zener_ratio' in df.columns:
            ax2.scatter(
                df['poisson_ratio'],
                df['zener_ratio'],
                s=100,
                alpha=0.7,
                color='coral',
                edgecolors='black'
            )
            ax2.axhline(y=1.0, color='red', linestyle='--', alpha=0.5)
            ax2.set_xlabel('Poisson Ratio', fontsize=12)
            ax2.set_ylabel('Zener Ratio', fontsize=12)
            ax2.set_title('Poisson vs Zener Ratio', fontsize=14, fontweight='bold')
            ax2.grid(True, alpha=0.3)

        # 3-N. Parameter distributions
        for i, param in enumerate(param_columns[:2]):  # Limit to 2 params for layout
            ax = plt.subplot(2, 2, 3 + i)
            df[param].hist(bins=20, ax=ax, color='lightgreen', edgecolor='black')
            ax.set_xlabel(param, fontsize=12)
            ax.set_ylabel('Frequency', fontsize=12)
            ax.set_title(f'{param} Distribution', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')

        plt.suptitle(f'Parametric Study Summary: {run_id}', fontsize=18, fontweight='bold')
        plt.tight_layout()

        # Generate filename
        if filename is None:
            filename = f'summary_report_{run_id}'

        output_path = self.output_dir / f'{filename}.{self.fig_format}'
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()

        logger.info(f"Saved summary report to {output_path}")
        return output_path


def create_visualizer_from_config(config: Dict) -> ParametricStudyVisualizer:
    """Create a visualizer instance from configuration dictionary.

    Args:
        config: Configuration dictionary with 'visualization' key containing:
            - output_dir: Path to output directory
            - dpi: Figure DPI (optional, default 300)
            - format: Figure format (optional, default 'png')
            - style: Matplotlib style (optional, default 'seaborn-v0_8-darkgrid')

    Returns:
        Configured ParametricStudyVisualizer instance

    Example:
        >>> from src.config.loader import load_config, get_config_path_for_env
        >>> config_path = get_config_path_for_env('visualization')
        >>> config = load_config(config_path)
        >>> viz = create_visualizer_from_config(config)
    """
    viz_config = config.get('visualization', config)

    return ParametricStudyVisualizer(
        output_dir=Path(viz_config['output_dir']),
        dpi=viz_config.get('dpi', 300),
        fig_format=viz_config.get('format', 'png'),
        style=viz_config.get('style', 'seaborn-v0_8-darkgrid')
    )
