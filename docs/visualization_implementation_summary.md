# パラメトリックスタディ可視化機能 - 実装サマリー

## 実装完了 ✓

カスタム格子のパラメトリックスタディ結果を可視化する機能を実装しました。

## 実装内容

### 1. コアモジュール

**`src/visualization/parametric_study_visualizer.py`**
- `ParametricStudyVisualizer` クラス
  - 弾性定数の比較プロット
  - Poisson比 vs Zener比 散布図
  - パラメータヒートマップ（2パラメータ）
  - サマリーレポート生成
- `create_visualizer_from_config()` ヘルパー関数

### 2. 設定ファイル

**開発環境: `configs/dev/visualization.yml`**
```yaml
visualization:
  output_dir: "results/visualizations/dev"
  dpi: 300
  format: "png"
```

**本番環境: `configs/prod/visualization.yml`**
```yaml
visualization:
  output_dir: "results/visualizations/prod"
  dpi: 600
  format: "pdf"  # 高品質出力
```

### 3. CLIスクリプト

**`scripts/visualize_parametric_study.py`**
- CSVファイルから結果を読み込み
- 複数の可視化を自動生成
- 環境別設定のサポート
- パラメータの自動検出

### 4. テスト

**`tests/unit/test_parametric_study_visualizer.py`**
- 16個のユニットテスト
- 全テスト合格 ✓
- エッジケースのカバー

### 5. ドキュメント

**`docs/visualization_guide.md`**
- 使用方法の詳細説明
- サンプルコード
- トラブルシューティング

## 主な機能

### 1. 弾性定数の比較プロット

パラメータの変化に対する弾性定数（C11, C12, C44など）の変化を可視化。

```python
viz.plot_elastic_constants_comparison(
    df=df,
    param_columns=['sphere.radius', 'beam.thickness']
)
```

### 2. Poisson比 vs Zener比プロット

材料の等方性・異方性を評価：
- **Zener比 (A)**: A = 2*C44/(C11-C12)
  - A = 1: 等方性材料
  - A ≠ 1: 異方性材料

```python
viz.plot_poisson_vs_zener(
    df=df,
    color_by='sphere.radius'  # パラメータで色分け
)
```

### 3. パラメータヒートマップ

2パラメータに対する特性値のヒートマップ：

```python
viz.plot_parameter_heatmap(
    df=df,
    param1='sphere.radius',
    param2='beam.thickness',
    value_col='C11'
)
```

### 4. サマリーレポート

複数のプロットを1つの図にまとめた包括的なレポート：

```python
viz.generate_summary_report(
    df=df,
    param_columns=['sphere.radius', 'beam.thickness'],
    run_id='study_001'
)
```

## 使用方法

### CLI経由

```bash
# 開発環境（PNG、300dpi）
python scripts/visualize_parametric_study.py \
    -i results/study_001/results.csv \
    -r study_001

# 本番環境（PDF、600dpi）
python scripts/visualize_parametric_study.py \
    -i results/study_001/results.csv \
    -r study_001 \
    --env prod
```

### Python経由

```python
from src.config.loader import load_config, get_config_path_for_env
from src.visualization import create_visualizer_from_config
import pandas as pd

# 設定読み込み
config = load_config(get_config_path_for_env('visualization'))
viz = create_visualizer_from_config(config)

# データ読み込み
df = pd.read_csv('results.csv')

# 可視化
viz.plot_elastic_constants_comparison(
    df=df,
    param_columns=['sphere.radius', 'beam.thickness']
)
```

## 入力データフォーマット

CSVファイルの例：

```csv
sphere.radius,beam.thickness,C11,C12,C44,poisson_ratio,zener_ratio
0.15,0.08,100,40,30,0.25,0.95
0.15,0.10,110,45,32,0.27,1.00
0.20,0.08,120,50,35,0.28,1.05
0.20,0.10,130,55,37,0.30,1.10
0.25,0.08,140,60,40,0.31,1.15
0.25,0.10,150,65,42,0.33,1.20
```

### 必須列

- パラメータ列（例: `sphere.radius`, `beam.thickness`）
- 弾性定数列（例: `C11`, `C12`, `C44`）

### オプション列

- `poisson_ratio`: Poisson比
- `zener_ratio`: Zener異方性比

## テスト結果

```
============================= test session starts ==============================
collected 16 items

tests/unit/test_parametric_study_visualizer.py ................              [100%]

============================== 16 passed in 12.19s ==============================
```

## 統合テスト結果

```
Visualizer created successfully
  Output dir: results/visualizations/dev
  DPI: 300
  Format: png

Generating test plots...
  ✓ Elastic constants: results/visualizations/dev/test_elastic_constants.png
  ✓ Poisson vs Zener: results/visualizations/dev/test_poisson_vs_zener.png
  ✓ Heatmap: results/visualizations/dev/test_heatmap.png
  ✓ Summary report: results/visualizations/dev/test_summary_report.png

All plots generated successfully!
```

## ファイル構成

```
src/visualization/
├── __init__.py
└── parametric_study_visualizer.py

configs/
├── dev/
│   └── visualization.yml
└── prod/
    └── visualization.yml

scripts/
└── visualize_parametric_study.py

tests/unit/
└── test_parametric_study_visualizer.py

docs/
├── visualization_guide.md
└── visualization_implementation_summary.md

results/visualizations/
├── dev/    # 開発環境の出力
└── prod/   # 本番環境の出力
```

## 設定システムとの統合

既存の `src/config/loader.py` を利用：

```python
from src.config.loader import (
    get_config_path_for_env,
    load_config,
    setup_logging,
)

# 環境別設定の自動読み込み
config_path = get_config_path_for_env('visualization', env='dev')
config = load_config(config_path)

# ロギングのセットアップ
logger = setup_logging(config)
```

## 次のステップ

現在の実装では、可視化のための内部ロジックが整備されています。
実際のCOMSOL結果データが得られた後：

1. 結果パーサーの実装（`src/parsers/comsol_result_parser.py`）
2. 弾性定数の計算ロジック
3. Poisson比とZener比の計算
4. CSV形式での結果保存
5. 可視化パイプラインへの統合

## 依存関係

- `matplotlib`: プロット生成
- `seaborn`: 統計的可視化
- `pandas`: データ処理
- `numpy`: 数値計算
- `pyyaml`: 設定ファイル読み込み

全ての依存関係は既に `docker/requirements.txt` に含まれています。

## まとめ

✅ コアクラスの実装完了
✅ 設定ファイルの整備完了
✅ CLIスクリプトの実装完了
✅ 16個のユニットテストが全て合格
✅ 統合テストで動作確認済み
✅ ドキュメント整備完了

可視化機能の内部ロジックが完成し、COMSOL結果データが得られ次第、
すぐに利用できる状態になっています。
