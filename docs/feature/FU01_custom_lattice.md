# カスタム格子機能 実装設計書 v2.0

**最終更新**: 2025-12-13
**ベース**: `tests/data/prototype.java` (実動作確認済み)

---

## 目次

1. [概要](#概要)
2. [プロトタイプ分析](#プロトタイプ分析)
3. [YAMLスキーマ](#yamlスキーマ)
4. [システムアーキテクチャ](#システムアーキテクチャ)
5. [ジオメトリビルダー詳細](#ジオメトリビルダー詳細)
6. [実装計画](#実装計画)
7. [技術仕様](#技術仕様)

---

## 概要

カスタム格子（Custom Lattice）機能は、ユーザーが独自の格子構造をYAML形式で定義し、COMSOL Multiphysicsでシミュレーションして弾性特性を計算する機能です。

### 設計方針

- **prototype.javaを完全にベースとする**: 既存テンプレートは無視し、実動作する `tests/data/prototype.java` の構造をそのまま踏襲
- **mm単位に統一**: すべての座標・半径・太さはmm（ミリメートル）単位
- **パラメトリックスタディは複数ファイル生成**: 球半径・梁太さのスイープは個別のJavaファイルを生成して対応

### 主要機能

1. **YAMLベースの格子定義**: 球（sphere）と梁（beam）の配置、材料特性、メッシュ設定
2. **柔軟なパラメトリックスタディ**: 全球一括 (`sphere.radius`) と個別指定 (`sphere.0.radius`) の両方をサポート
3. **弾性特性の自動計算**: C_ij, S_ij, ヤング率, ポアソン比, せん断弾性率, 体積弾性率
4. **結果の標準化出力**: CSV, YAML, DAT形式での出力

---

## プロトタイプ分析

### 1. ハードコードされたジオメトリデータ

`tests/data/prototype.java` では、ジオメトリデータがメソッド内に直接定義されています：

```java
private static double[][] createHardcodedSpheres(double lconst) {
    double[][] points = new double[][]{
        {0.0 * lconst, 0.0 * lconst, 0.0 * lconst},  // sphere_001
        {0.0 * lconst, 0.0 * lconst, 1.0 * lconst},  // sphere_002
        {0.0 * lconst, 1.0 * lconst, 0.0 * lconst},  // sphere_003
        // ... 8個の球
    };
    return points;
}

private static double[][][] createHardcodedBeams(double[][] points) {
    double[][][] lines = new double[][][]{
        {points[0], points[2]},  // sphere_001 → sphere_003
        {points[0], points[4]},  // sphere_001 → sphere_005
        // ... 12本の梁
    };
    return lines;
}
```

**Jinja2テンプレート化の方針**:
```jinja
double[][] points = new double[][]{
    {% for sphere in spheres -%}
    {{{ sphere.position[0] }}, {{ sphere.position[1] }}, {{ sphere.position[2] }}}{% if not loop.last %},{% endif %}

    {% endfor -%}
};

double[][][] lines = new double[][][]{
    {% for beam in beams -%}
    {points[{{ beam.endpoint1_index }}], points[{{ beam.endpoint2_index }}]}{% if not loop.last %},{% endif %}

    {% endfor -%}
};
```

### 2. 主要パラメータのマッピング

| prototype.java | YAML定義 | 単位 | 説明 |
|----------------|----------|------|------|
| `lconst` | `geometry.lattice_constant` | mm | 格子定数 |
| `rs` | `geometry.spheres[i].radius` | mm | 球の半径 |
| `rb` | `geometry.beams[i].thickness / 2` | mm | 梁の半径（太さの半分） |
| `delta_` | `study.strain.delta` | - | 最大歪み（0.01 = 1%） |
| `pratio` | `materials.mat1.poissons_ratio` | - | ポアソン比 |
| `youngsModulus` | `materials.mat1.youngs_modulus` | Pa | ヤング率 |
| `density` | `materials.mat1.density` | kg/m³ | 密度 |
| `meshSize` | `mesh.size` | - | autoMeshSize値（1-9） |

### 3. ジオメトリ生成フロー（prototype.javaより）

```
1. createSpheres()
   - 各球をSphereオブジェクトとして作成
   - 全てをunion (uni1) に追加

2. createBeams()
   - LineSegment: 2点を結ぶ線分
   - WorkPlane: 線分に垂直な作業平面
   - Circle: 作業平面上に円（半径rb）を作成
   - Sweep: 円を線分に沿ってスイープ → 円柱（梁）
   - unionに追加

3. createBlockOperations()
   - blk0: 単位セルのボックス
   - dif1 = blk0 - uni1 (ボックスから格子を引く → 空隙部分)
   - blk1: もう1つのボックス
   - dif2 = blk1 - dif1 (ボックスから空隙を引く → 格子構造のみ残る)

4. createBoundarySelections()
   - boxsel1-6: 6面（X-, X+, Y-, Y+, Z-, Z+）
   - boxsel7: 原点（0,0,0）の点

5. geom1.run()
   - ジオメトリをビルド
```

### 4. 周期境界条件

**GeneralExtrusion** で対向面をマッピング:

| Coupling | Source Face | Destination Mapping | 説明 |
|----------|-------------|---------------------|------|
| coupleX | boxsel1 (X-) | X-Lx, Y, Z | X+面をX-面にマッピング |
| coupleY | boxsel3 (Y-) | X, Y-Ly, Z | Y+面をY-面にマッピング |
| coupleZ | boxsel5 (Z-) | X, Y, Z-Lz | Z+面をZ-面にマッピング |

**Displacement2** で周期変位を設定:

```java
// periodicX (disp1)
U0 = {
    {"coupleX(u) - E11 * X * disp"},
    {"coupleX(v) - E21 * X * disp"},
    {"coupleX(w) - E31 * X * disp"}
}
```

### 5. パラメトリックスタディ（歪みテンソル）

prototype.javaでは、**9つの歪み状態**をバッチ実行：

- Cases 1-3: e11, e22, e33 (軸方向歪み)
- Cases 4-6: e23, e13, e12 (せん断歪み)
- Cases 7-9: その他の組み合わせ（検証用）

**本実装での方針**:
- 歪みスイープ（9状態）はprototypeのまま維持
- **球半径・梁太さのパラメトリックスタディは別途実装**（複数Javaファイル生成）

### 6. 結果出力

| ファイル | 内容 |
|---------|------|
| `job_001_kirchhoff.txt` | Kirchhoff応力テンソル (9成分 × 歪みステップ) |
| `job_001_maxmises.txt` | 最大von Mises応力 |
| `job_001_animation.gif` | 変形アニメーション |
| `job_001_stress.png` | 応力分布の静止画 |

---

## YAMLスキーマ

### 完全なスキーマ例

```yaml
job:
  name: "Simple Cubic Lattice"
  description: "8 spheres and 12 beams forming a cubic unit cell"
  unit_cell_size: [15.0, 15.0, 15.0]  # mm単位 [Lx, Ly, Lz]

  parametric:
    default:
      sphere.radius: 1.0       # 全球のデフォルト半径 (mm)
      beam.thickness: 0.5      # 全梁のデフォルト太さ (mm)

    sweeps:
      # 全球の半径を一括変更
      - parameter: "sphere.radius"
        values: [0.8, 1.0, 1.2]

      # 全梁の太さを一括変更
      - parameter: "beam.thickness"
        values: [0.4, 0.5, 0.6]

      # 特定の球（ID=1, 0-indexed）のみ変更
      - parameter: "sphere.0.radius"
        values: [0.9, 1.0, 1.1]

geometry:
  lattice_constant: 15.0  # mm (基準長さ)

  spheres:
    - id: 1
      position: [0.0, 0.0, 0.0]   # mm（絶対座標）
      radius: 1.0                  # mm
    - id: 2
      position: [0.0, 0.0, 15.0]
      radius: 1.0
    - id: 3
      position: [0.0, 15.0, 0.0]
      radius: 1.0
    - id: 4
      position: [0.0, 15.0, 15.0]
      radius: 1.0
    - id: 5
      position: [15.0, 0.0, 0.0]
      radius: 1.0
    - id: 6
      position: [15.0, 0.0, 15.0]
      radius: 1.0
    - id: 7
      position: [15.0, 15.0, 0.0]
      radius: 1.0
    - id: 8
      position: [15.0, 15.0, 15.0]
      radius: 1.0

  beams:
    # 底面（Z=0）
    - {id: 1, endpoints: [1, 3], thickness: 0.5}
    - {id: 2, endpoints: [1, 5], thickness: 0.5}
    - {id: 3, endpoints: [3, 7], thickness: 0.5}
    - {id: 4, endpoints: [5, 7], thickness: 0.5}
    # 上面（Z=15）
    - {id: 5, endpoints: [2, 4], thickness: 0.5}
    - {id: 6, endpoints: [2, 6], thickness: 0.5}
    - {id: 7, endpoints: [4, 8], thickness: 0.5}
    - {id: 8, endpoints: [6, 8], thickness: 0.5}
    # 垂直エッジ
    - {id: 9, endpoints: [1, 2], thickness: 0.5}
    - {id: 10, endpoints: [3, 4], thickness: 0.5}
    - {id: 11, endpoints: [5, 6], thickness: 0.5}
    - {id: 12, endpoints: [7, 8], thickness: 0.5}

materials:
  mat1:
    name: "Polymer"
    youngs_modulus: 10e6    # Pa (10 MPa)
    poissons_ratio: 0.0     # 無次元
    density: 950            # kg/m³

mesh:
  size: 5                   # autoMeshSize(5)
  type: "FreeTri"           # 現状未使用（将来拡張用）

study:
  strain:
    delta: 0.01                        # 最大歪み（1%）
    steps: "0, 0.25, 0.5, 0.75, 1"    # 変位ステップ
  boundary_conditions:
    fixed: true      # 原点固定
    copyface: true   # 周期境界条件
```

### パラメータ指定の柔軟性

| 指定方法 | 対象 | 例 |
|---------|------|---|
| `sphere.radius` | 全球を一括 | `values: [0.8, 1.0, 1.2]` |
| `sphere.0.radius` | 特定の球（0-indexed） | `values: [0.9, 1.1]` |
| `beam.thickness` | 全梁を一括 | `values: [0.4, 0.5]` |
| `beam.3.thickness` | 特定の梁（0-indexed） | `values: [0.3, 0.6]` |

**適用順序**: 一括指定 → 個別指定（個別が優先）

---

## システムアーキテクチャ

### 全体フロー

```
┌──────────────────┐
│ YAML定義ファイル  │
└────────┬─────────┘
         │ (1) load_custom_lattice_yaml()
         ▼
┌─────────────────────┐
│ YAMLパーサー         │
│ (yaml_loader.py)    │
│ • Pydantic validation│
│ • Geometry validation│
└────────┬────────────┘
         │ (2) CustomLatticeJob
         ▼
┌─────────────────────┐
│ ParametricGenerator │
│ (parametric_generator.py) │
│ • スイープ展開       │
│ • 組み合わせ生成     │
└────────┬────────────┘
         │ (3) List[ParameterSet]
         ▼
    ┌────────────────┐
    │ 各ParameterSet │
    └────┬───────────┘
         │ (4) apply_parameters()
         ▼
┌──────────────────────┐
│ GeometryBuilder      │
│ (geometry_builder.py) │
│ • 座標スケーリング    │
│ • 梁の端点計算        │
│ • パラメータ適用      │
└────────┬─────────────┘
         │ (5) GeometryData
         ▼
┌──────────────────────┐
│ Jinja2テンプレート    │
│ (custom_lattice.java.j2) │
│ • prototype.javaベース│
└────────┬─────────────┘
         │ (6) job_001.java, job_002.java, ...
         ▼
┌──────────────────────┐
│ COMSOL実行           │
│ (BatchExecutor)      │
└────────┬─────────────┘
         │ (7) kirchhoff.txt, maxmises.txt, ...
         ▼
┌──────────────────────┐
│ ResultAnalyzer       │
│ • 弾性テンソル計算    │
│ • CSV/YAML出力        │
└──────────────────────┘
```

### データフロー詳細

#### (1) YAML → Pydantic Model

```python
from src.parsers import load_custom_lattice_yaml

job = load_custom_lattice_yaml('simple_cubic.yml')
# job: CustomLatticeJob
# - job.geometry.spheres: List[Sphere]
# - job.geometry.beams: List[Beam]
# - job.job.parametric.sweeps: List[ParametricSweep]
```

#### (2) Pydantic Model → ParameterSets

```python
from src.services.parametric_generator import ParametricGenerator

generator = ParametricGenerator(job)
param_sets = generator.generate_parameter_sets()
# param_sets: List[ParameterSet]
# 例: 3×2=6個のパラメータセット
```

#### (3) ParameterSet → Geometry適用

```python
from src.services.geometry_builder import GeometryBuilder

builder = GeometryBuilder()
for param_set in param_sets:
    geometry_data = builder.build_geometry_data(job, param_set)
    # geometry_data.spheres: 座標・半径が確定した球のリスト
    # geometry_data.beams: 端点座標・太さが確定した梁のリスト
```

#### (4) GeometryData → Java生成

```python
from src.services.job_generator import JobGenerator

job_gen = JobGenerator(template_dir='templates', output_base_dir='jobs/comsol')
for idx, param_set in enumerate(param_sets):
    geometry_data = builder.build_geometry_data(job, param_set)
    job_gen.render_template(
        template_name='custom_lattice.java.j2',
        context={
            'spheres': geometry_data.spheres,
            'beams': geometry_data.beams,
            'lattice_constant': job.geometry.lattice_constant,
            'materials': job.materials,
            # ...
        },
        output_path=f'run_XXX/job_{idx+1:03d}/job_{idx+1:03d}.java'
    )
```

---

## ジオメトリビルダー詳細

### GeometryBuilderの責務

`src/services/geometry_builder.py` は以下の処理を実行：

#### 1. lattice_constantによるスケーリング

**相対座標 → 絶対座標**（オプション）:

```python
def scale_position(relative_pos: List[float], lattice_constant: float) -> List[float]:
    """相対座標（0~1）を絶対座標（mm）に変換"""
    return [pos * lattice_constant for pos in relative_pos]

# 例:
# relative: [0.5, 0.5, 0.5]
# lattice_constant: 15.0
# → absolute: [7.5, 7.5, 7.5]
```

**絶対座標の場合**: そのまま使用（YAMLでmm単位指定済み）

#### 2. 梁の端点座標の自動計算

YAMLでは球IDのみ指定 → ビルダーが座標を取得：

```python
def calculate_beam_endpoints(beam: Beam, spheres: List[Sphere]) -> Tuple[List[float], List[float]]:
    """梁の端点座標を球IDから取得"""
    sphere1_id, sphere2_id = beam.endpoints

    # IDからsphereオブジェクトを検索（0-indexed変換）
    sphere1 = next(s for s in spheres if s.id == sphere1_id)
    sphere2 = next(s for s in spheres if s.id == sphere2_id)

    return sphere1.position, sphere2.position

# 例:
# Beam(id=1, endpoints=[1, 2])
# Sphere(id=1, position=[0, 0, 0])
# Sphere(id=2, position=[0, 0, 15])
# → endpoint1=[0, 0, 0], endpoint2=[0, 0, 15]
```

#### 3. パラメトリックパラメータの適用

**適用順序**: 一括指定 → 個別指定

```python
def apply_parametric_parameters(geometry: Geometry, param_set: ParameterSet) -> Geometry:
    """パラメータセットをジオメトリに適用"""
    import copy
    new_geometry = copy.deepcopy(geometry)

    # (1) 一括指定を先に適用
    if 'sphere.radius' in param_set.parameters:
        radius = param_set.parameters['sphere.radius']
        for sphere in new_geometry.spheres:
            sphere.radius = radius

    if 'beam.thickness' in param_set.parameters:
        thickness = param_set.parameters['beam.thickness']
        for beam in new_geometry.beams:
            beam.thickness = thickness

    # (2) 個別指定で上書き
    for param_name, param_value in param_set.parameters.items():
        if param_name.startswith('sphere.') and '.' in param_name[7:]:
            # 例: "sphere.0.radius" → index=0, field="radius"
            parts = param_name.split('.')
            index = int(parts[1])
            field = parts[2]

            if field == 'radius':
                new_geometry.spheres[index].radius = param_value

        elif param_name.startswith('beam.') and '.' in param_name[5:]:
            # 例: "beam.3.thickness" → index=3, field="thickness"
            parts = param_name.split('.')
            index = int(parts[1])
            field = parts[2]

            if field == 'thickness':
                new_geometry.beams[index].thickness = param_value

    return new_geometry
```

**適用例**:

```yaml
parametric:
  sweeps:
    - parameter: "sphere.radius"      # 全球 → 0.8
      values: [0.8]
    - parameter: "sphere.0.radius"    # sphere[0]のみ → 1.2
      values: [1.2]

# 結果:
# sphere[0].radius = 1.2  (個別指定で上書き)
# sphere[1].radius = 0.8  (一括指定)
# sphere[2].radius = 0.8
# ...
```

### GeometryDataクラス

Jinja2テンプレートに渡すデータ構造：

```python
@dataclass
class SphereData:
    """テンプレート用の球データ"""
    id: int
    position: List[float]  # mm単位の絶対座標
    radius: float          # mm

@dataclass
class BeamData:
    """テンプレート用の梁データ"""
    id: int
    endpoint1_index: int   # points配列のインデックス（0-indexed）
    endpoint2_index: int
    thickness: float       # mm（直径）

@dataclass
class GeometryData:
    """テンプレートに渡すジオメトリデータ"""
    spheres: List[SphereData]
    beams: List[BeamData]
    lattice_constant: float
    unit_cell_size: List[float]
```

---

## 実装計画

### Phase 1: GeometryBuilderの実装 (3日)

**ファイル**: `src/services/geometry_builder.py` (新規作成)

**クラス・メソッド**:

```python
class GeometryBuilder:
    def build_geometry_data(
        self,
        job: CustomLatticeJob,
        param_set: ParameterSet
    ) -> GeometryData:
        """パラメータセットを適用してジオメトリデータを生成"""

    def apply_parametric_parameters(
        self,
        geometry: Geometry,
        param_set: ParameterSet
    ) -> Geometry:
        """パラメータ適用（一括 → 個別の順）"""

    def calculate_beam_endpoints(
        self,
        beam: Beam,
        spheres: List[Sphere]
    ) -> Tuple[int, int]:
        """梁の端点インデックスを計算（0-indexed）"""

    def scale_position(
        self,
        position: List[float],
        lattice_constant: float
    ) -> List[float]:
        """座標スケーリング（相対→絶対、または絶対のまま）"""
```

**ユニットテスト**: `tests/unit/test_geometry_builder.py`

### Phase 2: Jinja2テンプレートの改訂 (5日)

**ファイル**: `templates/custom_lattice.java.j2`

**方針**:
- `tests/data/prototype.java` を完全にベースにする
- 既存の `custom_lattice.java.j2` は破棄
- 以下の箇所をJinja2変数化:
  - ジオメトリデータ（spheres, beams）
  - 材料特性（youngs_modulus, poissons_ratio, density）
  - メッシュ設定（size）
  - スタディ設定（delta, steps）
  - 単位セルサイズ（unit_cell_size）

**主要な変更箇所**:

```java
// パラメータ定義部
double lconst = {{ lattice_constant }};  // mm
double rs = {{ default_sphere_radius }};  // mm (未使用、個別半径を使用)
double rb = {{ default_beam_radius }};    // mm (未使用、個別太さを使用)
double delta_ = {{ strain_delta }};
double pratio = {{ poissons_ratio }};
String[] dstep = new String[]{「{{ strain_steps }}」};

// 球の定義
private static double[][] createHardcodedSpheres(double lconst) {
    double[][] points = new double[][]{
        {% for sphere in spheres -%}
        {{{ sphere.position[0] }}, {{ sphere.position[1] }}, {{ sphere.position[2] }}}{% if not loop.last %},{% endif %}

        {% endfor -%}
    };
    return points;
}

// 梁の定義
private static double[][][] createHardcodedBeams(double[][] points) {
    double[][][] lines = new double[][][]{
        {% for beam in beams -%}
        {points[{{ beam.endpoint1_index }}], points[{{ beam.endpoint2_index }}]}{% if not loop.last %},{% endif %}

        {% endfor -%}
    };
    return lines;
}

// 球の半径（個別）
double[] sphereRadii = new double[]{
    {% for sphere in spheres -%}
    {{ sphere.radius }}{% if not loop.last %},{% endif %}

    {% endfor -%}
};

// 梁の太さ（個別）
double[] beamThicknesses = new double[]{
    {% for beam in beams -%}
    {{ beam.thickness }}{% if not loop.last %},{% endif %}

    {% endfor -%}
};
```

### Phase 3: JobGeneratorの拡張 (2日)

**ファイル**: `src/services/job_generator.py` (拡張)

**メソッド追加**:

```python
def generate_parametric_study_jobs(
    self,
    custom_job: CustomLatticeJob,
    run_id: Optional[str] = None
) -> Dict[str, Any]:
    """パラメトリックスタディのジョブを一括生成

    Returns:
        {
            'run_id': str,
            'run_dir': Path,
            'total_jobs': int,
            'job_dirs': List[Path]
        }
    """
```

### Phase 4: ParametricGeneratorの拡張 (2日)

**ファイル**: `src/services/parametric_generator.py` (拡張)

**拡張内容**:
- 個別指定のパース (`sphere.0.radius` → `(sphere, 0, radius)`)
- パラメータ適用優先順位の実装

### Phase 5: ResultAnalyzerの実装 (3日)

**ファイル**: `src/services/result_analyzer.py` (拡張)

**機能**:
- `analyze_custom_lattice_job(job_dir: Path) -> Dict`
- `generate_parametric_summary(run_dir: Path) -> pd.DataFrame`

**出力**:
- `job_001/results.yml`
- `job_001/elastic_constants.csv`
- `results_parametric_study.csv`（全ジョブのまとめ）

### Phase 6: 統合テストとドキュメント (3日)

**統合テスト**: `tests/integration/test_custom_lattice_workflow.py`

**ユーザーマニュアル**: `docs/user_guide_custom_lattice.md`

**サンプルYAML**:
- `examples/custom_lattice/simple_cubic.yml`
- `examples/custom_lattice/bcc.yml`

---

## 技術仕様

### 座標系と単位

- **長さ単位**: mm（ミリメートル）
- **座標系**: 右手系、原点 (0, 0, 0)
- **COMSOL設定**: `lengthUnit("mm")`
- **YAMLでの指定**: 絶対座標（mm単位）で直接指定

### ジオメトリ制約

| 項目 | 制約 |
|------|------|
| 球の最小半径 | 0.01 mm |
| 梁の最小太さ | 0.01 mm |
| 球の重なり | 中心間距離 > (半径1 + 半径2) × 0.95 |
| 単位セル境界 | 球の中心が `[0, Lx] × [0, Ly] × [0, Lz]` 内 |

### パラメトリックスタディの制限

- **最大ジョブ数**: 100（超える場合は警告 + ユーザー確認）
- **パラメータ次元**: 最大5次元
- **インデックス**: 0-indexed（`sphere.0.radius` = 1番目の球）

### バリデーション戦略

#### レベル1: YAMLパース時（Pydantic）
- 型チェック、範囲チェック
- 球ID・梁IDの重複チェック
- 梁の端点参照整合性チェック

#### レベル2: ジオメトリ検証時
- 球同士の重なりチェック
- 球が単位セル外に出ていないかチェック

#### レベル3: パラメトリック展開時
- パラメータ名の妥当性チェック
- 組み合わせ数の上限チェック

---

## 成功基準

- [ ] YAMLファイルから複数のJavaファイルが正常に生成できる
- [ ] 生成されたJavaファイルがCOMSOLでコンパイル・実行できる
- [ ] パラメトリックスイープで期待通りのジョブ数が生成される
- [ ] 個別指定（`sphere.0.radius`）が正しく動作する
- [ ] 球の重なりチェックが機能する
- [ ] Kirchhoff応力から弾性テンソルが正しく計算される
- [ ] CSV/YAML形式で結果が出力される
- [ ] ユニットテストカバレッジ 80% 以上
- [ ] E2Eテストが全てパスする
- [ ] ユーザーマニュアルが整備されている

---

## リスクと対策

| リスク | 影響 | 対策 |
|--------|------|------|
| パラメトリック組み合わせ爆発 | 高 | 上限100ジョブ、警告表示 |
| ユーザーの不正なYAML入力 | 中 | Pydantic + 詳細エラーメッセージ |
| 球・梁の配置エラー | 中 | GeometryValidatorで厳密チェック |
| prototype.javaとの互換性 | 高 | プロトタイプを完全ベースにする |
| 単位系の混乱 | 中 | mm統一、ドキュメント明記 |

---

## 補足事項

### 弾性テンソルの記法

- **Voigt記法**: 6×6行列（C_11, C_12, ..., C_66）
- **スティフネステンソル**: C_ij（応力 = C_ij × ひずみ）
- **コンプライアンステンソル**: S_ij（ひずみ = S_ij × 応力、S = C^(-1)）

### 既存機能との統合

```python
from src.services import JobGenerator
from src.parsers import load_custom_lattice_yaml

# カスタム格子機能
generator = JobGenerator(template_dir='templates', output_base_dir='jobs/comsol')
custom_job = load_custom_lattice_yaml('examples/simple_cubic.yml')
result = generator.generate_parametric_study_jobs(custom_job, run_id='test_run_01')

print(f"Generated {result['total_jobs']} jobs in {result['run_dir']}")
```

---

## 参考資料

- **プロトタイプ**: `tests/data/prototype.java`
- **既存Pydanticモデル**: `src/data/models/custom_lattice.py`
- **既存パーサー**: `src/parsers/yaml_loader.py`
- **既存パラメトリック生成器**: `src/services/parametric_generator.py`
