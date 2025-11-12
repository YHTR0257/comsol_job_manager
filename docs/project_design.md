# COMSOL Job Generator & Optimizer - Simplified Design Document

## 1. Project Purpose

このプロジェクトは、COMSOL Multiphysicsを用いた格子構造の形状最適化を自動化するための**研究用ツール**です。

### 1.1 主要目的
- **パラメトリックスタディの自動化**: 手動設定の手間を削減
- **結果の体系的な記録**: すべての試行パラメータと結果をデータベースに保存
- **再現性の確保**: 設定ファイルから完全な再実行が可能
- **WSL-Windows統合**: Linux開発環境とWindows COMSOL実行の連携

### 1.2 スコープ
- **含まれるもの**: ジョブ生成、逐次実行、結果解析、最適化ループ、データベース記録
- **含まれないもの**: 並列実行、Web UI、複雑なジョブキュー管理

### 1.3 想定利用規模
- 試行回数: 50〜500回程度
- 1試行の実行時間: 数分〜30分程度
- 同時実行ジョブ数: 1（逐次実行）

---

## 2. Architecture Overview

### 2.1 システムアーキテクチャ図

```
┌─────────────────────────────────────────────────────────┐
│              WSL / Linux Environment                    │
│           (Python Development & Execution)              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌────────────────────────────────────────────────────┐ │
│  │         Optimization Controller (main.py)          │ │
│  │  - 最適化ループ制御                                   │ │
│  │  - ジョブ生成 → 実行 → 解析の連続実行                   │ │
│  └────────────────────────────────────────────────────┘ │
│                         ↓↑                              │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │Job Generator│  │Batch Executor│  │Result        │    │
│  │- YAML生成    │  │- WSL→Windows │  │Analyzer       │     │
│  │- Java生成   │  │  実行        │  │- ファイル解析│  │
│  │- Batch生成  │  │- 同期待機    │  │- 剛性計算    │  │
│  └─────────────┘  └──────────────┘  └──────────────┘  │
│                         ↓↑                              │
│  ┌────────────────────────────────────────────────────┐ │
│  │      PostgreSQL Database (in Docker)               │ │
│  │  - trials: 試行履歴                                 │ │
│  │  - stiffness_matrices: 剛性行列                    │ │
│  └────────────────────────────────────────────────────┘ │
│                         ↓↑                              │
│  ┌────────────────────────────────────────────────────┐ │
│  │      Shared File System (H:/ drive)                │ │
│  │  jobs/job_YYYYMMDD_HHMMSS/  →  jobs/comsol/job_YYYYMMDD_HHMMSS/results/│ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
└─────────────────────────┬─────────────────────────────────┘
                          │ (cmd.exe execution)
                          ↓
┌─────────────────────────────────────────────────────────┐
│              Windows Environment                         │
│              (COMSOL Execution)                          │
├─────────────────────────────────────────────────────────┤
│  run.bat → comsol.exe → 結果出力                         │
└─────────────────────────────────────────────────────────┘
```

### 2.2 データフロー

```
[1] Optimizer → パラメータ提案
    ↓
[2] Job Generator → YAML/Java/Batch生成
    ↓
[3] Batch Executor → cmd.exe経由で実行（同期待機）
    ↓
[4] COMSOL → コンパイルして、計算実行
    ↓
[5] Result Analyzer → ファイル解析、剛性計算
    ↓
[6] Database → 結果保存、計算完了確認
    ↓
[7] Optimizer → 目的関数評価 → 次の試行へ
```

**重要な設計判断**: 
- ジョブキュー不要（1つずつ順次実行）
- 実行完了まで同期待機
- 状態管理簡素化

---

## 3. Directory Structure

