# 概要

- このドキュメントは、カスタム格子（Custom Lattice）機能の実装計画書
- カスタム格子を使用することで、ユーザーは独自の格子構造を定義し、シミュレーションや解析に利用することができる。

## 機能要件

- ユーザーがyamlを用いて、独自の格子構造体の弾性特性を計算できるようにジョブファイルを作成する
- カスタム格子の定義には、格子の幾何学的形状、材料特性、境界条件などを含む
- システムは、ユーザーが定義したカスタム格子を読み込み、解析を実行できる
- カスタム格子の解析結果は、標準的なフォーマットで出力され、他のツールと連携可能
    - 後に実装する予定の可視化ツールでの表示を考慮したフォーマット

必要な弾性特性
- 弾性コンプライアンス定数

弾性コンプライアンス定数から導出される定数群
- ヤング率(方向別)
- ポアソン比(方向別)
- せん断弾性率(方向別)
- 体積弾性率
- その他、必要に応じて追加可能

## 非機能要件

- システム自体のパフォーマンス要件は最低限
- 動作が安定すれば良いため、最低限のエラーハンドリングを実装する
- UIはCLIのみで実行する。
- ドキュメントは日本語で提供。ユーザーマニュアルとAPIドキュメントを含む。

## API設計

## 運用ステップ

**STEP1 : ユーザーは、カスタム格子の定義を含むyamlジョブファイルを作成する**
- カスタム格子の定義には、以下の情報を含む
    - 格子のジオメトリ
        - sphereの半径
        - beamの太さ
        - sphereの配置座標
        - beamの接続情報(どの球を繋いでいるか、端点を指定)
    - 材料特性（例：ヤング率、ポアソン比など）
    - 境界条件（例：固定端、荷重条件など）

**STEP2 : comsol_job_managerは、ジョブファイルを読み込み、カスタム格子の定義を解析(parse)する**
エラーハンドリング
- 想定していないフォーマットや変数が含まれていないか
- ジオメトリとして定義できる形になっているか

**STEP3 : comsol_job_managerは、解析されたカスタム格子の定義とjinja2テンプレートを用いて、シミュレーション入力ファイルを生成する**

フォルダ構造
```bash
run_YYYYMMDD_HHMMSS/
    |-- metadata.yml  # ジョブのメタデータ
    |-- structure.stl # COMSOLの機能で出力されるカスタム格子のSTLファイル 
    |-- preview.gif # COMSOLの機能で出力されるカスタム格子のプレビューGIFファイル
    |-- run.bat  # シミュレーション実行用バッチファイル
    |--job_001/
    |    |-- job_001.java # comsol_job_managerで生成したCOMSOL コンパイル対象のシミュレーションファイル
    |    |-- job_001.mph  # COMSOLシミュレーション入力ファイル
    |    |-- elastic_constants.csv  # 抽出された弾性特性のCSVファイル
    |    |-- results.yml
    |--job_002/
         |-- job_002.mph  # COMSOLシミュレーション入力ファイル
         |-- elastic_constants.csv  # 抽出された弾性特性のCSVファイル
```

出力情報
- どの程度のジョブファイルを生成したか

テスト要件
- parseは正常に動作しているか
- 生成されたシミュレーション入力ファイルが正しいか

**STEP4 : ユーザーは生成されたシミュレーション入力ファイルを確認する**

確認は手動で行う
- ジオメトリが正しく生成されているか
    - 球同士が重なっていないか
    - ビームと球が離れている部分はないか(2つの球の距離-2つの球の半径<ビームの長さ)
- 材料特性や境界条件が正しく反映されているか

**STEP5 : ユーザーは、スクリプトを実行してシミュレーションを開始する**

`scripts/run_comsol_simulation.py --job_dir run_YYYYMMDD_HHMMSS`で実行する
**STEP6 : COMSOLはシミュレーションを実行し、結果を出力する**
COMSOL compilerでコンパイル、comsol batchでシミュレーションを実行する
gifファイルとstlファイルの出力

**STEP7 : comsol_job_managerは、シミュレーション結果を解析し、必要な弾性特性を抽出する**
pythonの外回りプログラムを用いて、COMSOLの結果ファイルから弾性コンプライアンス定数を読み込む
読み込み対象
- COMSOLで出力された `p0_kirchhoff.txt` ファイル
    - 応力成分とひずみ成分が含まれている
弾性コンプライアンス定数の計算
- 応力-ひずみデータを用いて、弾性コンプライアンス定数を計算する
- 必要に応じて、ヤング率、ポアソン比、せん断弾性率、体積弾性率などの導出も行う

