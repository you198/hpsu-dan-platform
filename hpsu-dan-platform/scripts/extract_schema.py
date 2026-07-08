# -*- coding: utf-8 -*-
"""提取共享 PredictRequest schema 到 hpsu_dan_adapter 包"""
import sys, os, re

ROOT = os.getcwd()
ADAPTER_DIR = os.path.join(ROOT, 'hpsu-dan-platform', 'packages', 'hpsu_dan_adapter', 'hpsu_dan_adapter')
API_SCHEMAS = os.path.join(ROOT, 'hpsu-dan-platform', 'services', 'api', 'app', 'schemas.py')
API_INIT = os.path.join(ROOT, 'hpsu-dan-platform', 'services', 'api', 'app', '__init__.py')
INFERENCE_MAIN = os.path.join(ROOT, 'hpsu-dan-platform', 'services', 'inference', 'app', 'main.py')
ADAPTER_INIT = os.path.join(ADAPTER_DIR, '__init__.py')
ADAPTER_SCHEMAS = os.path.join(ADAPTER_DIR, 'schemas.py')

# Step 1: Create the shared schemas.py
schemas_content = """from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    \"\"\"共享推理请求模型：API 服务转发给推理服务时使用。\"\"\"
    samples: list[float] = Field(min_length=1024, max_length=262144)
    sampling_rate: int = Field(default=25600, ge=1, le=1000000)
    model_id: str = Field(default=\"{MODEL_ID}\", max_length=128)
""".replace("{MODEL_ID}", "hpsu-dan-v1")

with open(ADAPTER_SCHEMAS, 'w', encoding='utf-8') as f:
    f.write(schemas_content)
print(f"1. Created {ADAPTER_SCHEMAS}")

# Step 2: Update adapter __init__.py
init_content = open(ADAPTER_INIT, 'r', encoding='utf-8').read()
if "PredictRequest" not in init_content:
    if "from .legacy_bridge" in init_content:
        init_content = init_content.replace(
            "from .legacy_bridge import HPSUDANLegacyBridge",
            "from .legacy_bridge import HPSUDANLegacyBridge\nfrom .schemas import PredictRequest"
        )
    if "__all__" in init_content:
        init_content = init_content.replace(
            '__all__ = ["HPSUDANLegacyBridge"]',
            '__all__ = ["HPSUDANLegacyBridge", "PredictRequest"]'
        )
    with open(ADAPTER_INIT, 'w', encoding='utf-8') as f:
        f.write(init_content)
    print(f"2. Updated {ADAPTER_INIT}")
else:
    print("2. Already has PredictRequest, skipped")

# Step 3: Add sys.path setup in api/app/__init__.py
api_init_content = open(API_INIT, 'r', encoding='utf-8').read()
adapter_import = "from pathlib import Path\nimport sys\n"
adapter_path_setup = (
    'ADAPTER_SRC = str(Path(__file__).resolve().parents[3] / "packages" / "hpsu_dan_adapter")\n'
    'if ADAPTER_SRC not in sys.path:\n'
    '    sys.path.insert(0, ADAPTER_SRC)\n'
)
if "ADAPTER_SRC" not in api_init_content:
    new_init = adapter_import + adapter_path_setup
    with open(API_INIT, 'w', encoding='utf-8') as f:
        f.write(new_init)
    print(f"3. Updated {API_INIT}")
else:
    print("3. Already has ADAPTER_SRC, skipped")

# Step 4: Update API schemas.py - replace class with import
schemas_full = open(API_SCHEMAS, 'r', encoding='utf-8').read()
old_diagnosis_class = (
    "class DiagnosisRequest(BaseModel):\n"
    "    samples: list[float] = Field(min_length=1024, max_length=262144)\n"
    "    sampling_rate: int = Field(default=25600, ge=1, le=1000000)\n"
    "    model_id: str = Field(default=\"hpsu-dan-v1\", max_length=128)"
)
new_diagnosis_import = (
    "from hpsu_dan_adapter.schemas import PredictRequest as DiagnosisRequest\n"
    "\n"
    "\n"
    "class TaskView(BaseModel):"
)

# Find the position of the DiagnosisRequest class
if "class DiagnosisRequest" in schemas_full:
    lines = schemas_full.split("\n")
    new_lines = []
    skip_diagnosis = False
    replaced = False
    for i, line in enumerate(lines):
        if line.strip().startswith("class DiagnosisRequest(BaseModel):"):
            skip_diagnosis = True
            # Add the import line before this class
            new_lines.append("from hpsu_dan_adapter.schemas import PredictRequest as DiagnosisRequest")
            replaced = True
            continue
        if skip_diagnosis:
            # Skip until we hit a blank line followed by "class" or end of file
            if line.strip() == "" and i + 1 < len(lines) and lines[i + 1].strip().startswith("class "):
                skip_diagnosis = False
            elif line.strip().startswith("class "):
                skip_diagnosis = False
                new_lines.append(line)
                continue
            elif not line.strip() and not any(l.strip() for l in lines[i+1:i+3]):
                continue
            else:
                continue
        new_lines.append(line)
    
    schemas_full = "\n".join(new_lines)
    with open(API_SCHEMAS, 'w', encoding='utf-8') as f:
        f.write(schemas_full)
    print(f"4. Updated {API_SCHEMAS} (removed DiagnosisRequest, added import)")
else:
    print("4. DiagnosisRequest not found or already replaced")

# Step 5: Update inference main.py - replace PredictRequest class with import
inf_main = open(INFERENCE_MAIN, 'r', encoding='utf-8').read()

# Check if it already imports from adapter
if "from hpsu_dan_adapter.schemas" in inf_main:
    print("5. PredictRequest already imported from adapter, skipped")
else:
    # Find and remove the PredictRequest class
    lines = inf_main.split("\n")
    new_lines = []
    skip_predict = False
    in_predict = False
    replaced = False
    prev_was_class = False
    
    for i, line in enumerate(lines):
        if line.strip().startswith("class PredictRequest(BaseModel):"):
            in_predict = True
            skip_predict = True
            continue
        if in_predict:
            # Check if we've finished the class
            if line.strip() == "":
                # Check next non-empty line
                next_non_empty = None
                for j in range(i + 1, min(i + 5, len(lines))):
                    if lines[j].strip():
                        next_non_empty = lines[j].strip()
                        break
                if next_non_empty and (next_non_empty.startswith("@") or next_non_empty.startswith("async def") or next_non_empty.startswith("def ") or next_non_empty.startswith("class ") or next_non_empty.startswith("LABELS")):
                    in_predict = False
                    skip_predict = False
                    if not replaced:
                        new_lines.append("from hpsu_dan_adapter.schemas import PredictRequest")
                        replaced = True
                    continue
            elif line.strip().startswith("LABELS"):
                in_predict = False
                skip_predict = False
                if not replaced:
                    new_lines.append("from hpsu_dan_adapter.schemas import PredictRequest")
                    new_lines.append("")
                    replaced = True
                new_lines.append(line)
                continue
            continue
        new_lines.append(line)
    
    inf_main = "\n".join(new_lines)
    with open(INFERENCE_MAIN, 'w', encoding='utf-8') as f:
        f.write(inf_main)
    print(f"5. Updated {INFERENCE_MAIN}")

print("\nAll done!")
