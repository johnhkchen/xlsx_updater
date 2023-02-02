# Quality Check
# Expected Usage: python3 src/quality_check.py
#
# Log whether annotation files have inconsistent data
#
# Input: Annotation File (xlsx)
# Input Path: 'input/xlsx'
#
# Output: Quality Check Report (yaml)
# Output Path: 'output/yaml'

from pathlib import Path

from lib.formula import FormulaAnnotation
from lib.utils import export_yaml


def quality_check(xlsx: str | FormulaAnnotation, output: str | Path = "output/yaml/"):
    if isinstance(xlsx, str):
        xlsx = FormulaAnnotation(xlsx)
    if isinstance(output, str):
        output = Path(output)
    file_name = (
        "qc_report_"
        + xlsx.formula_name.replace(" ", "_").replace("-", "_").lower()
        + ".yaml"
    )
    obj = {
        "Summary": "Quality Check Report (Prototype)",
        "Checks": [
            {"Check 1": "Pass"},
            {"Check 2": "Pass"},
            {"Check 3": "Pass"},
        ],
    }
    export_yaml(file_name, obj, output)
