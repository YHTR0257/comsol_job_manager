from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
import re
from typing import Any, Dict, Union

import yaml

# Public API
__all__ = [
    "load_config",
    "setup_logging",
    "get_logger",
    "get_config_path_for_env",
    "get_current_env",
]

_LOGGER_NAME = "esp"  # project logger name
_PLACEHOLDER_PATTERN = re.compile(r"\$\{([^}]+)\}")

# Environment mapping
_ENV_MAP = {
    "development": "dev",
    "dev": "dev",
    "production": "prod",
    "prod": "prod",
}


# ---- Environment utilities ----

def get_current_env() -> str:
    """Get the current environment from ENV variable.

    Returns
    -------
    str
        Environment name: 'dev' or 'prod'.
        Defaults to 'dev' if ENV is not set.

    Examples
    --------
    >>> # With ENV=development in .env
    >>> get_current_env()
    'dev'

    >>> # With ENV=production in .env
    >>> get_current_env()
    'prod'
    """
    # Try to load from .env file if python-dotenv is available
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    env_value = os.getenv("ENV", "development").lower()
    return _ENV_MAP.get(env_value, "dev")


def get_config_path_for_env(
    config_type: str,
    env: str = None,
    base_dir: Union[str, Path] = None
) -> Path:
    """Get the configuration file path for a given environment and config type.

    Parameters
    ----------
    config_type : str
        Type of configuration: 'elf_features' or 'training'.
    env : str, optional
        Environment name. If None, uses get_current_env().
        Can be 'dev', 'prod', 'development', 'production'.
    base_dir : str | Path, optional
        Base directory for configs. Default: PROJECT_ROOT/configs

    Returns
    -------
    Path
        Path to the configuration file.

    Raises
    ------
    FileNotFoundError
        If the configuration file doesn't exist.

    Examples
    --------
    >>> # Get training config for current environment
    >>> path = get_config_path_for_env('training')

    >>> # Get feature extraction config for production
    >>> path = get_config_path_for_env('elf_features', env='production')

    >>> # Custom base directory
    >>> path = get_config_path_for_env('training', base_dir='/custom/configs')
    """
    if env is None:
        env = get_current_env()
    else:
        env = _ENV_MAP.get(env.lower(), env.lower())

    if base_dir is None:
        # Try to find project root
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent.parent  # src/config/loader.py -> project root
        base_dir = project_root / "configs"
    else:
        base_dir = Path(base_dir)

    config_path = base_dir / env / f"{config_type}.yml"

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}\n"
            f"Environment: {env}\n"
            f"Config type: {config_type}\n"
            f"Expected path: {config_path}"
        )

    return config_path


# ---- Config loading ----

def load_config(path: Union[str, os.PathLike], resolve_vars: bool = True) -> Dict[str, Any]:
    """
    Load a YAML config file as a nested dict.

    - Supports simple placeholder interpolation like ${a.b.c} referencing other
      keys in the same config. Interpolation runs a few passes until stable.
    - Does not execute arbitrary code (safe_load).

    Parameters
    ----------
    path : str | Path
        Path to the YAML configuration file.
    resolve_vars : bool
        If True, resolve ${...} placeholders using values in the config.

    Returns
    -------
    dict
        Configuration dictionary.
    """
    with open(path, "r", encoding="utf-8") as f:
        cfg: Dict[str, Any] = yaml.safe_load(f) or {}

    if resolve_vars:
        cfg = _resolve_placeholders(cfg)

    return cfg


def _resolve_placeholders(cfg: Dict[str, Any], max_passes: int = 3) -> Dict[str, Any]:
    """Resolve ${a.b.c} placeholders in strings within the config dict.

    Performs up to `max_passes` passes or until no changes detected.
    """
    def lookup(path: str) -> Any:
        cur: Any = cfg
        for key in path.split('.'):
            if isinstance(cur, dict) and key in cur:
                cur = cur[key]
            else:
                return None
        return cur

    def resolve_in_value(v: Any) -> Any:
        if isinstance(v, str):
            def replacer(m: re.Match[str]) -> str:
                found = lookup(m.group(1))
                return str(found) if found is not None else m.group(0)
            return _PLACEHOLDER_PATTERN.sub(replacer, v)
        if isinstance(v, list):
            return [resolve_in_value(x) for x in v]
        if isinstance(v, dict):
            return {k: resolve_in_value(val) for k, val in v.items()}
        return v

    before = None
    current = cfg
    for _ in range(max_passes):
        after = resolve_in_value(current)
        if before == after:
            break
        before = after
        current = after
    return current  # type: ignore[return-value]


# ---- Logging setup ----

def setup_logging(cfg: Dict[str, Any] | None = None) -> logging.Logger:
    """
    Configure project logging using settings from config["logging"].

    Supported keys (with defaults):
      logging:
        level: INFO             # base logger level
        fmt: "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        datefmt: "%Y-%m-%d %H:%M:%S"
        console:
          enabled: true
          level: INFO
        file:
          enabled: true
          dir: logs
          filename: "run.log"
          level: INFO
          rotate: true
          max_bytes: 1048576
          backup_count: 5

    Returns the configured project logger.
    """
    log_cfg = (cfg or {}).get("logging", {}) if isinstance(cfg, dict) else {}

    def to_level(x: Any, default: int = logging.INFO) -> int:
        if isinstance(x, int):
            return x
        if isinstance(x, str):
            return getattr(logging, x.upper(), default)
        return default

    fmt = log_cfg.get("fmt", "%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    datefmt = log_cfg.get("datefmt", "%Y-%m-%d %H:%M:%S")
    base_level = to_level(log_cfg.get("level", logging.INFO))

    console_cfg = log_cfg.get("console", {}) or {}
    file_cfg = log_cfg.get("file", {}) or {}

    logger = logging.getLogger(_LOGGER_NAME)
    logger.setLevel(base_level)
    logger.propagate = False

    # Avoid duplicate handlers in repeated calls
    if logger.handlers:
        logger.handlers.clear()

    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

    # Console handler
    if console_cfg.get("enabled", True):
        ch = logging.StreamHandler()
        ch.setLevel(to_level(console_cfg.get("level", base_level)))
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    # File handler
    if file_cfg.get("enabled", True):
        log_dir = Path(file_cfg.get("dir", "logs"))
        log_dir.mkdir(parents=True, exist_ok=True)
        filename = str(file_cfg.get("filename", "run.log"))
        file_path = log_dir / filename

        file_level = to_level(file_cfg.get("level", base_level))
        rotate = bool(file_cfg.get("rotate", True))
        if rotate:
            max_bytes = int(file_cfg.get("max_bytes", 1_048_576))
            backup_count = int(file_cfg.get("backup_count", 5))
            fh = RotatingFileHandler(file_path, maxBytes=max_bytes, backupCount=backup_count)
        else:
            fh = logging.FileHandler(file_path)
        fh.setLevel(file_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    # Make root permissive so handlers decide, but don't add handlers to root
    logging.getLogger().setLevel(logging.WARNING)

    logger.debug("Logging configured", extra={"logger_name": _LOGGER_NAME})
    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    """Get the project logger or a named child logger."""
    base = logging.getLogger(_LOGGER_NAME)
    if not base.handlers:
        # Provide sensible defaults if setup_logging wasn't called
        setup_logging({})
        base = logging.getLogger(_LOGGER_NAME)
    return base if not name else base.getChild(name)
