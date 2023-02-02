import os

from unittest.mock import patch
from pathlib import Path

from lib.utils import export_yaml


@patch("builtins.open")
def test_export_yaml_creates_file(mock_open):
    file_name = "test_ouput.yaml"
    output_path = "tests/output/yaml/"
    sample_obj = {"foo": "bar"}
    export_yaml(file_name, sample_obj, output_dir=output_path)
    expected_output_path = os.path.join(output_path, file_name)
    mock_open.assert_called_once_with(expected_output_path, "w")


@patch("builtins.open")
def test_export_yaml_accepts_str_paths(mock_open):
    # Case 1: str only
    file_str = "test_ouput.yaml"
    output_str = "tests/output/yaml/"
    export_yaml(file_str, {}, output_dir=output_str)
    expected_path = os.path.join(output_str, file_str)
    mock_open.assert_called_once_with(expected_path, "w")


@patch("builtins.open")
def test_export_yaml_accepts_mixed_paths(mock_open):
    # Case 2: Mixed str + path
    file_str = "test_ouput.yaml"
    output_path = Path("tests/output/yaml/")
    export_yaml(file_str, {}, output_dir=output_path)
    expected_path = os.path.join(output_path, file_str)
    mock_open.assert_called_once_with(expected_path, "w")


@patch("builtins.open")
def test_export_yaml_accepts_paths(mock_open):
    # Case 3: Path only
    file_str = "test_ouput.yaml"
    output_str = "tests/output/yaml/"
    full_file_path = Path(os.path.join(output_str, file_str))
    export_yaml(full_file_path, {})
    mock_open.assert_called_once_with(full_file_path, "w")
