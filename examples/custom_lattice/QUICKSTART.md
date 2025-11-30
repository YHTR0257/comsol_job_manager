# クイックスタートガイド

## 1. 最初のカスタム格子ジョブを生成

最もシンプルな例から始めましょう：

```bash
# シンプルな立方格子ジョブを生成
python scripts/generate_custom_lattice_job.py \
    -i examples/custom_lattice/simple_cubic.yml \
    --run-id my_first_lattice
```

出力例：
```
======================================================================
Custom Lattice Job Generator
======================================================================

Loading custom lattice definition: examples/custom_lattice/simple_cubic.yml
✓ YAML loaded and validated successfully

Job Information:
  Name: Simple Cubic Lattice
  Description: Basic cubic lattice with 8 corner spheres and 12 edge beams
  Geometry: 8 spheres, 12 beams

Single job (no parametric sweeps)

Generating jobs...
✓ Successfully generated 1 jobs

Results:
  Run ID: my_first_lattice
  Run directory: jobs/comsol/my_first_lattice
  Jobs generated: 1
```

## 2. 生成されたファイルを確認

```bash
# ディレクトリ構造を確認
tree jobs/comsol/my_first_lattice/

# 出力:
# jobs/comsol/my_first_lattice/
# ├── metadata.yml          # Run全体のメタデータ
# └── job_001/
#     ├── job_001.java      # COMSOLシミュレーションファイル
#     ├── run.bat           # Windows実行スクリプト
#     └── metadata.yml      # ジョブのメタデータ
```

## 3. パラメトリックスタディを試す

複数のパラメータ組み合わせを自動生成：

```bash
# パラメトリックスタディの例を実行
python scripts/generate_custom_lattice_job.py \
    -i examples/custom_lattice/parametric_study_example.yml \
    --run-id parametric_test
```

出力：
```
Parametric Study:
  Number of sweeps: 2
  Total jobs to generate: 6
  Sweep 1: sphere.radius (3 values)
  Sweep 2: beam.thickness (2 values)

Generating jobs...
✓ Successfully generated 6 jobs
```

## 4. ジョブを実行（WSL環境のみ）

```bash
# 単一ジョブの実行
python scripts/execute_comsol_job.py -j jobs/comsol/my_first_lattice/job_001

# Run全体（全ジョブ）を実行
python scripts/execute_comsol_job.py -j jobs/comsol/my_first_lattice
```

## 5. 自分のカスタム格子を作成

既存のサンプルをコピーして編集：

```bash
# サンプルをコピー
cp examples/custom_lattice/simple_cubic.yml examples/custom_lattice/my_lattice.yml

# エディタで編集
vi examples/custom_lattice/my_lattice.yml

# ジョブ生成
python scripts/generate_custom_lattice_job.py \
    -i examples/custom_lattice/my_lattice.yml
```

## よくある使い方

### ケース1: 単一パラメータの最適化

```yaml
parametric:
  default:
    sphere.radius: 0.2
  sweep1:
    parameter: "sphere.radius"
    values: [0.1, 0.15, 0.2, 0.25, 0.3]
```

### ケース2: 2パラメータの最適化

```yaml
parametric:
  default:
    sphere.radius: 0.2
    beam.thickness: 0.1
  sweep1:
    parameter: "sphere.radius"
    values: [0.15, 0.2, 0.25]
  sweep2:
    parameter: "beam.thickness"
    values: [0.08, 0.1, 0.12]
# → 3 × 3 = 9ジョブ
```

### ケース3: 3パラメータ以上の最適化

```yaml
parametric:
  default:
    sphere.radius: 0.2
    beam.thickness: 0.1
    scale.factor: 1.0
  sweeps:
    - parameter: "sphere.radius"
      values: [0.15, 0.2]
    - parameter: "beam.thickness"
      values: [0.08, 0.1]
    - parameter: "scale.factor"
      values: [0.9, 1.0, 1.1]
# → 2 × 2 × 3 = 12ジョブ
```

## トラブルシューティング

### 問題: バリデーションエラー

```
✗ YAML validation failed:
  geometry -> sphere -> 0 -> radius: Input should be greater than 0
```

**解決策**: YAMLファイルを確認し、エラーメッセージに従って修正

### 問題: 球の重なり

```
✗ Geometry validation failed:
  Spheres 1 and 2 overlap: distance=0.8000, min_distance=1.0000
```

**解決策**:
- 球の位置を調整
- または球の半径を小さくする

### 問題: ジョブが多すぎる

```
Parametric Study:
  Total jobs to generate: 100
Generate 100 jobs? [y/N]:
```

**解決策**:
- スイープの値を減らす
- または段階的にパラメータを最適化する

## さらに詳しく

- [README.md](README.md) - 詳細な使用方法
- [../../docs/feature/FU01_custom_lattice.md](../../docs/feature/FU01_custom_lattice.md) - 設計書
- [../../tests/fixtures/](../../tests/fixtures/) - テスト用サンプル

## ヘルプ

```bash
# ジョブ生成のヘルプ
python scripts/generate_custom_lattice_job.py --help

# ジョブ実行のヘルプ
python scripts/execute_comsol_job.py --help
```
