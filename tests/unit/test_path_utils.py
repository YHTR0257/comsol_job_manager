"""Unit tests for path utility functions."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.utils.path_utils import (
    detect_wsl,
    wsl_to_windows_path,
    windows_to_wsl_path,
    normalize_path_for_platform,
)


class TestDetectWSL:
    """Tests for WSL detection."""

    @patch('os.path.exists')
    @patch('builtins.open', create=True)
    def test_detect_wsl_from_proc_version_microsoft(self, mock_open, mock_exists):
        """Test WSL detection from /proc/version with 'microsoft'."""
        mock_exists.return_value = True
        mock_open.return_value.__enter__.return_value.read.return_value = (
            "Linux version 4.4.0-19041-Microsoft"
        )

        assert detect_wsl() is True

    @patch('os.path.exists')
    @patch('builtins.open', create=True)
    def test_detect_wsl_from_proc_version_wsl(self, mock_open, mock_exists):
        """Test WSL detection from /proc/version with 'wsl'."""
        mock_exists.return_value = True
        mock_open.return_value.__enter__.return_value.read.return_value = (
            "Linux version 5.10.16.3-WSL2"
        )

        assert detect_wsl() is True

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_wsl_from_wslpath_command(self, mock_run, mock_exists):
        """Test WSL detection from wslpath command availability."""
        mock_exists.return_value = False
        mock_run.return_value = MagicMock(returncode=0)

        assert detect_wsl() is True

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_wsl_not_in_wsl(self, mock_run, mock_exists):
        """Test WSL detection when not in WSL."""
        mock_exists.return_value = False
        mock_run.return_value = MagicMock(returncode=1)

        assert detect_wsl() is False


class TestWSLToWindowsPath:
    """Tests for WSL to Windows path conversion."""

    @patch('src.utils.path_utils.detect_wsl')
    @patch('subprocess.run')
    def test_wsl_to_windows_path_success(self, mock_run, mock_detect):
        """Test successful path conversion."""
        mock_detect.return_value = True
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='C:\\Users\\user\\file.txt\n'
        )

        result = wsl_to_windows_path('/home/user/file.txt')
        assert result == 'C:\\Users\\user\\file.txt'
        mock_run.assert_called_once()

    @patch('src.utils.path_utils.detect_wsl')
    def test_wsl_to_windows_path_not_in_wsl(self, mock_detect):
        """Test path conversion when not in WSL."""
        mock_detect.return_value = False

        result = wsl_to_windows_path('/home/user/file.txt')
        assert result == '/home/user/file.txt'

    @patch('src.utils.path_utils.detect_wsl')
    @patch('subprocess.run')
    def test_wsl_to_windows_path_with_pathlib(self, mock_run, mock_detect):
        """Test path conversion with Path object."""
        mock_detect.return_value = True
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='C:\\Users\\user\\data\n'
        )

        result = wsl_to_windows_path(Path('/home/user/data'))
        assert result == 'C:\\Users\\user\\data'

    @patch('src.utils.path_utils.detect_wsl')
    @patch('subprocess.run')
    def test_wsl_to_windows_path_conversion_failure(self, mock_run, mock_detect):
        """Test path conversion failure."""
        mock_detect.return_value = True
        mock_run.side_effect = subprocess.CalledProcessError(
            1, 'wslpath', stderr='Invalid path'
        )

        with pytest.raises(RuntimeError, match='Failed to convert path'):
            wsl_to_windows_path('/invalid/path')

    @patch('src.utils.path_utils.detect_wsl')
    @patch('subprocess.run')
    def test_wsl_to_windows_path_timeout(self, mock_run, mock_detect):
        """Test path conversion timeout."""
        mock_detect.return_value = True
        mock_run.side_effect = subprocess.TimeoutExpired('wslpath', 10)

        with pytest.raises(RuntimeError, match='Path conversion timed out'):
            wsl_to_windows_path('/home/user/file.txt')


class TestWindowsToWSLPath:
    """Tests for Windows to WSL path conversion."""

    @patch('src.utils.path_utils.detect_wsl')
    @patch('subprocess.run')
    def test_windows_to_wsl_path_success(self, mock_run, mock_detect):
        """Test successful path conversion."""
        mock_detect.return_value = True
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='/mnt/c/Users/user/file.txt\n'
        )

        result = windows_to_wsl_path('C:\\Users\\user\\file.txt')
        assert result == '/mnt/c/Users/user/file.txt'
        mock_run.assert_called_once()

    @patch('src.utils.path_utils.detect_wsl')
    def test_windows_to_wsl_path_not_in_wsl(self, mock_detect):
        """Test path conversion when not in WSL."""
        mock_detect.return_value = False

        result = windows_to_wsl_path('C:\\Users\\user\\file.txt')
        assert result == 'C:\\Users\\user\\file.txt'


class TestNormalizePathForPlatform:
    """Tests for platform-specific path normalization."""

    @patch('src.utils.path_utils.detect_wsl')
    @patch('src.utils.path_utils.wsl_to_windows_path')
    def test_normalize_path_in_wsl(self, mock_convert, mock_detect):
        """Test path normalization in WSL."""
        mock_detect.return_value = True
        mock_convert.return_value = 'C:\\Users\\user\\file.txt'

        result = normalize_path_for_platform('/home/user/file.txt')
        assert result == 'C:\\Users\\user\\file.txt'
        mock_convert.assert_called_once_with('/home/user/file.txt')

    @patch('src.utils.path_utils.detect_wsl')
    def test_normalize_path_not_in_wsl(self, mock_detect):
        """Test path normalization when not in WSL."""
        mock_detect.return_value = False

        result = normalize_path_for_platform('/home/user/file.txt')
        assert result == '/home/user/file.txt'

    @patch('src.utils.path_utils.detect_wsl')
    @patch('src.utils.path_utils.wsl_to_windows_path')
    def test_normalize_path_with_pathlib(self, mock_convert, mock_detect):
        """Test path normalization with Path object."""
        mock_detect.return_value = True
        mock_convert.return_value = 'C:\\Users\\user\\data'

        result = normalize_path_for_platform(Path('/home/user/data'))
        assert result == 'C:\\Users\\user\\data'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
