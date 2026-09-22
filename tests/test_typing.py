import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_mypy_reports_no_errors() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "config", "url_shortener"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout or result.stderr
