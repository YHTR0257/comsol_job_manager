# カスタム格子YAML設定ファイル

このディレクトリには、カスタム格子構造を定義するYAMLファイルの例が含まれています。

## ディレクトリ構造

```
examples/custom_lattice/
├── README.md                    # このファイル
├── simple_cubic.yml             # シンプルな立方格子の例
├── bcc_like.yml                 # BCC風の格子の例
├── tetrahedral.yml              # 四面体構造の例
└── parametric_study.yml         # パラメトリックスタディの例
```

## 使用方法

### 1. YAMLファイルを作成または編集

```bash
# エディタで開く
vi examples/custom_lattice/simple_cubic.yml
```

### 2. ジョブを生成

```bash
# 基本的な使用方法
python scripts/generate_custom_lattice_job.py -i examples/custom_lattice/simple_cubic.yml

# 出力ディレクトリを指定
python scripts/generate_custom_lattice_job.py \
    -i examples/custom_lattice/simple_cubic.yml \
    -o jobs/comsol

# Run IDを指定（わかりやすい名前をつける）
python scripts/generate_custom_lattice_job.py \
    -i examples/custom_lattice/simple_cubic.yml \
    --run-id simple_cubic_test_01
```

### 3. ジョブを実行（WSL環境のみ）

```bash
# 生成されたジョブディレクトリを指定
python scripts/test_job_executor.py -j jobs/comsol/simple_cubic_test_01

# タイムアウトを指定（デフォルト: 3600秒 = 1時間）
python scripts/test_job_executor.py \
    -j jobs/comsol/simple_cubic_test_01 \
    -t 7200  # 2時間
```

## YAMLファイルのフォーマット

詳細は[docs/feature/FU01_custom_lattice.md](../../docs/feature/FU01_custom_lattice.md)を参照してください。

### 基本構造

```yaml
job:
  name: "格子の名前"
  description: "説明"
  scale:
    length: 1e-3  # 長さスケール (m)
    force: 1e-3   # 力スケール (N)
  parametric:
    default:
      sphere.radius: 0.2
      beam.thickness: 0.1
    # オプション: パラメトリックスイープ
    sweep1:
      parameter: "sphere.radius"
      values: [0.15, 0.2, 0.25]
    sweep2:
      parameter: "beam.thickness"
      values: [0.08, 0.1]

geometry:
  lattice_vector:
    - [2.0, 0.0, 0.0]
    - [0.0, 2.0, 0.0]
    - [0.0, 0.0, 2.0]
  sphere:
    - id: 1
      radius: 0.2
      position: [0, 0, 0]
    - id: 2
      radius: 0.2
      position: [1, 0, 0]
  beam:
    - id: 1
      endpoints: [1, 2]
      thickness: 0.1

mesh:
  size: 5
  type: "FreeTri"

materials:
  material_1:
    name: "mat1"
    youngs_modulus: 200e9  # Pa
    poissons_ratio: 0.3
    density: 960  # kg/m^3

study:
  parametic_sweep:
    strain:
      delta: 0.01
      range: [0.0, 0.05]
  boundary_conditions:
    fixed: true
    copyface: true
```

## パラメトリックスタディ

### 2つのパラメータをスイープ

```yaml
parametric:
  default:
    sphere.radius: 0.2
    beam.thickness: 0.1
  sweep1:
    parameter: "sphere.radius"
    values: [0.15, 0.2, 0.25]  # 3つの値
  sweep2:
    parameter: "beam.thickness"
    values: [0.08, 0.1]         # 2つの値
# → 3 × 2 = 6個のジョブが生成されます
```

### 3つ以上のパラメータをスイープ

```yaml
parametric:
  default:
    sphere.radius: 0.2
    beam.thickness: 0.1
    scale.factor: 1.0
  sweeps:  # sweepsリストを使用
    - parameter: "sphere.radius"
      values: [0.15, 0.2]
    - parameter: "beam.thickness"
      values: [0.08, 0.1]
    - parameter: "scale.factor"
      values: [0.9, 1.0, 1.1]
# → 2 × 2 × 3 = 12個のジョブが生成されます
```

## バリデーション

ジョブ生成前に自動的に以下のチェックが行われます：

1. **YAMLフォーマット**: 構文エラーのチェック
2. **必須フィールド**: 全ての必須項目の存在確認
3. **データ型**: 数値、文字列などの型チェック
4. **ジオメトリ検証**:
   - 球の重なりチェック
   - ビームと球の接続確認
   - 格子ベクトルの妥当性

バリデーションをスキップする場合（推奨しません）:
```bash
python scripts/generate_custom_lattice_job.py \
    -i my_lattice.yml \
    --no-validate
```

## トラブルシューティング

### エラー: "Spheres overlap"
- 球の位置と半径を調整してください
- 球の中心間距離 > 半径の和 となるようにしてください

### エラー: "Beam does not connect"
- ビームのendpointsが正しい球IDを参照しているか確認
- 球が離れすぎていないか確認

### エラー: "Missing required parameter"
- YAMLファイルの必須フィールドが全て含まれているか確認
- サンプルファイルと比較してください

## 参考

- 設計書: [docs/feature/FU01_custom_lattice.md](../../docs/feature/FU01_custom_lattice.md)
- テストファイル: [tests/fixtures/sample_custom_lattice.yml](../../tests/fixtures/sample_custom_lattice.yml)
