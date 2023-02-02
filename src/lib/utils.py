import os
import yaml
from pathlib import Path


def get_input_files(path="input/"):
    # Ignore phantom copy made by MS Excel
    def is_valid(f: Path):
        return f.suffix == ".xlsx" and f.name[0] != "~"

    return [f for f in Path(path).iterdir() if is_valid(f)]


def export_yaml(file_name: str | Path, obj, output_dir: str | Path = "output/yaml/"):
    # file_name might be a full path on its own
    # or just file name with path specified in output_dir
    if isinstance(file_name, str):
        file_name = os.path.join(output_dir, file_name)
    with open(file_name, "w") as f:
        yaml.dump(obj, f)