```
comsol-optimizer/
├── README.md
├── .gitignore
├── .env.example
│
├── docker/
│   ├── docker-compose.yml            # PostgreSQLのみ
│   └── postgres/
│       └── init.sql
│
├── data/
│   ├── postgres/                     # DBボリューム
│   ├── templates/                    # テンプレートファイル
│   │   ├── config_template.yaml
│   │   ├── comsol_template.java.j2
│   │   └── run_template.bat.j2
│   └── logs/
│       └── optimization.log
│
├── docs/
│   ├── design.md                     # 本ドキュメント
│   ├── database.md                   # DB設計
│   └── user_guide.md                 # 使い方
│
├── src/
│   ├── __init__.py
│   ├── main.py                       # メインエントリーポイント
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── loader.py               # 設定管理
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── db.py               # DB接続
│   │   └── models               # ORMモデル
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── parameter.py              # パラメータ定義
│   │   └── simulation_config.py      # シミュレーション設定
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── job_generator.py          # ジョブファイル生成
│   │   ├── batch_executor.py         # バッチ実行
│   │   └── result_analyzer.py        # 結果解析
│   │
│   ├── optimizers/
│   │   ├── __init__.py
│   │   ├── base.py                   # 抽象基底クラス
│   │   └── optuna_optimizer.py       # Optuna実装
│   │
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── kirchhoff_parser.py
│   │   └── maxmises_parser.py
│   │
│   ├── visualize/
│   │  ├── __init__.py
│   │  └── plot_results.py            # 結果可視化
│   │
│   └── utils/
│       ├── __init__.py
│       ├── path_converter.py         # パス変換
│       └── logger.py                 # ロギング
│
├── scripts/
│   ├── setup_environment.py          # 初期セットアップ
│   ├── test_batch_execution.py       # バッチ実行テスト
│   └── visualize_results.py          # 結果可視化
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── unit/                         # ユニットテストのみ
│       ├── test_job_generator.py
│       ├── test_result_analyzer.py
│       └── test_parsers.py
│
├── .gitignore
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── README.md
└── pytest.ini
```

---

## 4. Component Responsibilities

### 4.1 Main Controller (main.py)

**責務**: 最適化ループ全体の制御

**フロー**:
1. 設定読み込み、データベース接続
2. 最適化エンジン初期化
3. パラメータ提案 → ジョブ生成 → 実行 → 解析 → 保存のループ
4. 最適解の抽出と表示

---

### 4.2 Job Generator

**責務**:
- Jinja2テンプレートからYAML/Java/Batch生成
- ジョブIDの生成（連番: job_001, job_002, ...）
- パラメータバリデーション

**入力**: パラメータ辞書（lattice_type, lattice_constant, sphere_radius_ratio等）

**出力**: 
- `jobs/comsol/job_YYYYMMDD_HHMMSS/config.yml`
- `jobs/comsol/job_YYYYMMDD_HHMMSS/simulation.java`
- `jobs/comsol/job_YYYYMMDD_HHMMSS/run.bat`

**設計方針**:
- テンプレート駆動（ロジックとデータの分離）
- シンプルなバリデーション（範囲チェックのみ）

---

### 4.3 Batch Executor

**責務**:
- WSLからWindows側のrun.batを実行
- **同期実行**（完了まで待機）
- パス変換（WSL → Windows）
- タイムアウト管理

**設計方針**:
- シンプル: 同期実行のみ、キュー管理不要
- ロバスト: タイムアウトとエラーハンドリング

---

### 4.4 Result Analyzer

**責務**:
- kirchhoff.txt, maxmises.txtのパース
- 剛性行列の計算
- 弾性定数の導出（ヤング率、ポアソン比等）
- 目的関数の評価

**入力**: `jobs/comsol/job_YYYYMMDD_HHMMSS/results/`内のファイル群

**出力**: 剛性行列、弾性定数、目的関数値の辞書

**設計方針**:
- ファイル解析に集中
- エラー時は例外を投げる（上位で処理）

---

### 4.5 Optuna Optimizer

**責務**:
- パラメータ探索空間の定義
- 次のパラメータ提案
- 試行結果の記録
- 最適解の抽出

**設計方針**:
- Optunaに最適化ロジックを任せる
- シンプルな目的関数定義
- 失敗した試行には最悪値を返す

---

## 5. Database Design

詳細は[database.md](database.md)を参照。

---

## 6. Configuration Management

### 6.1 設定ファイル構造

単一のYAML設定ファイル（`config.yml`）で管理

**主要セクション**:
- `comsol`: 実行ファイルパス、タイムアウト
- `paths`: ベースディレクトリ、ジョブ/結果ディレクトリ
- `optimization`: アルゴリズム、試行回数、探索空間定義
- `logging`: ログレベル、出力先
- `visualization`: プロット設定

**設計方針**:
- 単一ファイルで完結
- 環境変数で機密情報管理（`.env`ファイル）
- YAMLで可読性確保

