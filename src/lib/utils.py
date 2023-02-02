import yaml
from pathlib import Path


def get_input_files(path="input/"):
    # Ignore phantom copy made by MS Excel
    def is_valid(f: Path):
        return f.suffix == ".xlsx" and f.name[0] != "~"

    return [f for f in Path(path).iterdir() if is_valid(f)]


def export_yaml(file_name, obj, output_dir: str = "output/yaml/"):
    with open(output_dir + file_name, "w") as f:
        yaml.dump(obj, f)
