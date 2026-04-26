# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for QwenPaw Desktop (Windows).

Build from repo root (on Windows):
    pyinstaller scripts/pack/qwenpaw.spec --noconfirm

Output:
    dist/QwenPaw/  — portable folder (QwenPaw.exe + _internal/)
    dist/QwenPaw-Setup-<ver>.exe — NSIS installer (optional)
"""

import sys
from pathlib import Path

# --- Project paths -----------------------------------------------------------
REPO_ROOT = Path(SPECPATH).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src" / "qwenpaw"
ICON_PATH = REPO_ROOT / "scripts" / "pack" / "assets" / "icon.ico"

# --- Version -----------------------------------------------------------------
version = "0.0.0"
ver_file = REPO_ROOT / "src" / "qwenpaw" / "__version__.py"
if ver_file.exists():
    for line in ver_file.read_text(encoding="utf-8").splitlines():
        if line.startswith("__version__"):
            version = line.split('"')[1]
            break

# --- Data files (package data that must be bundled) --------------------------
datas = []

# Console frontend (built by npm, copied to src/qwenpaw/console/)
console_dir = SRC_ROOT / "console"
if console_dir.is_dir() and (console_dir / "index.html").is_file():
    datas.append((str(console_dir), "qwenpaw/console"))

# Agent markdown files and skills
agents_md = SRC_ROOT / "agents" / "md_files"
if agents_md.is_dir():
    datas.append((str(agents_md), "qwenpaw/agents/md_files"))

agents_skills = SRC_ROOT / "agents" / "skills"
if agents_skills.is_dir():
    datas.append((str(agents_skills), "qwenpaw/agents/skills"))

# Tokenizer data
tokenizer_dir = SRC_ROOT / "tokenizer"
if tokenizer_dir.is_dir():
    datas.append((str(tokenizer_dir), "qwenpaw/tokenizer"))

# Security rules
for rule_dir in [
    SRC_ROOT / "security" / "tool_guard" / "rules",
    SRC_ROOT / "security" / "skill_scanner" / "rules",
    SRC_ROOT / "security" / "skill_scanner" / "data",
]:
    if rule_dir.is_dir():
        rel = rule_dir.relative_to(SRC_ROOT)
        datas.append((str(rule_dir), str(Path("qwenpaw") / rel)))

# certifi CA bundle (for SSL in offline environments)
try:
    import certifi
    datas.append((certifi.where(), "certifi"))
except ImportError:
    pass

# --- Hidden imports ----------------------------------------------------------
# PyInstaller cannot detect many dynamically-imported modules.
# We list the most critical ones here.
hiddenimports = [
    # ---- qwenpaw internal modules ----
    "qwenpaw",
    "qwenpaw.__main__",
    "qwenpaw.__version__",
    "qwenpaw.constant",
    "qwenpaw.exceptions",
    "qwenpaw.cli",
    "qwenpaw.cli.main",
    "qwenpaw.cli.app_cmd",
    "qwenpaw.cli.desktop_cmd",
    "qwenpaw.cli.init_cmd",
    "qwenpaw.cli.cron_cmd",
    "qwenpaw.cli.channels_cmd",
    "qwenpaw.cli.skills_cmd",
    "qwenpaw.cli.agents_cmd",
    "qwenpaw.cli.providers_cmd",
    "qwenpaw.cli.env_cmd",
    "qwenpaw.cli.daemon_cmd",
    "qwenpaw.cli.update_cmd",
    "qwenpaw.cli.uninstall_cmd",
    "qwenpaw.cli.shutdown_cmd",
    "qwenpaw.cli.clean_cmd",
    "qwenpaw.cli.auth_cmd",
    "qwenpaw.cli.chats_cmd",
    "qwenpaw.cli.acp_cmd",
    "qwenpaw.cli.plugin_commands",
    "qwenpaw.cli.task_cmd",
    "qwenpaw.cli.mission_cmd",
    "qwenpaw.cli.doctor_cmd",
    "qwenpaw.cli.doctor_checks",
    "qwenpaw.cli.doctor_fix_runner",
    "qwenpaw.cli.process_utils",
    "qwenpaw.cli.http",
    "qwenpaw.app",
    "qwenpaw.app._app",
    "qwenpaw.agents",
    "qwenpaw.agents.agent",
    "qwenpaw.agents.acp",
    "qwenpaw.agents.acp.server",
    "qwenpaw.agents.tools",
    "qwenpaw.agents.tools.edit_file",
    "qwenpaw.agents.tools.send_file",
    "qwenpaw.agents.tools.shell",
    "qwenpaw.agents.tools.browser_control",
    "qwenpaw.agents.tools.desktop_screenshot",
    "qwenpaw.agents.tools.view_media",
    "qwenpaw.agents.tools.memory_search",
    "qwenpaw.agents.tools.get_current_time",
    "qwenpaw.agents.tools.get_token_usage",
    "qwenpaw.agents.tools.agent_management",
    "qwenpaw.agents.tools.file_operations",
    "qwenpaw.agents.tools.grep_search",
    "qwenpaw.agents.tools.glob_search",
    "qwenpaw.config",
    "qwenpaw.config.utils",
    "qwenpaw.providers",
    "qwenpaw.providers.provider",
    "qwenpaw.providers.provider_manager",
    "qwenpaw.providers.dashscope",
    "qwenpaw.providers.openai_compat",
    "qwenpaw.providers.ollama",
    "qwenpaw.providers.lmstudio",
    "qwenpaw.providers.gemini",
    "qwenpaw.local_models",
    "qwenpaw.local_models.llamacpp",
    "qwenpaw.local_models.download_manager",
    "qwenpaw.security",
    "qwenpaw.security.tool_guard",
    "qwenpaw.security.skill_scanner",
    "qwenpaw.token_usage",
    "qwenpaw.tokenizer",
    "qwenpaw.token_usage.tracker",
    "qwenpaw.envs",
    "qwenpaw.envs.store",
    "qwenpaw.utils",
    "qwenpaw.utils.logging",
    "qwenpaw.utils.console_static",
    "qwenpaw.utils.system_info",
    "qwenpaw.utils.command_runner",
    "qwenpaw.utils.telemetry",
    "qwenpaw.utils.stdio",
    "qwenpaw.backup",
    "qwenpaw.plugins",
    "qwenpaw.tunnel",
    "qwenpaw.custom_channels",
    "qwenpaw.agent_stats",
    # ---- agentscope ----
    "agentscope",
    "agentscope.runtime",
    "agentscope_runtime",
    "agentscope_runtime.engine",
    "agentscope_runtime.engine.schemas",
    "agentscope_runtime.engine.schemas.agent_schemas",
    # ---- web framework ----
    "uvicorn",
    "uvicorn.lifespan",
    "uvicorn.lifespan.on",
    "uvicorn.protocols",
    "uvicorn.protocols.http",
    "uvicorn.protocols.http.auto",
    "uvicorn.protocols.websockets",
    "uvicorn.protocols.websockets.auto",
    "uvicorn.logging",
    "uvicorn.loops",
    "uvicorn.loops.auto",
    "fastapi",
    "starlette",
    "starlette.responses",
    "starlette.routing",
    "starlette.middleware",
    "starlette.staticfiles",
    "pydantic",
    "pydantic.deprecated",
    "pydantic.deprecated.decorator",
    # ---- channel SDKs ----
    "dingtalk_stream",
    "alibabacloud_dingtalk",
    "alibabacloud_tea_openapi",
    "lark_oapi",
    "discord",
    "telegram",
    "twilio",
    "matrix_nio",
    "wecom_aibot_python_sdk",
    "paho",
    "paho.mqtt",
    # ---- AI/ML ----
    "transformers",
    "huggingface_hub",
    "modelscope",
    "onnxruntime",
    "reme_ai",
    "google.genai",
    # ---- utilities ----
    "certifi",
    "httpx",
    "apscheduler",
    "apscheduler.schedulers",
    "apscheduler.schedulers.background",
    "apscheduler.triggers",
    "apscheduler.triggers.cron",
    "apscheduler.triggers.interval",
    "apscheduler.executors",
    "apscheduler.executors.pool",
    "playwright",
    "pywebview",
    "webview",
    "questionary",
    "mss",
    "pillow",
    "PIL",
    "cryptography",
    "cryptography.hazmat",
    "cryptography.hazmat.primitives",
    "keyring",
    "pyyaml",
    "json_repair",
    "segno",
    "shortuuid",
    "aiofiles",
    "python_socks",
    "python_dotenv",
    "packaging",
    "dotenv",
    "anyio",
    "sniffio",
    "click",
    "rich",
    "yaml",
]

# --- Binary/includes (native extensions) ------------------------------------
binaries = []

# onnxruntime native libs
try:
    import onnxruntime
    ort_path = Path(onnxruntime.__file__).parent
    binaries.append((str(ort_path / "capi"), "onnxruntime/capi"))
except (ImportError, OSError):
    pass

# --- Excludes (shrink bundle size) -------------------------------------------
excludes = [
    # Test/dev packages
    "pytest",
    "hypothesis",
    "pre_commit",
    # Unnecessary large submodules
    "tkinter",
    "unittest",
    "xmlrpc",
    "pydoc",
    "doctest",
    "lib2to3",
    "distutils",
    "setuptools",
    "pip",
    "wheel",
    # Playwright browser binaries (hundreds of MB; user installs separately)
    "playwright._impl._driver",
]

# --- Analysis ----------------------------------------------------------------
a = Analysis(
    [str(REPO_ROOT / "scripts" / "pack" / "pyinstaller_entry.py")],
    pathex=[str(REPO_ROOT / "src")],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    noconfirm=True,
)

# --- Bundle ------------------------------------------------------------------
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    name="QwenPaw",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # GUI mode (no console window on launch)
    icon=str(ICON_PATH) if ICON_PATH.exists() else None,
    version=version,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="QwenPaw",
)

# --- Debug EXE (with console window) ----------------------------------------
exe_debug = EXE(
    pyz,
    a.scripts,
    [],
    name="QwenPaw-Debug",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Shows console window for debugging
    icon=str(ICON_PATH) if ICON_PATH.exists() else None,
    version=version,
)

coll_debug = COLLECT(
    exe_debug,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="QwenPaw-Debug",
)
