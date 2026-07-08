from pathlib import Path
import sys
ADAPTER_SRC = str(Path(__file__).resolve().parents[3] / "packages" / "hpsu_dan_adapter")
if ADAPTER_SRC not in sys.path:
    sys.path.insert(0, ADAPTER_SRC)
