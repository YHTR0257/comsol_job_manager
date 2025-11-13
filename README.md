
# Project Overview

COMSOL Job Manager は、COMSOL Multiphysics を用いた格子構造の形状最適化を研究目的で自動化するツール群です。

テンプレート（Java / batch / YAML）を生成して Windows 側の COMSOL を実行し、結果を解析して PostgreSQL に記録します。

# Usage Instructions

## 環境要件

- **WSL (Windows Subsystem for Linux)**: Python実行環境
- **Windows**: COMSOL Multiphysics実行環境
- **Docker**: PostgreSQL等のサービス

## Installation

このプロジェクトは依存関係をコンテナで提供する設計のため、セットアップは Docker コンテナを起動するだけです。

```bash
# コンテナ起動（PostgreSQL 等）
docker compose -f docker/docker-compose.yml up -d
```

## 基本的な使い方

### 1. ジョブ生成

```python
from src.services import JobGenerator
from pathlib import Path

generator = JobGenerator(
    template_dir=Path("templates"),
    output_base_dir=Path("jobs/comsol")
)

params = {
    'lattice_constant': 1.0,
    'sphere_radius_ratio': 0.15,
    'bond_radius_ratio': 0.08,
    'num_cells': 3,
}

result = generator.generate_job(params)
print(f"Generated: {result['job_dir']}")
```

### 2. ジョブ実行（WSL環境）

```python
from src.services import execute_job

# ジョブディレクトリを指定して実行
result = execute_job("jobs/comsol/job_YYYYMMDD_HHMMSS", timeout=3600)

if result.returncode == 0:
    print("✓ Simulation completed successfully")
else:
    print(f"✗ Failed with code: {result.returncode}")
```

詳細な実行手順や `.env` の設定は `docs/user_guide.md` および `docs/batch_executor_guide.md` を参照してください。

# Development Setup

- 推奨 Python: 3.8+
- 開発フロー:
	1. 仮想環境を作成
	2. 依存インストール
	3. `src/` を編集、`pytest tests/` で確認
- 推奨ツール: `pytest`
- 使用データベース: PostgreSQL (Docker コンテナ内)
- 開発(Development) 環境では `docker/docker-compose.dev.yml` を使用
    - データベースはローカルホストのポート5432にマッピング
    - 自由にデータをリセット・変更可能
- 本番(Production) 環境では `docker/docker-compose.prod.yml` を使用
    - データベースは別コンテナで永続化
    - docker内のnetworkで接続

---


# Project Structure

- `docs/` — 設計書・ユーザーガイド（`docs/project_design.md` を参照）
- `docker/` — PostgreSQL、コンテナ設定
- `data/` — DB ボリュームやテンプレート、ログ
- `jobs/` — ジョブ単位のワークディレクトリ（`jobs/comsol/job_YYYYMMDD_HHMMSS/`）
- `src/` — アプリケーションコード
	- `src/services/`
        -  `job_generator.py`, `batch_executor.py`, `result_analyzer.py`
	- `src/optimizers/` — Optuna 実装等
	- `src/data/` — DB 接続・モデル
- `tests/` — 単体テスト
- `scripts/` — 補助スクリプト

# Where to find more

- **詳細設計**: `docs/project_design.md`
- **DB スキーマ**: `docs/database.md`
- **ジョブ生成**: `docs/job_generator_guide.md`
- **ジョブ実行**: `docs/batch_executor_guide.md`
- **ユーザー向け手順**: `docs/user_guide.md`
- **開発者ガイド**: `CLAUDE.md`

---

この README は短く要点をまとめたものです。細かい操作や設定は `docs/` 配下の各ドキュメントを参照してください。


Guidelines for contributing, code style, branches, and pull request process.


