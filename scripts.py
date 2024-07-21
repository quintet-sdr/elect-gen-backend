import subprocess
import sys
from pathlib import Path
from typing import Never
import os
from os import path
from src.cli import Args


def dev() -> None:
    args = Args().parse_args()
    os.environ["CORE"] = str(args.core)
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
    os.environ["CORE"] = str(args.core)
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


def venv(exe: str, venv_path: Path = Path(".venv")) -> str:
    if path.exists(venv_path / "bin"):
        return str(venv_path / "bin" / exe)
    elif path.exists(venv_path / "Scripts"):
        return str(venv_path / "Scripts" / exe)
    else:
        raise RuntimeError("No bin directory found in the venv dir")


def test() -> None:
    args = Args().parse_args()
    command = f'python {os.path.join(str(args.core), "algorithm_cli.py")} --courses {os.path.join(str(args.core), "courses.json")} --students {os.path.join(str(args.core), "students.json")} --output {os.path.join(str(args.core), "distribution.json")}'
    print(command)
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True, encoding="utf-8"
    )
    print(result.stdout)
