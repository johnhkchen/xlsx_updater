# Quality Check Tests
# Expected Usage: python3 src/workflows/quality_check.py
#
# Log whether annotation files have inconsistent data
#
# Input: Annotation File (xlsx)
# Input Path: 'input/xlsx'
#
# Output: Quality Check Report (yaml)
# Output Path: 'output/yaml'

import os
import pytest

from unittest.mock import patch

from lib.formula import FormulaAnnotation
from quality_check import quality_check


@pytest.fixture
def biscuit_xlsx_path():
    return "tests/input/xlsx/[No Kit] Savoury Biscuits with Malt Extract.xlsx"


@pytest.fixture
def biscuit_formula(biscuit_xlsx_path):
    return FormulaAnnotation(biscuit_xlsx_path)


def test_quality_check_method_available():
    assert callable(quality_check)


@patch("builtins.open")
def test_quality_check_accepts_path(mock_open):
    # quality_check should accept a file and generate a report
    # The report should be a yaml file with a list of errors
    biscuit_path = "tests/input/xlsx/[No Kit] Savoury Biscuits with Malt Extract.xlsx"
    output_path = "tests/output/yaml/"
    expected_report_name = "qc_report_savoury_biscuits_with_malt_extract.yaml"
    expected_report_path = os.path.join(output_path, expected_report_name)
    quality_check(biscuit_path, output_path)
    mock_open.assert_called_once_with(expected_report_path, "w")


@patch("builtins.open")
def test_quality_check_accepts_formula_annotation(mock_open):
    # quality_check should accept a file and generate a report
    # The report should be a yaml file with a list of errors
    biscuit_xlsx = FormulaAnnotation(
        "tests/input/xlsx/[No Kit] Savoury Biscuits with Malt Extract.xlsx"
    )
    output_path = "tests/output/yaml/"
    expected_report_name = "qc_report_savoury_biscuits_with_malt_extract.yaml"
    expected_report_path = os.path.join(output_path, expected_report_name)
    quality_check(biscuit_xlsx, output_path)
    mock_open.assert_called_once_with(expected_report_path, "w")
