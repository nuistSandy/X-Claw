#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PyInstaller entry point for QwenPaw Desktop.

When the frozen executable is double-clicked, it launches the desktop
mode (webview window) by default. It also supports all CLI subcommands
(e.g. ``QwenPaw.exe app``, ``QwenPaw.exe init --defaults``), which is
essential because ``desktop_cmd`` spawns a subprocess running the same
executable with the ``app`` subcommand.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _setup_env() -> None:
    """Set environment variables for the frozen desktop application."""
    os.environ.setdefault("QWENPAW_DESKTOP_APP", "1")
    os.environ.setdefault("PYTHONNOUSERSITE", "1")
    os.environ.setdefault("QWENPAW_LOG_LEVEL", "info")

    # SSL certificates — use certifi's CA bundle
    try:
        import certifi

        cert_path = certifi.where()
        if cert_path and os.path.exists(cert_path):
            os.environ.setdefault("SSL_CERT_FILE", cert_path)
            os.environ.setdefault("REQUESTS_CA_BUNDLE", cert_path)
            os.environ.setdefault("CURL_CA_BUNDLE", cert_path)
    except ImportError:
        pass


def _auto_init() -> None:
    """Create default config if none exists."""
    config_path = Path.home() / ".qwenpaw" / "config.json"
    if config_path.exists():
        return
    try:
        # In frozen mode sys.executable is the .exe itself, so:
        #   QwenPaw.exe init --defaults --accept-security
        # Click will route "init" to init_cmd.
        import subprocess

        result = subprocess.run(
            [sys.executable, "init", "--defaults", "--accept-security"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            print(
                f"[QwenPaw] Auto-init failed (exit {result.returncode}): "
                f"{result.stderr}",
                file=sys.stderr,
            )
    except Exception as exc:
        print(f"[QwenPaw] Auto-init exception: {exc}", file=sys.stderr)


def _redirect_stdio_to_log() -> None:
    """Redirect stdout/stderr to a log file when running without console.

    PyInstaller builds with ``console=False`` have no terminal, so we
    redirect to ``~/.qwenpaw/desktop.log`` for troubleshooting.
    """
    log_dir = Path.home() / ".qwenpaw"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "desktop.log"

    try:
        log_file = open(log_path, "a", encoding="utf-8")  # noqa: SIM115
        sys.stdout = log_file
        sys.stderr = log_file
    except Exception:
        pass  # Best effort


def main() -> None:
    """Entry point for the frozen QwenPaw Desktop application."""
    _setup_env()

    # Detect whether we have a console window.
    # When built with console=False, sys.stdout may be None.
    has_console = sys.stdout is not None
    if not has_console:
        _redirect_stdio_to_log()

    # Default to "desktop" subcommand when launched without arguments
    # (i.e. user double-clicked the .exe).
    if len(sys.argv) == 1:
        sys.argv = [sys.argv[0], "desktop"]

    # Auto-init before running the command
    if sys.argv[1:2] == ["desktop"]:
        _auto_init()

    from qwenpaw.cli.main import cli

    cli()


if __name__ == "__main__":
    main()
