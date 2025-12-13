# Parametric Study Design

## 概要

COMSOL Multiphysicsでのパラメトリック解析における設計方針とタスク管理。

## 現在の設計（v1.0 - 実装済み）

### 基本方針

**1つのジョブ = 1つのジオメトリ構造 + strainのパラメトリックスイープ**

- ジオメトリ（球の半径、ビームの太さなど）は固定
- 境界条件（強制変位 `disp`）のみをCOMSOL内部でスイープ
- 1ジョブで1つの応力-ひずみ曲線（S-Sカーブ）を取得

### アーキテクチャ

```
YAML設定ファイル (1つのジオメトリ定義)
    ↓
Job生成スクリプト
    ↓
job_001/
  ├── job_001.java      (ジオメトリ固定、dispをスイープ)
  ├── run.bat
  └── results/
      └── S-S curve data
```

### YAMLファイル構造（現状）

```yaml
job:
  name: "Simple Cubic Lattice"
  description: "..."
  scale:
    length: 1e-3
    force: 1e-3

geometry:
  lattice_vector: [...]
  sphere: [...]         # 固定値
  beam: [...]           # 固定値

study:
  strain_delta: 0.01    # dispの刻み幅
  strain_range: [0.0, 0.05]  # dispの範囲
  boundary_conditions:
    fixed: true
    copyface: true
```

### メリット

1. **計算効率**: メッシュ生成は1回だけ、同じメッシュで複数の境界条件を計算
2. **エラーの局所化**: ジオメトリ固定なのでメッシュエラーが起きにくい
3. **データ管理の容易さ**: 1ジョブフォルダ = 1つのS-Sカーブ

---

## 将来の拡張方針（v2.0 - TODO）

### 目標

**複数のジオメトリバリエーションを一度に解析**

### 2階層のループ構造

```
外側のループ（Python/Job生成レベル）
├── ジオメトリパラメータの変更
│   ├── sphere_radius: [0.15, 0.20, 0.25]
│   ├── beam_thickness: [0.08, 0.10, 0.12]
│   └── 組み合わせ = 3 × 3 = 9 ジョブ
│
内側のループ（COMSOL/Parametric Sweep）
└── 物理パラメータ（disp）のスイープ
    └── 各ジョブで同じメッシュを使い回し
```

### 拡張後のYAML構造案

```yaml
job:
  name: "Parametric Geometry Study"
  description: "Multiple geometry variations"

# ジオメトリのバリエーション（各組み合わせが1つのジョブになる）
geometry_variations:
  - sphere_radius: 0.15
    beam_thickness: 0.08
  - sphere_radius: 0.20
    beam_thickness: 0.08
  - sphere_radius: 0.15
    beam_thickness: 0.10

# または、グリッドサーチ形式
geometry_parameters:
  sphere_radius: [0.15, 0.20, 0.25]
  beam_thickness: [0.08, 0.10, 0.12]

# 各ジョブで共通のスイープ設定
study:
  strain_delta: 0.01
  strain_range: [0.0, 0.05]
  boundary_conditions:
    fixed: true
    copyface: true
```

### 実装タスク

#### Phase 1: データモデル拡張
- [ ] `CustomLatticeJob` に `geometry_variations` フィールドを追加
- [ ] バリデーションロジックの実装
- [ ] 後方互換性の確保（既存のYAMLファイルも動作）

#### Phase 2: Job生成ロジック
- [ ] `geometry_variations` から複数ジョブを生成する機能
- [ ] ジョブIDの命名規則（例: `job_001_r015_w008`）
- [ ] メタデータへのパラメータ記録

#### Phase 3: Python側のループ実装
```python
# 疑似コード
for variation in geometry_variations:
    job_params = {
        'sphere_radius': variation['sphere_radius'],
        'beam_thickness': variation['beam_thickness'],
        # ジオメトリを更新
    }
    generate_job(f"job_{idx:03d}", job_params)
```

#### Phase 4: 結果の集約
- [ ] 複数ジョブの結果を統合してプロット
- [ ] パラメータ vs 物性値のマトリックス生成
- [ ] 可視化ツールの拡張

### アーキテクチャ（拡張後）

```
YAML設定ファイル (複数のジオメトリ定義)
    ↓
Job生成スクリプト
    ↓
run_YYYYMMDD_HHMMSS/
  ├── job_001/  (r=0.15, w=0.08)
  │   ├── job_001.java
  │   └── results/ (S-S curve A)
  ├── job_002/  (r=0.20, w=0.08)
  │   ├── job_002.java
  │   └── results/ (S-S curve B)
  └── job_003/  (r=0.15, w=0.10)
      ├── job_003.java
      └── results/ (S-S curve C)
```

---

## 参考: メッシュ生成と計算負荷

### ジオメトリ変更時
- メッシュの再生成が必要
- 計算コスト: 高
- エラーリスク: 中（形状によってメッシュが失敗する可能性）

### 境界条件変更時（disp）
- 同じメッシュを再利用
- 計算コスト: 低
- エラーリスク: 低

### 推奨アプローチ
**ジオメトリ変更 = 別ジョブ**として分離することで、計算効率とエラー管理を両立。

---

## 実装優先度

1. **現在（v1.0）**: 1ジオメトリ + strainスイープ → **完遂が目標**
2. **次期（v2.0）**: 複数ジオメトリのバッチ生成 → **上記タスク参照**
3. **将来（v3.0）**: 材料特性もパラメータ化（Young率、Poisson比など）

---

## 関連ファイル

- `examples/custom_lattice/simple_cubic.yml` - 現在の設定例
- `src/data/models/custom_lattice.py` - データモデル定義
- `src/services/job_generator.py` - ジョブ生成ロジック
- `scripts/generate_custom_lattice_job.py` - CLI スクリプト
