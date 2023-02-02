from pathlib import Path

from lib.utils import export_yaml


def test_export_yaml_creates_file():
    file_name = "test_ouput.yaml"
    output_path = "tests/output/yaml/"
    sample_obj = {"foo": "bar"}
    export_yaml(file_name, sample_obj, output_dir=output_path)
    assert Path(output_path + file_name).exists()