**STEP8 : comsol_job_managerは、抽出された弾性特性を標準フォーマットで出力する**

各jobごとの結果と、パラメトリックスタディでの結果をまとめた結果を出力する

まとめファイル
パラメトリックスタディ結果 `results_parametric_study.csv`
- 弾性コンプライアンステンソル(cijの21成分)
- パラメトリックスタディでのパラメータ名、値

各jobごとの結果
出力フォーマット
- datファイル
- yamlファイル

**STEP9 : ユーザーは、出力された弾性特性を確認し、必要に応じて他のツールで利用する**


# 機能詳細

yamlジョブファイルのフォーマット例

```yaml
job:
  name: "Custom Lattice Simulation"
  description: "Simulation of a custom lattice structure"
  scale:
    length: 1e-3  # 長さのスケール (m)
    force: 1e-3   # 力のスケール (N)
  parametric:
    default:
      sphere.radius: 0.2
      beam.thickness: 0.1
    sweep1:
      parameter: "sphere.radius"
      values: [0.1, 0.2, 0.3]
    sweep2:
      parameter: "beam.thickness"
      values: [0.05, 0.1]

geometry:
  lattice_vector:
    - [2, 0, 0]
    - [0, 2, 0]
    - [0, 0, 2]
  sphere:
  - id: 1
    radius: 0.5
    position: [0, 0, 0]
  - id: 2
    radius: 0.5
    position: [1, 0, 0]
  beam:
  - id: 1
    endpoints: [1, 2]
    thickness: 0.1

mesh:
  size: 5  # メッシュ要素の細かさ
  type: "FreeTri" # メッシュタイプ、例: FreeTri, FreeQuadなど

materials:
  material_1:
    name: "mat1"
    youngs_modulus: 200e9  # ヤング率 (Pa)
    poissons_ratio: 0.3  # ポアソン比
    density: 960
study:
  parametic_sweep:
    strain:
      delta: 0.01
      range: [0.0, 0.05]
  boundary_conditions:
    fixed : true
    copyface: true
```

## 注意点

- カスタム格子の定義は、ユーザーが正確に行う必要があるため、ドキュメントで詳細なガイドラインを提供する
- COMSOLでは、yamlの読み込みに対応していないため、jinja2テンプレートを用いてシミュレーション実行ファイルにハードコードする
- シミュレーションの精度は、ユーザーが定義した格子構造と材料特性に依存するため、注意喚起を行う
- 将来的に、可視化ツールとの連携を考慮し、出力フォーマットはcsv, dat, yamlの3パターンで出力できるように実装する

---

# 実装計画書

## 1. 実装の全体方針

### 1.1 既存システムとの統合

既存の `JobGenerator` をリファクタリングして、カスタム格子機能に対応する。
- 既存機能(FCC/BCC格子のパラメトリックスタディ)は維持
- カスタム格子機能を新しいモードとして追加
- テンプレートシステム(Jinja2)を活用し、柔軟な拡張を可能にする

### 1.2 アーキテクチャ設計

```
ユーザー入力YAML
    ↓
YAMLパーサー(validation + parsing)
    ↓
ParametricStudyGenerator (パラメトリックスイープ展開)
    ↓
JobGenerator (リファクタリング版)
    ├── CustomLatticeGeometryBuilder
    ├── Jinja2テンプレートエンジン
    └── ファイル生成(Java, Batch, Config)
    ↓
BatchExecutor (既存)
    ↓
結果解析・出力
```

## 2. 実装タスク一覧

### Phase 1: YAMLパーサーとバリデーション (STEP1-2)

**タスク1.1: カスタム格子YAML定義モデルの作成**
- ファイル: `src/data/models/custom_lattice.py` (新規作成)
- 内容:
  - Pydanticを使用したYAMLスキーマ定義
  - データクラス: `CustomLatticeJob`, `Geometry`, `Sphere`, `Beam`, `Material`, `Study`
  - バリデーション機能の実装
    - 必須フィールドチェック
    - 値の範囲チェック(radius > 0, thickness > 0など)
    - sphere IDの重複チェック
    - beam endpoints参照の整合性チェック

**タスク1.2: ジオメトリバリデーターの実装**
- ファイル: `src/validators/geometry_validator.py` (新規作成)
- 内容:
  - 球同士の重なりチェック
    - 2つの球の中心間距離 > 半径の和
  - ビームと球の接続チェック
    - 球の中心間距離 - 2×球の半径 ≒ ビームの長さ(許容誤差あり)
  - 格子ベクトルの正当性チェック(周期境界条件用)
  - 詳細なエラーメッセージの生成

