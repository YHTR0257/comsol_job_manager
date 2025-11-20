# WSL-Windows Path Conversion Guide

WSL (Windows Subsystem for Linux) 環境では、LinuxパスとWindowsパスの変換が必要になります。本プロジェクトでは `src.utils.path_utils` モジュールがこの機能を提供します。

## 概要

WSLからWindowsアプリケーション（COMSOL等）を実行する際、パスの形式が異なるため変換が必要です:

- **WSLパス**: `/home/user/project/data.txt` または `/mnt/c/Users/user/data.txt`
- **Windowsパス**: `C:\Users\user\data.txt` または `\\wsl.localhost\Ubuntu\home\user\...`

## 主な機能

### 1. WSL環境の検出

```python
from src.utils import detect_wsl

if detect_wsl():
    print("WSL環境で実行中")
else:
    print("通常のLinuxまたはWindows環境")
```

**検出方法:**
- `/proc/version` ファイルに `microsoft` または `wsl` が含まれているか確認
- `wslpath` コマンドが利用可能か確認

### 2. WSLパス → Windowsパス変換

```python
from src.utils import wsl_to_windows_path

# 文字列パス
wsl_path = '/home/user/project/data.txt'
windows_path = wsl_to_windows_path(wsl_path)
print(windows_path)
# 出力例: \\wsl.localhost\Ubuntu-22.04\home\user\project\data.txt

# Pathオブジェクト
from pathlib import Path
wsl_path = Path('/mnt/c/Users/user/data.txt')
windows_path = wsl_to_windows_path(wsl_path)
print(windows_path)
# 出力例: C:\Users\user\data.txt
```

### 3. Windowsパス → WSLパス変換

```python
from src.utils import windows_to_wsl_path

windows_path = 'C:\\Users\\user\\data.txt'
wsl_path = windows_to_wsl_path(windows_path)
print(wsl_path)
# 出力: /mnt/c/Users/user/data.txt
```

### 4. プラットフォーム対応のパス正規化

```python
from src.utils import normalize_path_for_platform

# WSL環境: Windowsパスに変換
# 非WSL環境: そのまま返す
path = normalize_path_for_platform('/home/user/data.txt')
```

## 実装詳細

### エラーハンドリング

パス変換に失敗した場合、`RuntimeError` が発生します:

```python
from src.utils import wsl_to_windows_path

try:
    windows_path = wsl_to_windows_path('/invalid/path')
except RuntimeError as e:
    print(f"変換エラー: {e}")
```

### フォールバック動作

1. **UTF-8デコード**: まずUTF-8でデコードを試みる
2. **CP932デコード**: UTF-8が失敗したらCP932（日本語Windows）を試す
3. **Latin-1デコード**: 最終フォールバック（必ず成功）

### タイムアウト

パス変換コマンドには10秒のタイムアウトが設定されています。

## BatchExecutorでの使用

`BatchExecutor` は自動的にパス変換を行います:

```python
from src.services import BatchExecutor

executor = BatchExecutor()

# WSLパスを指定しても自動的にWindowsパスに変換される
result = executor.execute_batch('/home/user/project/run.bat')
```

内部的には `wsl_to_windows_path` を使用してパス変換を行っています。

## テスト

ユニットテストは `tests/unit/test_path_utils.py` に含まれています:

```bash
pytest tests/unit/test_path_utils.py -v
```

## 注意事項

1. **WSL環境のみ**: パス変換機能はWSL環境でのみ有効です。通常のLinux環境では入力パスをそのまま返します。

2. **wslpathコマンド**: WSL2以降で利用可能な `wslpath` コマンドを使用します。コマンドが見つからない場合はフォールバック動作を行います。

3. **UNCパスの制限**: 一部のWindowsアプリケーションはUNCパス (`\\wsl.localhost\...`) をサポートしていません。その場合は `/mnt/c/` 形式のパスを使用してください。

## 使用例

### COMSOLジョブの実行

```python
from pathlib import Path
from src.services import JobGenerator, execute_job
from src.utils import wsl_to_windows_path

# ジョブ生成
generator = JobGenerator(
    template_dir=Path('templates'),
    output_base_dir=Path('jobs/comsol')
)

params = {'lattice_constant': 1.0, ...}
result = generator.generate_job(params)

# ジョブ実行（パスは自動変換される）
exec_result = execute_job(result['job_dir'])
```

### 手動パス変換

```python
from pathlib import Path
from src.utils import wsl_to_windows_path

job_dir = Path('/home/user/project/jobs/comsol/job_20251119_161230')

# Windowsパスに変換してログ出力
windows_job_dir = wsl_to_windows_path(job_dir)
print(f"Job directory (Windows): {windows_job_dir}")
```

## 関連ドキュメント

- [Batch Executor Guide](batch_executor_guide.md) - バッチファイル実行の詳細
- [User Guide](user_guide.md) - 全体的な使用方法
- [Project Design](project_design.md) - プロジェクト設計
