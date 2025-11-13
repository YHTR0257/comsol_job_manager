# Batch Executor Usage Guide

このドキュメントでは、WSLからWindowsのCOMSOLバッチファイルを実行する`BatchExecutor`の使い方を説明します。

## 概要

`BatchExecutor`は、WSL（Windows Subsystem for Linux）環境からWindowsのバッチファイル（`.bat`）を実行するためのユーティリティです。COMSOL Multiphysicsシミュレーションジョブの実行に特化しています。

## 前提条件

- **WSL環境**: Windows上でWSL (Windows Subsystem for Linux) が動作していること
- **COMSOL**: Windows側にCOMSOL Multiphysicsがインストールされていること
- **PATH設定**: `comsol`コマンドがWindows環境変数PATHに設定されていること

## 基本的な使い方

### 1. 単一ジョブの実行

```python
from src.services import execute_job
from pathlib import Path

# ジョブディレクトリを指定して実行
job_dir = Path("jobs/comsol/job_20251113_011825")
result = execute_job(job_dir, timeout=3600)  # 1時間タイムアウト

# 実行結果を確認
print(f"Exit code: {result.returncode}")
print(f"STDOUT:\n{result.stdout}")
if result.returncode != 0:
    print(f"STDERR:\n{result.stderr}")
```

### 2. BatchExecutorクラスを使用

```python
from src.services import BatchExecutor
from pathlib import Path

# Executorの初期化
executor = BatchExecutor(timeout=3600)  # デフォルトタイムアウト: 1時間

# バッチファイルのパス
batch_file = Path("jobs/comsol/job_20251113_011825/run.bat")

# 実行（同期）
result = executor.execute_batch(batch_file)

# 結果の確認
if result.returncode == 0:
    print("✓ Simulation completed successfully")
else:
    print(f"✗ Simulation failed with code {result.returncode}")
```

### 3. 非同期実行

長時間実行されるシミュレーションを非同期で実行し、他の処理を並行して行う場合：

```python
from src.services import BatchExecutor
import time

executor = BatchExecutor()

# 非同期で開始
process = executor.execute_batch_async(batch_file)

print(f"Process started with PID: {process.pid}")

# 他の処理を実行しながら、プロセスの完了を待つ
while process.poll() is None:
    print("Simulation is still running...")
    time.sleep(60)  # 1分ごとにチェック

# 完了後、結果を取得
stdout, stderr = process.communicate()
print(f"Exit code: {process.returncode}")
print(f"Output:\n{stdout}")
```

## 完全なワークフロー例

ジョブの生成から実行、結果の確認まで：

```python
from src.services import JobGenerator, execute_job
from pathlib import Path

# 1. ジョブ生成
generator = JobGenerator(
    template_dir=Path("templates"),
    output_base_dir=Path("jobs/comsol")
)

params = {
    'lattice_constant': 1.0,
    'sphere_radius_ratio': 0.15,
    'bond_radius_ratio': 0.08,
    'num_cells': 3,
    'poisson_ratio': 0.3,
    'file_name': 'fcc_lattice_test',
}

result = generator.generate_job(params, comsol_command="comsol")
job_dir = result['job_dir']

print(f"Generated job: {job_dir}")

# 2. ジョブ実行
print("Starting COMSOL simulation...")
exec_result = execute_job(job_dir, timeout=7200)  # 2時間タイムアウト

# 3. 結果確認
if exec_result.returncode == 0:
    print("✓ Simulation completed successfully")

    # 結果ファイルを確認
    results_dir = job_dir / "results"
    kirchhoff_file = results_dir / f"{params['file_name']}_kirchhoff.txt"
    maxmises_file = results_dir / f"{params['file_name']}_maxmises.txt"

    if kirchhoff_file.exists():
        print(f"✓ Kirchhoff stress data: {kirchhoff_file}")

    if maxmises_file.exists():
        print(f"✓ Max mises stress data: {maxmises_file}")
else:
    print(f"✗ Simulation failed with exit code: {exec_result.returncode}")

    # ログを確認
    log_file = job_dir / "results" / "run.log"
    if log_file.exists():
        with open(log_file, 'r') as f:
            print(f"\nLog file contents:\n{f.read()}")
```

## パラメトリックスタディの実行

複数のジョブを順次実行：

```python
from src.services import JobGenerator, execute_job
from pathlib import Path
import pandas as pd

generator = JobGenerator(
    template_dir=Path("templates"),
    output_base_dir=Path("jobs/comsol")
)

# パラメータスイープ
sphere_radii = [0.10, 0.15, 0.20]
bond_radii = [0.05, 0.08, 0.10]

results_data = []

for rs in sphere_radii:
    for rb in bond_radii:
        # ジョブ生成
        params = {
            'lattice_constant': 1.0,
            'sphere_radius_ratio': rs,
            'bond_radius_ratio': rb,
            'num_cells': 3,
            'file_name': f'fcc_rs{int(rs*100)}_rb{int(rb*100)}',
        }

        job_result = generator.generate_job(params)
        job_dir = job_result['job_dir']

        print(f"\nRunning: rs={rs:.2f}, rb={rb:.2f}")

        # ジョブ実行
        exec_result = execute_job(job_dir, timeout=7200)

        # 結果を記録
        results_data.append({
            'job_id': job_dir.name,
            'sphere_radius': rs,
            'bond_radius': rb,
            'exit_code': exec_result.returncode,
            'success': exec_result.returncode == 0
        })

        if exec_result.returncode == 0:
            print(f"  ✓ Success")
        else:
            print(f"  ✗ Failed (code: {exec_result.returncode})")

# 結果をDataFrameに
df = pd.DataFrame(results_data)
print("\n" + "="*60)
print("Parametric Study Results:")
print(df)

# CSVに保存
df.to_csv("jobs/comsol/parametric_study_results.csv", index=False)
```