**タスク1.3: YAMLローダーの実装**
- ファイル: `src/parsers/yaml_loader.py` (新規作成)
- 内容:
  - YAMLファイルの読み込み
  - Pydanticモデルへのパース
  - バリデーションエラーのハンドリングとユーザーフレンドリーなエラー表示

### Phase 2: パラメトリックスタディ展開 (STEP3の準備)

**タスク2.1: パラメトリックスイープジェネレーターの実装**
- ファイル: `src/services/parametric_generator.py` (新規作成)
- 内容:
  - パラメトリックスイープの組み合わせ展開
    - 例: sweep1=[0.1, 0.2, 0.3], sweep2=[0.05, 0.1] → 6通りのパラメータセット生成
  - デフォルト値の適用
  - 各ジョブへのパラメータ割り当て
  - ジョブID生成: `job_001`, `job_002`, ..., `job_NNN`

### Phase 3: JobGeneratorのリファクタリング (STEP3)

**タスク3.1: JobGeneratorの機能分離**
- ファイル: `src/services/job_generator.py` (リファクタリング)
- 内容:
  - 既存のFCC/BCC格子生成ロジックを `StandardLatticeMode` として分離
  - カスタム格子生成ロジックを `CustomLatticeMode` として追加
  - 共通インターフェース `LatticeMode` を定義
  - `generate_job()` でモード選択を可能にする

**タスク3.2: カスタム格子ジオメトリビルダーの実装**
- ファイル: `src/services/geometry_builder.py` (新規作成)
- 内容:
  - YAMLから読み込んだsphere/beam情報をCOMSOL Java API用のデータ構造に変換
  - 座標変換・スケーリング処理
  - 周期境界条件用の格子ベクトル処理

**タスク3.3: カスタム格子用Jinja2テンプレートの作成**
- ファイル: `templates/custom_lattice.java.j2` (新規作成)
- 内容:
  - sphere/beamのジオメトリ生成コード
  - パラメトリックスタディ対応のCOMSOL Java API呼び出し
  - メッシュ生成、境界条件、材料特性の設定
  - 結果出力(kirchhoff.txt, STL, GIF)の実装

**タスク3.4: metadata.ymlの生成**
- ファイル: `src/services/job_generator.py` (拡張)
- 内容:
  - ジョブディレクトリ直下に `metadata.yml` を生成
  - 含む情報: job_id, 生成日時, 入力パラメータ, パラメトリックスタディ設定

### Phase 4: 結果解析と出力 (STEP7-8)

**タスク4.1: kirchhoff.txt パーサーの拡張**
- ファイル: `src/parsers/kirchhoff_parser.py` (既存の拡張)
- 内容:
  - `p0_kirchhoff.txt` から応力-ひずみデータを読み込み
  - 弾性スティフネステンソル C_ij の計算(21成分)
  - 弾性コンプライアンステンソル S_ij の計算(C_ijの逆行列)

**タスク4.2: 弾性特性計算モジュールの実装**
- ファイル: `src/services/elastic_properties.py` (新規作成)
- 内容:
  - ヤング率(方向別)の計算
  - ポアソン比(方向別)の計算
  - せん断弾性率(方向別)の計算
  - 体積弾性率の計算

**タスク4.3: 結果出力フォーマッターの実装**
- ファイル: `src/services/result_formatter.py` (新規作成)
- 内容:
  - 各ジョブ個別の結果出力
    - `elastic_constants.dat` (固定幅フォーマット)
    - `results.yml` (YAML形式)
  - パラメトリックスタディまとめ出力
    - `results_parametric_study.csv` (全ジョブの結果を1つのCSVにまとめる)
    - 列: job_id, parameter_name, parameter_value, c11, c12, ..., c66, s11, s12, ..., s66

**タスク4.4: 結果解析サービスの実装**
- ファイル: `src/services/result_analyzer.py` (既存の拡張またはカスタム格子対応)
- 内容:
  - ジョブディレクトリから結果ファイルを読み込み
  - kirchhoff_parserを使って弾性テンソルを計算
  - elastic_propertiesを使って各種弾性特性を計算
  - result_formatterを使って出力ファイルを生成
  - 複数ジョブの結果を集約してパラメトリックスタディ結果を生成
  - **コアロジック**:
    - `analyze_single_job(job_dir)` - 単一ジョブの解析
    - `analyze_parametric_study(run_dir)` - パラメトリックスタディ全体の解析
    - `generate_summary_report(run_dir)` - サマリーレポート生成

