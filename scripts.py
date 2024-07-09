import subprocess
import sys
from pathlib import Path
from typing import Never

from src.cli import Args


def dev() -> None:
    args = Args().parse_args()
    execute(
        [
            venv("uvicorn"),
            "--host",
            args.host,
            "--port",
            str(args.port),
            "--reload",
            "src.main:app",
        ]
    )


def start() -> None:
    args = Args().parse_args()
    execute(
        [
            venv("uvicorn"),
            "--host",
            args.host,
            "--port",
            str(args.port),
            "src.main:app",
        ]
    )


def lint() -> None:
    execute([venv("ruff"), "format", "--check"])
    execute([venv("ruff"), "check"])


def format() -> None:
    execute([venv("ruff"), "format"])


def execute(args: list[str]) -> None | Never:
    status = subprocess.run(args).returncode
    if status != 0:
        sys.exit(status)


def venv(exe: str, venv_path: str = ".venv") -> str:
    return str(Path(venv_path) / "bin" / exe)
