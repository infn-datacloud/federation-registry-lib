import sys
from pathlib import Path

external_path = Path.cwd().parent
sys.path.insert(1, str(external_path))