## 環境検出

`BatchExecutor`は自動的にWSL環境を検出します：

```python
from src.services import BatchExecutor

executor = BatchExecutor()

if executor.is_wsl:
    print("✓ Running in WSL environment")
    print("  Windows batch files can be executed")
else:
    print("⚠ Not running in WSL")
    print("  Batch execution may not work")
```

## パス変換

WSLパスとWindowsパスの変換：

```python
from src.services import BatchExecutor
from pathlib import Path

executor = BatchExecutor()

# WSLパス → Windowsパス
wsl_path = Path("/workspace/jobs/comsol/job_XXX/run.bat")
windows_path = executor.convert_wsl_to_windows_path(wsl_path)

print(f"WSL path: {wsl_path}")
print(f"Windows path: {windows_path}")
# 例: \\wsl$\Ubuntu\workspace\jobs\comsol\job_XXX\run.bat
#     または C:\Users\...\workspace\jobs\comsol\job_XXX\run.bat
```

## COMSOLの確認

COMSOLがWindows PATHに設定されているか確認：

```python
from src.services import BatchExecutor

executor = BatchExecutor()

if executor.check_comsol_available():
    print("✓ COMSOL is available")
else:
    print("✗ COMSOL not found in Windows PATH")
    print("  Please add COMSOL to Windows PATH")
```

## エラーハンドリング

```python
from src.services import BatchExecutor, BatchExecutionError
import subprocess

executor = BatchExecutor(timeout=3600)

try:
    result = executor.execute_batch(batch_file)

    if result.returncode == 0:
        print("Success")
    else:
        print(f"Job failed with exit code: {result.returncode}")
        print(f"Error output:\n{result.stderr}")

except subprocess.TimeoutExpired:
    print("Error: Simulation timed out after 1 hour")

except BatchExecutionError as e:
    print(f"Error: {e}")

except FileNotFoundError:
    print("Error: Batch file or cmd.exe not found")
```

## タイムアウト設定

シミュレーションの規模に応じてタイムアウトを調整：

```python
from src.services import execute_job

# 小規模シミュレーション: 30分
execute_job(job_dir, timeout=1800)

# 中規模シミュレーション: 2時間
execute_job(job_dir, timeout=7200)

# 大規模シミュレーション: 24時間
execute_job(job_dir, timeout=86400)
```

## トラブルシューティング

### エラー: cmd.exe not found

**原因:** WSL環境ではない、またはWSLが正しく設定されていません。

**解決策:**
- Windowsで`wsl --version`を実行してWSLが有効か確認
- WSLディストリビューション（Ubuntu等）を再インストール

### エラー: COMSOL command not found

**原因:** COMSOLがWindows環境変数PATHに設定されていません。

**解決策:**
1. Windowsで「環境変数の編集」を開く
2. システム環境変数の`Path`に以下を追加:
   ```
   C:\Program Files\COMSOL\COMSOL61\Multiphysics\bin\win64
   ```
3. コマンドプロンプトで確認:
   ```cmd
   where comsol
   ```

### エラー: Timeout

**原因:** シミュレーションが指定時間内に完了しませんでした。

**解決策:**
- タイムアウト値を増やす
- パラメータ（`num_cells`等）を調整してシミュレーション規模を小さくする
- ログファイル（`results/run.log`）で進捗を確認

### パス関連のエラー

**原因:** WSLとWindowsのパスマッピングに問題があります。

**解決策:**
```python
# パス変換を明示的に無効化
executor = BatchExecutor()
result = executor.execute_batch(batch_file, convert_path=False)
```

## 本番環境での推奨設定

```python
import logging
from src.services import JobGenerator, execute_job, BatchExecutor
from src.config.loader import setup_logging, get_logger

# ロギング設定
setup_logging({
    'logging': {
        'level': 'INFO',
        'console': {'enabled': True},
        'file': {
            'enabled': True,
            'path': 'logs/comsol_execution.log',
            'rotation': {
                'max_bytes': 10485760,  # 10MB
                'backup_count': 5
            }
        }
    }
})

logger = get_logger("production")

# COMSOLの確認
executor = BatchExecutor(timeout=7200)
if not executor.check_comsol_available():
    logger.error("COMSOL not available - aborting")
    sys.exit(1)

# ジョブ生成と実行
# ... (上記の例を参照)
```

## 関連ドキュメント

- [Job Generator Guide](job_generator_guide.md) - ジョブ生成の詳細
- [Project Design](project_design.md) - 全体設計
- [CLAUDE.md](../CLAUDE.md) - 開発者向けガイド