### Phase 5: CLIインターフェースの実装 (STEP1, STEP5)

**タスク5.1: ジョブ生成スクリプトの作成**
- ファイル: `scripts/generate_custom_lattice_job.py` (新規作成)
- **役割**: CLIインターフェース(薄いラッパー)
- 内容:
  - コマンドライン引数のパース: `--input job.yml --output jobs/comsol`
  - `src.parsers.yml_loader` を呼び出してYAMLを読み込み
  - `src.services.JobGenerator` を呼び出してジョブ生成
  - 生成されたジョブの情報を表示(標準出力)
  - エラーハンドリングとユーザーへのメッセージ表示
  - **実装ポイント**: ビジネスロジックは含めず、`src`モジュールの呼び出しに徹する

**タスク5.2: 既存のジョブ実行スクリプトの拡張**
- ファイル: `scripts/test_job_executor.py` (拡張)
- **役割**: CLIインターフェース(薄いラッパー)
- 内容:
  - カスタム格子ジョブの実行に対応(既存の`BatchExecutor`を使用)
  - 既存機能(--latest, --list)はそのまま維持
  - **実装ポイント**: ビジネスロジックは`src.services.batch_executor`に任せる

**タスク5.3: 結果解析スクリプトの作成**
- ファイル: `scripts/analyze_custom_lattice_results.py` (新規作成)
- **役割**: CLIインターフェース(薄いラッパー)
- 内容:
  - コマンドライン引数のパース: `--run_dir run_YYYYMMDD_HHMMSS`
  - `src.services.result_analyzer.analyze_parametric_study()` を呼び出し
  - 解析結果のサマリーを表示(標準出力)
  - エラーハンドリングとユーザーへのメッセージ表示
  - **実装ポイント**: 解析ロジックは`src.services.result_analyzer`に実装し、スクリプトは呼び出しのみ

### Phase 6: テストとドキュメント

**タスク6.1: ユニットテストの作成**
- ファイル: `tests/unit/test_custom_lattice_parser.py` (新規作成)
- ファイル: `tests/unit/test_geometry_validator.py` (新規作成)
- ファイル: `tests/unit/test_parametric_generator.py` (新規作成)
- 内容:
  - YAMLパースのテスト(正常系・異常系)
  - ジオメトリバリデーションのテスト
  - パラメトリックスイープ展開のテスト

**タスク6.2: 統合テストの作成**
- ファイル: `tests/integration/test_custom_lattice_workflow.py` (新規作成)
- 内容:
  - YAML入力 → ジョブ生成 → ファイル確認の一連のフロー
  - モックCOMSOL出力を使った結果解析テスト

**タスク6.3: ユーザーマニュアルの作成**
- ファイル: `docs/user_guide_custom_lattice.md` (新規作成)
- 内容:
  - カスタム格子の定義方法(YAML記述例)
  - ジョブ生成から実行、結果確認までの手順
  - トラブルシューティング

## 3. ファイル構成

### 新規作成ファイル

```
src/                                   ← ビジネスロジック・コアロジック
├── data/
│   └── models/
│       └── custom_lattice.py          # Pydanticモデル定義
├── validators/
│   └── geometry_validator.py          # ジオメトリ検証ロジック
├── parsers/
│   └── yaml_loader.py                 # YAMLローダー
├── services/
│   ├── parametric_generator.py        # パラメトリックスイープ展開
│   ├── geometry_builder.py            # カスタム格子ジオメトリビルダー
│   ├── elastic_properties.py          # 弾性特性計算
│   └── result_formatter.py            # 結果出力フォーマッター
└── ...

templates/
└── custom_lattice.java.j2             # カスタム格子用Javaテンプレート

scripts/                               ← CLIインターフェース(薄いラッパー)
├── generate_custom_lattice_job.py     # ジョブ生成CLI(srcへの呼び出しのみ)
└── analyze_custom_lattice_results.py  # 結果解析CLI(srcへの呼び出しのみ)

tests/
├── unit/
│   ├── test_custom_lattice_parser.py
│   ├── test_geometry_validator.py
│   ├── test_parametric_generator.py
│   ├── test_result_analyzer.py        # result_analyzerのテスト
│   └── test_elastic_properties.py     # elastic_propertiesのテスト
└── integration/
    └── test_custom_lattice_workflow.py

docs/
└── user_guide_custom_lattice.md       # ユーザーマニュアル
```

