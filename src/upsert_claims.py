import csv

from lib.utils import export_yaml

CLAIMS_PATH = "tests/input/csv/claims_mapping.csv"
YAML_NAME = "claims_cleanup.yaml"


def upsert_claims(claims_path=CLAIMS_PATH) -> dict[str, str]:
    output = {}
    with open(claims_path, "r") as claims_csv:
        reader = csv.reader(claims_csv, delimiter=",")
        for _ in range(4):
            next(reader)
        for row in reader:
            key, value = row[1], row[2]
            if key == "" or value == "":
                continue
            output[key] = [s.strip() for s in value.split(",")]

        export_yaml(YAML_NAME, output)
        return output


if __name__ == "__main__":
    from pprint import pprint

    obj = upsert_claims()
    pprint(obj)
    # print(obj["naturally preserve cosmetic skin-friendly formulations"])
