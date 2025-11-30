#!/usr/bin/env python
"""Visualize parametric study results from custom lattice simulations.

This script loads parametric study results and generates visualizations including:
- Elastic constants comparison across parameter combinations
- Poisson ratio vs Zener ratio scatter plots
- Parameter heatmaps
- Summary reports

Usage:
    python scripts/visualize_parametric_study.py -i results.csv -r run_001
    python scripts/visualize_parametric_study.py -i results.csv -r run_001 --env prod
"""

import argparse
import sys
from pathlib import Path
import pandas as pd

from src.config.loader import (
    get_config_path_for_env,
    load_config,
    setup_logging,
    get_logger,
)
from src.visualization import create_visualizer_from_config


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Visualize parametric study results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage (development environment)
  python scripts/visualize_parametric_study.py -i results/study_001/results.csv -r study_001

  # Production environment (higher quality outputs)
  python scripts/visualize_parametric_study.py -i results/study_001/results.csv -r study_001 --env prod

  # Specify parameter columns explicitly
  python scripts/visualize_parametric_study.py -i results.csv -r test --params sphere.radius beam.thickness

  # Generate only specific plots
  python scripts/visualize_parametric_study.py -i results.csv -r test --plots elastic poisson
        """
    )

    parser.add_argument(
        '-i', '--input',
        type=str,
        required=True,
        help='Path to results CSV file'
    )

    parser.add_argument(
        '-r', '--run-id',
        type=str,
        required=True,
        help='Run ID for organizing outputs'
    )

    parser.add_argument(
        '--env',
        type=str,
        default='dev',
        choices=['dev', 'prod', 'development', 'production'],
        help='Environment (dev/prod, default: dev)'
    )

    parser.add_argument(
        '--params',
        type=str,
        nargs='+',
        default=None,
        help='Parameter column names (auto-detected if not specified)'
    )

    parser.add_argument(
        '--plots',
        type=str,
        nargs='+',
        default=['elastic', 'poisson', 'heatmap', 'summary'],
        choices=['elastic', 'poisson', 'heatmap', 'summary'],
        help='Which plots to generate (default: all)'
    )

    parser.add_argument(
        '--color-by',
        type=str,
        default=None,
        help='Parameter to color Poisson vs Zener plot by'
    )

    args = parser.parse_args()

    # Load configuration
    config_path = get_config_path_for_env('visualization', env=args.env)
    config = load_config(config_path)

    # Setup logging
    logger = setup_logging(config)
    logger.info("=" * 70)
    logger.info("Parametric Study Visualization")
    logger.info("=" * 70)
    logger.info(f"Environment: {args.env}")
    logger.info(f"Configuration: {config_path}")
    logger.info(f"Input file: {args.input}")
    logger.info(f"Run ID: {args.run_id}")

    # Load results
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"✗ Input file not found: {input_path}")
        return 1

    logger.info("Loading results...")
    try:
        df = pd.read_csv(input_path)
        logger.info(f"✓ Loaded {len(df)} rows from {input_path}")
        logger.info(f"  Columns: {', '.join(df.columns)}")
    except Exception as e:
        logger.error(f"✗ Failed to load CSV: {e}")
        return 1

    # Auto-detect parameter columns if not specified
    if args.params is None:
        # Look for columns with dots (e.g., sphere.radius, beam.thickness)
        param_cols = [col for col in df.columns if '.' in col]
        if not param_cols:
            logger.warning("No parameter columns auto-detected (looking for '.' in name)")
            logger.warning("Please specify parameter columns with --params")
            return 1
        logger.info(f"Auto-detected parameter columns: {', '.join(param_cols)}")
    else:
        param_cols = args.params
        # Validate parameter columns exist
        missing = [col for col in param_cols if col not in df.columns]
        if missing:
            logger.error(f"✗ Parameter columns not found in data: {', '.join(missing)}")
            return 1

    # Create visualizer
    logger.info("Initializing visualizer...")
    viz = create_visualizer_from_config(config)
    logger.info(f"  Output directory: {viz.output_dir}")
    logger.info(f"  Format: {viz.fig_format}, DPI: {viz.dpi}")

    # Generate plots
    logger.info("=" * 70)
    logger.info("Generating visualizations...")
    logger.info("=" * 70)

    generated_files = []

    try:
        # 1. Elastic constants comparison
        if 'elastic' in args.plots:
            logger.info("Generating elastic constants comparison plot...")
            output_path = viz.plot_elastic_constants_comparison(
                df=df,
                param_columns=param_cols,
                filename=f'elastic_constants_{args.run_id}'
            )
            generated_files.append(output_path)
            logger.info(f"  ✓ Saved to {output_path}")

        # 2. Poisson vs Zener ratio
        if 'poisson' in args.plots:
            if 'poisson_ratio' in df.columns and 'zener_ratio' in df.columns:
                logger.info("Generating Poisson vs Zener plot...")
                output_path = viz.plot_poisson_vs_zener(
                    df=df,
                    color_by=args.color_by,
                    filename=f'poisson_vs_zener_{args.run_id}'
                )
                generated_files.append(output_path)
                logger.info(f"  ✓ Saved to {output_path}")
            else:
                logger.warning("  ⊗ Skipping Poisson vs Zener plot (columns not found)")

        # 3. Heatmaps (for 2-parameter studies)
        if 'heatmap' in args.plots and len(param_cols) >= 2:
            logger.info("Generating parameter heatmaps...")
            # Generate heatmap for each elastic constant
            elastic_cols = [
                col for col in df.columns
                if col.startswith(('C', 'c')) and col[1:].replace('.', '').isdigit()
            ]

            if elastic_cols:
                for elastic_col in elastic_cols[:3]:  # Limit to first 3
                    try:
                        output_path = viz.plot_parameter_heatmap(
                            df=df,
                            param1=param_cols[0],
                            param2=param_cols[1],
                            value_col=elastic_col,
                            filename=f'heatmap_{elastic_col}_{args.run_id}'
                        )
                        generated_files.append(output_path)
                        logger.info(f"  ✓ Saved {elastic_col} heatmap to {output_path}")
                    except Exception as e:
                        logger.warning(f"  ⊗ Could not generate heatmap for {elastic_col}: {e}")
            else:
                logger.warning("  ⊗ No elastic constants found for heatmap")
        elif 'heatmap' in args.plots:
            logger.warning("  ⊗ Skipping heatmaps (requires 2+ parameters)")

        # 4. Summary report
        if 'summary' in args.plots:
            logger.info("Generating summary report...")
            output_path = viz.generate_summary_report(
                df=df,
                param_columns=param_cols,
                run_id=args.run_id
            )
            generated_files.append(output_path)
            logger.info(f"  ✓ Saved to {output_path}")

    except Exception as e:
        logger.error(f"✗ Error during visualization: {e}", exc_info=True)
        return 1

    # Summary
    logger.info("=" * 70)
    logger.info("Visualization Complete")
    logger.info("=" * 70)
    logger.info(f"Generated {len(generated_files)} plots:")
    for path in generated_files:
        logger.info(f"  - {path}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