---

## 7. Error Handling Strategy

### 7.1 エラー分類

**致命的エラー** → 即座に停止:
- データベース接続失敗
- テンプレートファイル不足
- COMSOLパス不正

**回復可能エラー** → ログ記録して次へ:
- ジョブ実行タイムアウト
- COMSOL収束失敗
- 結果ファイル解析エラー

### 7.2 設計方針
- 複雑な再試行ロジック不要
- 失敗は記録して次の試行へ
- 最適化アルゴリズムが自動的に失敗パラメータを避ける

---

## 8. Testing Strategy

### 8.1 ユニットテストのみ実装

**テスト対象**:
- `job_generator`: パラメータ → ファイル生成
- `result_analyzer`: ファイル → 剛性行列計算
- `parsers`: テキスト解析ロジック
- `path_converter`: WSL ↔ Windows パス変換

**テスト方針**:
- ファイル生成/解析ロジックの正確性を確認
- モックデータを使用

### 8.2 E2Eテスト
開発者が手動で実行して確認（自動化不要）

---

## 9. File System Design

### 9.1 ディレクトリ構造（H:ドライブ）

```
jobs/comsol/
└── job_YYYYMMDD_HHMMSS/
    ├── config.yml
    ├── simulation.java
    └── run.bat
    └── results/
        ├── kirchhoff.txt
        ├── maxmises.txt
        ├── run.log
        └── other_output_files.txt
```

### 9.2 ファイル命名規則

**Job ID**: `job_YYYYMMDD_HHMMSS` （タイムスタンプ形式）

**結果ファイル**:
- `kirchhoff.txt`: Kirchhoff応力データ
- `maxmises.txt`: 最大ミーゼス応力データ
- `run.log`: 実行ログ
- その他COMSOL出力ファイルはそのまま保存

### 9.3 設計方針
- シンプルな階層構造
- ジョブ完了後もファイルは保持（手動削除）
- 結果はDB優先、ファイルは参照用

---

## 10. Design Principles

### 10.1 SOLID原則の適用

**Single Responsibility**:
- 各コンポーネントは単一の責務のみ

**Open/Closed**:
- 新しいパーサー、最適化アルゴリズムの追加が容易

**Dependency Inversion**:
- 抽象に依存（`base.py`の抽象基底クラス）

### 10.2 その他の設計原則

- **KISS (Keep It Simple, Stupid)**: 過度な抽象化を避ける
- **YAGNI (You Aren't Gonna Need It)**: 将来の拡張は今実装しない
- **DRY (Don't Repeat Yourself)**: 共通処理はutils/に集約

---

## 11. Deployment

### 11.1 初期セットアップ手順

1. リポジトリクローン
2. Python仮想環境構築
3. 依存パッケージインストール
4. 環境変数設定（`.env`）
5. PostgreSQLコンテナ起動
6. データベース初期化
7. バッチ実行テスト

### 11.2 実行方法

設定ファイル指定実行モードのみで対応

config.ymlで設定を管理、以下のコマンドで最適化＋COMSOL計算開始:

```bash
python src/main.py --config path/to/config.yaml
```

---

## 12. Monitoring & Logging

### 12.1 ログ出力

**ログレベル**: DEBUG, INFO, WARNING, ERROR, CRITICAL

**出力先**: 
- コンソール（INFO以上）
- ファイル（DEBUG以上、ローテーション対応）

**ログ内容**:
- 試行開始/完了
- ジョブ生成/実行/解析の各フェーズ
- エラー詳細

### 12.2 設計方針
- シンプルなファイル出力
- 必要最低限のエラーハンドリング
- 複雑な監視システム不要（小規模研究用）

---

## 13. Appendix

### 13.1 用語集

- **RVE**: Representative Volume Element（代表体積要素）
- **剛性行列**: 応力-ひずみ関係を表す6×6対称行列
- **Compliance**: 柔軟性（剛性の逆数）
- **ベイズ最適化**: サンプル効率の高いブラックボックス最適化手法

### 13.2 関連ドキュメント

- `database.md`: データベーススキーマ詳細
- `user_guide.md`: 使用方法とチュートリアル

---

**Document Version**: 1.0  
**Last Updated**: 2025-01-12  
**Status**: Final