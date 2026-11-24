import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
DASHBOARD = PROJECT_DIR / 'dashboard.py'

if not DASHBOARD.exists():
    raise FileNotFoundError('Dashboard file not found.')

subprocess.run(
    [sys.executable, '-m', 'streamlit', 'run', str(DASHBOARD)],
    cwd=str(PROJECT_DIR),
    check=True
)
