# パラメトリックスタディ結果の可視化ガイド

## 概要

このガイドでは、カスタム格子のパラメトリックスタディ結果を可視化する方法を説明します。

## 主な機能

### 1. 弾性定数の比較プロット

パラメータの変化に対する弾性定数（C11, C12, C44など）の変化を可視化します。

### 2. Poisson比 vs Zener比プロット

- **Poisson比**: 横ひずみと縦ひずみの比率
- **Zener比**: 弾性異方性の指標 (A = 2*C44/(C11-C12))
  - A = 1: 等方性材料
  - A ≠ 1: 異方性材料

### 3. パラメータヒートマップ

2つのパラメータに対する任意の特性値のヒートマップを生成します。

### 4. サマリーレポート

複数のプロットを1つの図にまとめた包括的なレポートを生成します。

## 設定ファイル

### 開発環境 (`configs/dev/visualization.yml`)

```yaml
visualization:
  output_dir: "results/visualizations/dev"
  dpi: 300
  format: "png"
  style: "seaborn-v0_8-darkgrid"

logging:
  level: "DEBUG"
```

### 本番環境 (`configs/prod/visualization.yml`)

```yaml
visualization:
  output_dir: "results/visualizations/prod"
  dpi: 600
  format: "pdf"  # 高品質出力
  style: "seaborn-v0_8-darkgrid"

logging:
  level: "INFO"
```

## 使用方法

### CLIスクリプトを使用

```bash
# 基本的な使用方法（開発環境）
python scripts/visualize_parametric_study.py \
    -i results/study_001/results.csv \
    -r study_001

# 本番環境（高品質PDF出力）
python scripts/visualize_parametric_study.py \
    -i results/study_001/results.csv \
    -r study_001 \
    --env prod

# パラメータを明示的に指定
python scripts/visualize_parametric_study.py \
    -i results.csv \
    -r test \
    --params sphere.radius beam.thickness

# 特定のプロットのみ生成
python scripts/visualize_parametric_study.py \
    -i results.csv \
    -r test \
    --plots elastic poisson

# Poisson vs Zenerプロットに色付け
python scripts/visualize_parametric_study.py \
    -i results.csv \
    -r test \
    --color-by sphere.radius
```

### Pythonコードで使用

```python
from pathlib import Path
import pandas as pd
from src.config.loader import load_config, get_config_path_for_env
from src.visualization import create_visualizer_from_config

# 設定ファイルを読み込み
config_path = get_config_path_for_env('visualization')
config = load_config(config_path)

# Visualizerを作成
viz = create_visualizer_from_config(config)

# 結果データを読み込み
df = pd.read_csv('results/parametric_study/results.csv')

# 1. 弾性定数の比較
viz.plot_elastic_constants_comparison(
    df=df,
    param_columns=['sphere.radius', 'beam.thickness']
)

# 2. Poisson vs Zener比
viz.plot_poisson_vs_zener(
    df=df,
    color_by='sphere.radius'
)

# 3. ヒートマップ（2パラメータの場合）
viz.plot_parameter_heatmap(
    df=df,
    param1='sphere.radius',
    param2='beam.thickness',
    value_col='C11'
)

# 4. サマリーレポート
viz.generate_summary_report(
    df=df,
    param_columns=['sphere.radius', 'beam.thickness'],
    run_id='study_001'
)
```

## 入力データフォーマット

CSVファイルは以下の列を含む必要があります：

### 必須列

- パラメータ列（例: `sphere.radius`, `beam.thickness`）
- 弾性定数列（例: `C11`, `C12`, `C44`）

### オプション列

- `poisson_ratio`: Poisson比
- `zener_ratio`: Zener異方性比
- その他の機械的特性

### サンプルCSV

```csv
sphere.radius,beam.thickness,C11,C12,C44,poisson_ratio,zener_ratio
0.15,0.08,100,40,30,0.25,0.95
0.15,0.10,110,45,32,0.27,1.00
0.20,0.08,120,50,35,0.28,1.05
0.20,0.10,130,55,37,0.30,1.10
0.25,0.08,140,60,40,0.31,1.15
0.25,0.10,150,65,42,0.33,1.20
```

## 出力例

### ディレクトリ構造

```
results/visualizations/dev/
├── elastic_constants_study_001.png
├── poisson_vs_zener_study_001.png
├── heatmap_C11_study_001.png
├── heatmap_C12_study_001.png
├── heatmap_C44_study_001.png
└── summary_report_study_001.png
```

## カスタマイズ

### プロットスタイルの変更

設定ファイルの`style`パラメータを変更：

```yaml
visualization:
  style: "default"  # または "ggplot", "seaborn-v0_8-whitegrid" など
```

### 解像度とフォーマットの変更

```yaml
visualization:
  dpi: 600      # 高解像度
  format: "pdf" # ベクター形式
```

### カラーマップの変更

```yaml
visualization:
  heatmap:
    cmap: "viridis"  # または "plasma", "RdYlBu" など
```

## トラブルシューティング

### エラー: "No elastic constant columns found"

- CSVファイルに `C11`, `C12`, `C44` などの列が含まれているか確認
- または `elastic_columns` パラメータで明示的に指定

### エラー: "Configuration file not found"

- `configs/dev/visualization.yml` が存在するか確認
- または `--env` オプションで正しい環境を指定

### プロットが空白

- データフレームに十分なデータポイントがあるか確認
- パラメータ列名が正しいか確認

## 応用例

### 1. 最適パラメータの特定

```python
# C11が最大となるパラメータ組み合わせを特定
best_idx = df['C11'].idxmax()
best_params = df.loc[best_idx, ['sphere.radius', 'beam.thickness']]
print(f"Best parameters: {best_params}")

# プロット上にマーク
viz.plot_poisson_vs_zener(df=df, color_by='C11')
```

### 2. パラメータ感度分析

```python
# 各パラメータの変化に対するC11の感度を計算
for param in ['sphere.radius', 'beam.thickness']:
    sensitivity = df.groupby(param)['C11'].std()
    print(f"{param} sensitivity: {sensitivity}")
```

### 3. バッチ処理

```python
# 複数のrunを一度に処理
run_ids = ['run_001', 'run_002', 'run_003']

for run_id in run_ids:
    df = pd.read_csv(f'results/{run_id}/results.csv')
    viz.generate_summary_report(
        df=df,
        param_columns=['sphere.radius', 'beam.thickness'],
        run_id=run_id
    )
```

## 参考資料

- [カスタム格子機能設計書](feature/FU01_custom_lattice.md)
- [パラメトリックスタディ例](../examples/custom_lattice/parametric_study_example.yml)
- Matplotlib公式ドキュメント: https://matplotlib.org/
- Seaborn公式ドキュメント: https://seaborn.pydata.org/