### 変更ファイル

```
src/services/job_generator.py          # リファクタリング(モード分離)
src/services/result_analyzer.py        # 拡張(カスタム格子対応)
src/parsers/kirchhoff_parser.py        # 拡張(カスタム格子対応)
scripts/test_job_executor.py           # 拡張(カスタム格子対応、srcへの呼び出しのみ)
```

## 4. 実装順序

**Week 1-2: Phase 1, 2**
- YAMLパーサー、バリデーション、パラメトリックスイープ
- テスト用ファイルの整備
- テスト用環境の整備
    - テスト用フォルダの指定、モックファイルの準備

**Week 3-4: Phase 3**
- JobGeneratorリファクタリング、ジオメトリビルダー、テンプレート作成

**Week 5: Phase 4**
- 結果解析と出力フォーマッター

**Week 6: Phase 5, 6**
- CLIスクリプト、テスト、ドキュメント

## 5. 技術スタック

- **言語**: Python 3.10+
- **バリデーション**: Pydantic 2.x
- **テンプレート**: Jinja2
- **テスト**: pytest
- **YAML処理**: PyYAML
- **数値計算**: NumPy (弾性テンソル計算用)

## 6. リスクと対策

| リスク | 対策 |
|--------|------|
| COMSOLのジオメトリAPI仕様が不明 | 既存の`simulation.java.j2`を参考にし、段階的に実装 |
| パラメトリックスイープの組み合わせ爆発 | ジョブ数の上限設定(警告表示) |
| ユーザーの不正なYAML入力 | Pydanticによる厳格なバリデーション、詳細なエラーメッセージ |
| 既存機能の破壊 | 既存のテストケースを維持、リファクタリング時に回帰テスト実行 |

## 7. 成功基準

- [ ] YAMLファイルからジョブファイルが正常に生成できる
- [ ] パラメトリックスイープで複数ジョブが生成できる
- [ ] ジオメトリバリデーションが正しく動作する
- [ ] 生成されたCOMSOL Javaファイルがコンパイル・実行できる
- [ ] 弾性特性が正しく抽出され、CSV/YAML/DATで出力できる
- [ ] 既存のFCC/BCC格子機能が引き続き動作する
- [ ] ユニットテストカバレッジ80%以上
- [ ] ユーザーマニュアルが完備されている

## 8. 補足事項

### 8.1 格子ベクトルの扱い

周期境界条件(Periodic Boundary Condition, PBC)が有効な場合:
- `lattice_vector` で定義された3つのベクトルが単位格子を構成
- COMSOL側で対向する面をコピー(copyface)する設定を適用

### 8.2 弾性テンソルの記法

- **スティフネステンソル**: C_ij (応力 = C_ij × ひずみ)
- **コンプライアンステンソル**: S_ij (ひずみ = S_ij × 応力, C_ijの逆行列)
- 出力ファイルには両方を含める

### 8.3 既存JobGeneratorとの統合イメージ

```python
# 使用例(srcモジュール内での使用)
from src.services import JobGenerator
from src.parsers import yaml_loader
from src.services import result_analyzer

# 既存機能(FCC格子)
generator = JobGenerator(template_dir='templates', output_base_dir='jobs/comsol')
result = generator.generate_job(params={'lattice_constant': 1.0, 'lattice_type': 'fcc'})

# 新機能(カスタム格子) - srcモジュールで実装
custom_lattice_data = yaml_loader.load_custom_lattice_yaml('custom_lattice.yml')
result = generator.generate_job_from_yaml(custom_lattice_data)

# 結果解析(srcモジュールで実装)
analysis_result = result_analyzer.analyze_parametric_study('run_20251130_120000')
```

### 8.4 責任分離の原則

**`src/` モジュール(ビジネスロジック層)**
- データの読み込み・解析・変換
- ジオメトリ検証・バリデーション
- ジョブファイル生成
- COMSOL結果の解析と弾性特性計算
- ファイル出力フォーマット生成
- **すべてのコアロジックはここに実装**

**`scripts/` (インターフェース層)**
- コマンドライン引数のパース
- `src/`モジュールの関数・クラスの呼び出し
- 標準出力への結果表示
- エラーメッセージの表示
- **薄いラッパーとして実装し、ロジックは含めない**

この分離により:
- `src/`モジュールは単体テスト可能
- `scripts/`を変更せずに`src/`の機能を他から利用可能
- ビジネスロジックの再利用性が向上