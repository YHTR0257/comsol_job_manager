# Custom Lattice Structure Implementation Plan
# カスタム格子構造実装計画書

**Document Version:** 1.0
**Created:** 2025-11-19
**Status:** Draft / 草案

---

## Table of Contents / 目次

1. [Executive Summary / 概要](#executive-summary--概要)
2. [Current State Analysis / 現状分析](#current-state-analysis--現状分析)
3. [Requirements / 要件定義](#requirements--要件定義)
4. [File Format Specification / ファイルフォーマット仕様](#file-format-specification--ファイルフォーマット仕様)
5. [Data Structure Design / データ構造設計](#data-structure-design--データ構造設計)
6. [Implementation Plan / 実装手順](#implementation-plan--実装手順)
7. [Migration Strategy / マイグレーション戦略](#migration-strategy--マイグレーション戦略)
8. [Testing Strategy / テスト戦略](#testing-strategy--テスト戦略)
9. [Timeline / スケジュール](#timeline--スケジュール)

---

## Executive Summary / 概要

### English
This document outlines the implementation plan for transitioning from hardcoded lattice types to a flexible, file-based lattice structure definition system. The new system will support both CSV and YAML formats, allowing researchers to define custom lattice structures without modifying source code.

### 日本語
本文書は、ハードコードされた格子タイプから、柔軟なファイルベースの格子構造定義システムへの移行実装計画を示します。新システムはCSVとYAML両方のフォーマットをサポートし、研究者がソースコードを変更せずにカスタム格子構造を定義できるようになります。

---

## Current State Analysis / 現状分析

### Current Implementation / 現在の実装

#### Hardcoded Lattice Types / ハードコード化された格子タイプ

**Location:** `templates/simulation.java.j2:176-205`

```java
private static LatticeTypeConfig getLatticeTypeConfig(String latticeType, double lconst) {
    LatticeTypeConfig config = new LatticeTypeConfig();

    if (latticeType.equals("fcc")) {
        config.loc = new double[][]{{0,0,0}, {0,.5,.5}, {.5,0,.5}, {.5,.5,0}};
        config.dMin = 0.7 * lconst;
        config.dMax = 0.71 * lconst;
    } else if (latticeType.equals("dia")) {
        config.loc = new double[][]{
            {0,0,0}, {0,.5,.5}, {.5,0,.5}, {.5,.5,0},
            {0.25,0.25,0.25}, {0.25,0.75,0.75}, {0.75,0.25,0.75}, {0.75,0.75,0.25}
        };
        config.dMin = 0.4 * lconst;
        config.dMax = 0.45 * lconst;
    } else if (latticeType.equals("bcc")) {
        config.loc = new double[][]{{0,0,0}, {.5,.5,.5}};
        config.dMin = 0.8 * lconst;
        config.dMax = 0.9 * lconst;
    } else if (latticeType.equals("simple")) {
        config.loc = new double[][]{{0,0,0}};
        config.dMin = 0.9 * lconst;
        config.dMax = 1.1 * lconst;
    }

    return config;
}
```

### Current Data Structure / 現在のデータ構造

```java
private static class LatticeTypeConfig {
    double[][] loc;      // Atomic positions in fractional coordinates / 分数座標での原子位置
    double dMin;         // Minimum bond distance / 最小ボンド距離
    double dMax;         // Maximum bond distance / 最大ボンド距離
}
```

### Limitations / 制約

1. **Inflexibility / 柔軟性の欠如**
   - New lattice types require code modification / 新しい格子タイプにはコード修正が必要
   - No support for complex structures / 複雑な構造に対応できない
   - Template regeneration needed for each change / 変更のたびにテンプレート再生成が必要

2. **Scalability / スケーラビリティ**
   - Limited to predefined types / 事前定義されたタイプに制限
   - Difficult to share custom structures / カスタム構造の共有が困難

3. **Research Workflow / 研究ワークフロー**
   - Requires programming knowledge / プログラミング知識が必要
   - High barrier for material scientists / 材料科学者にとって敷居が高い

---

## Requirements / 要件定義

### Functional Requirements / 機能要件

#### FR1: File-Based Lattice Definition / ファイルベース格子定義
- **Priority:** High / 高
- **Description:** System must read lattice structure definitions from external files
- **説明:** yamlファイルから格子構造定義を読み込む

#### FR2: Backward Compatibility / 後方互換性
- **Priority:** High / 高
- **Description:** Existing hardcoded lattice types must continue to work
- **説明:** 既存のハードコード格子タイプは引き続き動作する必要がある

#### FR3: Validation / バリデーション
- **Priority:** Medium / 中
- **Description:** Validate file format and data integrity
- **説明:** ファイルフォーマットとデータ整合性の検証

#### FR4: Documentation / ドキュメント
- **Priority:** Medium / 中
- **Description:** Provide examples and templates for custom lattice definitions
- **説明:** カスタム格子定義のサンプルとテンプレートを提供

### Non-Functional Requirements / 非機能要件

#### NFR1: Performance / パフォーマンス
- File loading should add < 100ms to job generation time
- ファイル読み込みはジョブ生成時間に100ms未満の追加

#### NFR2: Usability / 使いやすさ
- Non-programmers should be able to define lattices using spreadsheet tools
- プログラマーでなくてもスプレッドシートツールで格子を定義できる

#### NFR3: Maintainability / 保守性
- Clear separation between builtin and custom lattices
- 組み込み格子とカスタム格子の明確な分離

---

## File Format Specification / ファイルフォーマット仕様

### Option 1: YAML Format (Advanced) / YAML形式（高度）

**Advantages / 利点:**
- Human-readable / 人間が読みやすい
- Supports metadata / メタデータをサポート
- Hierarchical structure / 階層構造

**File Structure:**

```yaml
# geometry.yml
spheres:
    sphe1:
        radius_ratio: 15
    sphe2:
        radius_ratio: 8
bonds:
    bond1:
        radius_ratio: 5
    bond2:
        radius_ratio: 3

```
---


### Java Template Integration / Javaテンプレート統合

The Jinja2 template will receive processed data from Python:

```jinja2
{# templates/simulation.java.j2 #}

private static LatticeTypeConfig getLatticeTypeConfig(String latticeType, double lconst) {
    LatticeTypeConfig config = new LatticeTypeConfig();

    // Generated from lattice library
    config.loc = new double[][]{% raw %}{
        {% for atom in lattice_atoms %}
        {{'{'}}{{ atom[0] }}, {{ atom[1] }}, {{ atom[2] }}{{'}'}}{{ "," if not loop.last }}
        {% endfor %}
    }{% endraw %};
    config.dMin = {{ lattice_d_min }};
    config.dMax = {{ lattice_d_max }};

    return config;
}
```

---

## Implementation Plan / 実装手順

### Phase 1: Core Implementation / コア実装

#### Step 1.1: Create Data Models / データモデル作成
**Files:** `src/data/lattice_structure.py`

```bash
# Create new module
touch src/data/lattice_structure.py
```

**Tasks:**
- [ ] Implement `BondDistance` dataclass
- [ ] Implement `LatticeStructure` dataclass
- [ ] Implement `LatticeLibrary` class
- [ ] Add validation methods
- [ ] Add YAML loading

**Estimated Time:** 4 hours / 4時間

#### Step 1.2: Update JobGenerator / JobGenerator更新
**Files:** `src/services/job_generator.py`

**Changes:**
```python
class JobGenerator:
    def __init__(self, template_dir, output_base_dir, lattice_file=None):
        # ... existing code ...
        self.lattice_library = LatticeLibrary(lattice_file)

    def generate_java_from_template(self, job_dir, params):
        # Get lattice structure
        lattice_type = params.get('lattice_type', 'fcc')
        lattice = self.lattice_library.get_lattice(lattice_type)

        # Calculate absolute bond distances
        lconst = params['lattice_constant']
        d_min, d_max = lattice.bond_distance.get_absolute_range(lconst)

        # Pass to template
        template_vars = {
            **params,
            'lattice_atoms': lattice.atoms,
            'lattice_d_min': d_min,
            'lattice_d_max': d_max,
        }

        # ... rest of template rendering ...
```

**Tasks:**
- [ ] Add `LatticeLibrary` initialization
- [ ] Update template variable preparation
- [ ] Handle lattice loading errors
- [ ] Add logging

**Estimated Time:** 3 hours / 3時間

#### Step 1.3: Update Template / テンプレート更新
**Files:** `templates/simulation.java.j2`

**Tasks:**
- [ ] Update `getLatticeTypeConfig` to use template variables
- [ ] Remove hardcoded lattice definitions (keep as fallback)
- [ ] Test template rendering

**Estimated Time:** 2 hours / 2時間

### Phase 2: Default Library / デフォルトライブラリ

#### Step 2.1: Create Default Lattice Library
**Files:** `data/lattices/builtin_lattices.yml`

```bash
mkdir -p data/lattices
```

**Tasks:**
- [ ] Create YAML file with builtin lattices
- [ ] Add comprehensive documentation
- [ ] Add example custom lattice

**Estimated Time:** 2 hours / 2時間

#### Step 2.2: Create User Template
**Files:** `data/lattices/custom_lattices_template.yml`

**Tasks:**
- [ ] Create template with examples
- [ ] Add inline documentation
- [ ] Provide copy-paste examples

**Estimated Time:** 1 hour / 1時間

### Phase 3: Documentation / ドキュメント

#### Step 3.1: User Guide
**Files:** `docs/lattice_structure_guide.md`

**Content:**
- How to define custom lattices / カスタム格子の定義方法
- YAML format reference / YAMLフォーマットリファレンス
- Examples and best practices / サンプルとベストプラクティス
- Troubleshooting / トラブルシューティング

**Estimated Time:** 3 hours / 3時間

#### Step 3.2: Update Existing Docs
**Files:** `docs/job_generator_guide.md`, `CLAUDE.md`

**Tasks:**
- [ ] Add lattice file parameter documentation
- [ ] Update examples
- [ ] Add migration notes

**Estimated Time:** 1 hour / 1時間

### Phase 4: Testing / テスト

#### Step 4.1: Unit Tests
**Files:** `tests/unit/test_lattice_structure.py`

**Test Cases:**
- [ ] Lattice structure validation
- [ ] YAML file loading
- [ ] Bond distance calculation
- [ ] Error handling
- [ ] Builtin vs custom priority

**Estimated Time:** 4 hours / 4時間

#### Step 4.2: Integration Tests
**Files:** `tests/integration/test_job_generation_with_lattice.py`

**Test Cases:**
- [ ] Job generation with builtin lattices
- [ ] Job generation with custom lattices
- [ ] Invalid lattice handling
- [ ] Backward compatibility

**Estimated Time:** 3 hours / 3時間

---

## Migration Strategy / マイグレーション戦略

### Backward Compatibility / 後方互換性

**Approach:** Gradual migration with dual support
**アプローチ:** デュアルサポートによる段階的移行

#### Stage 1: Introduce Feature (v1.1.0)
- Add lattice library support
- Keep hardcoded lattices as default
- Optional lattice file parameter

**Status:** Both old and new methods work
**状態:** 旧方式と新方式の両方が動作

#### Stage 2: Encourage Migration (v1.2.0)
- Mark hardcoded approach as deprecated in docs
- Provide migration examples
- Add warnings for hardcoded usage

**Status:** Old method deprecated, new method recommended
**状態:** 旧方式は非推奨、新方式を推奨

#### Stage 3: Remove Hardcoded (v2.0.0)
- Remove hardcoded lattice types from template
- Require lattice library
- Builtin lattices moved to YAML file

**Status:** Only lattice library supported
**状態:** 格子ライブラリのみサポート

### Migration Examples / 移行例

#### Before / 以前
```python
from src.services import JobGenerator

generator = JobGenerator(
    template_dir=Path('templates'),
    output_base_dir=Path('jobs/comsol')
)

params = {
    'lattice_type': 'fcc',  # Hardcoded type
    'lattice_constant': 1.0,
    # ...
}

result = generator.generate_job(params)
```

#### After / 以後
```python
from src.services import JobGenerator

generator = JobGenerator(
    template_dir=Path('templates'),
    output_base_dir=Path('jobs/comsol'),
    lattice_file=Path('data/lattices/my_custom_lattices.yml')  # NEW
)

params = {
    'lattice_type': 'custom_hex',  # Can be custom or builtin
    'lattice_constant': 1.0,
    # ...
}

result = generator.generate_job(params)
```

---

## Testing Strategy / テスト戦略

### Test Coverage Goals / テストカバレッジ目標

- Unit tests: > 90% / ユニットテスト: 90%以上
- Integration tests: All critical paths / 統合テスト: すべての重要パス
- End-to-end: Major use cases / E2Eテスト: 主要ユースケース

### Test Data / テストデータ

```yaml
# tests/fixtures/test_lattices.yml
lattices:
  test_simple:
    name: "Test Simple"
    atoms:
      - [0.0, 0.0, 0.0]
    bond_distance:
      min_factor: 0.9
      max_factor: 1.1

  test_invalid_coords:
    name: "Invalid Coordinates"
    atoms:
      - [1.5, 0.0, 0.0]  # Invalid: > 1.0
    bond_distance:
      min_factor: 0.9
      max_factor: 1.1
```

### Test Scenarios / テストシナリオ

1. **Valid YAML loading** / 有効なYAMLの読み込み
2. **Invalid YAML handling** / 無効なYAMLの処理
3. **Coordinate validation** / 座標の検証
4. **Bond distance calculation** / ボンド距離の計算
5. **Custom vs builtin priority** / カスタムと組み込みの優先順位
6. **Template rendering with custom lattice** / カスタム格子でのテンプレートレンダリング
7. **Backward compatibility** / 後方互換性

---

## Timeline / スケジュール

### Development Schedule / 開発スケジュール

| Phase | Task | Estimated Time | Dependencies |
|-------|------|----------------|--------------|
| 1.1 | Data Models | 4 hours | - |
| 1.2 | JobGenerator Update | 3 hours | 1.1 |
| 1.3 | Template Update | 2 hours | 1.2 |
| 2.1 | Default Library | 2 hours | 1.1 |
| 2.2 | User Template | 1 hour | 2.1 |
| 3.1 | User Guide | 3 hours | 2.2 |
| 3.2 | Doc Updates | 1 hour | 3.1 |
| 4.1 | Unit Tests | 4 hours | 1.3 |
| 4.2 | Integration Tests | 3 hours | 4.1 |

**Total Estimated Time:** 23 hours / 合計見積時間: 23時間

**Suggested Sprint:** 1 week (with ~4 hours/day dedicated time)
**推奨スプリント:** 1週間（1日約4時間の専念時間）

---

## Risk Assessment / リスク評価

### Technical Risks / 技術リスク

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| YAML parsing errors | Medium | Medium | Comprehensive validation, clear error messages |
| Template rendering issues | Low | High | Extensive testing with various lattices |
| Performance degradation | Low | Low | Benchmark with large lattices |
| Backward compatibility break | Low | High | Thorough testing of existing code |

### User Adoption Risks / ユーザー採用リスク

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Learning curve too steep | Medium | Medium | Clear documentation, examples |
| Resistance to change | Low | Low | Maintain backward compatibility |
| Configuration errors | High | Medium | Validation, helpful error messages |

---

## Appendix / 付録

### A. Example Custom Lattice Files / カスタム格子ファイルの例

#### A.1: Hexagonal Close-Packed (HCP)

```yaml
# custom_hcp.yml
lattices:
  hcp:
    name: "Hexagonal Close-Packed"
    description: "HCP structure with a/c ratio"
    crystal_system: "hexagonal"
    atoms:
      - [0.0, 0.0, 0.0]
      - [0.333, 0.667, 0.5]
    bond_distance:
      min_factor: 0.95
      max_factor: 1.05
    metadata:
      c_over_a_ratio: 1.633
      coordination_number: 12
```

#### A.2: Perovskite Structure

```yaml
# custom_perovskite.yml
lattices:
  perovskite_abo3:
    name: "Perovskite ABO3"
    description: "Cubic perovskite structure"
    crystal_system: "cubic"
    atoms:
      # A-site (corner)
      - [0.0, 0.0, 0.0]
      # B-site (body center)
      - [0.5, 0.5, 0.5]
      # O-sites (face centers)
      - [0.5, 0.5, 0.0]
      - [0.5, 0.0, 0.5]
      - [0.0, 0.5, 0.5]
    bond_distance:
      min_factor: 0.35
      max_factor: 0.65
    metadata:
      formula: "ABO3"
      space_group: "Pm-3m"
```

### B. Configuration Examples / 設定例

#### B.1: Using Custom Lattice in Job Generation

```python
# Example script: examples/generate_hcp_job.py

from pathlib import Path
from src.services import JobGenerator

def main():
    # Initialize generator with custom lattice file
    generator = JobGenerator(
        template_dir=Path('templates'),
        output_base_dir=Path('jobs/comsol'),
        lattice_file=Path('data/lattices/custom_hcp.yml')
    )

    # Define job parameters
    params = {
        'lattice_type': 'hcp',  # From custom file
        'lattice_constant': 3.2,  # Angstroms
        'sphere_radius_ratio': 15,
        'bond_radius_ratio': 8,
        'num_cells': 3,
        'poisson_ratio': 30,
    }

    # Generate job
    result = generator.generate_job(params)
    print(f"Job created: {result['job_dir']}")

if __name__ == '__main__':
    main()
```

### C. Validation Rules / バリデーションルール

#### C.1: Coordinate Validation
- All coordinates must be in range [0.0, 1.0]
- At least one atom required
- Maximum 100 atoms per unit cell (performance limit)

#### C.2: Bond Distance Validation
- `min_factor` > 0
- `max_factor` > `min_factor`
- Recommended range: 0.1 < `min_factor` < 2.0

#### C.3: File Validation
- Valid YAML syntax
- Required fields present
- No duplicate lattice IDs

---

## Change Log / 変更履歴

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-19 | Claude Code | Initial draft |

---

## References / 参考文献

1. COMSOL Multiphysics API Reference
2. Jinja2 Template Documentation
3. PyYAML Documentation
4. International Tables for Crystallography

---

## Approval / 承認

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Author | Claude Code | - | 2025-11-19 |
| Reviewer | - | - | - |
| Approver | - | - | - |

---

**End of Document / 文書終わり**
