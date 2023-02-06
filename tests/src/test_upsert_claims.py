# Upsert Claims Tests
# Expected Usage: python3 src/workflows/upsert_claims.py
#
# Parses a CSV file of updated claim strings, and generates a
# fine-grained list of deletions and inserts that makes it
# easy for DB operations
#
# Input: Claims Update Table (CSV)
# File Name: 'claims_consolidation_mapping.csv'
# Input Path: 'input/csv'
#
# Input: Claims Worksheet (XLSX)
# Input Path: 'input/xlsx'
#
# Output: Claims Update Queries (csv)
# Output Path: 'output/csv'


import csv
import pytest
from pathlib import Path

from upsert_claims import upsert_claims


def test_upsert_claims_method_available():
    assert callable(upsert_claims)


@pytest.fixture
def claims_csv_path():
    return "tests/input/csv/claims_mapping.csv"


@pytest.fixture
def results():
    return upsert_claims()


def test_csv_path_exists(claims_csv_path):
    my_path = Path(claims_csv_path)

    assert my_path.exists()


def test_upsert_returns_dict(results):
    assert isinstance(results, dict)


def test_upsert_doesnt_return_junk(results):
    assert "" not in results


def test_upsert_excludes_headers(results):
    HEADER_CELL = "Unique Ing Claim"
    assert HEADER_CELL not in results


def test_upsert_all_keys_in_dict(claims_csv_path):
    HEADER_TITLE = "Unique Ing Claim"
    result = upsert_claims(claims_csv_path)

    with open(claims_csv_path, "r") as claims_csv:
        reader = csv.reader(claims_csv, delimiter=",")
        for row in reader:
            key, value = row[1], row[2]
            if key == HEADER_TITLE or key == "":
                continue
            if value != "":
                assert key in result
                assert isinstance(result[key], list)
                assert isinstance(result[key][0], str)
                assert len(result[key][0]) > 0


def test_upsert_creates_split_values(results):
    test_key = "naturally preserve cosmetic skin-friendly formulations"
    assert isinstance(results[test_key], list)
    assert len(results[test_key]) == 2
    for tag in results[test_key]:
        assert isinstance(tag, str)


def test_upsert_splits_along_comma_properly(results):
    test_key = "100% rutile-type titanium dioxide core with a very tight double coating of silica and dimethicone"  # noqa: E501
    assert test_key in results
    value = results[test_key]
    assert len(value) == 2
    assert value[0] == "100% rutile-type titanium dioxide core"
    assert value[1] == "very tight double coating of silica and dimethicone"


def test_upsert_creates_yaml():
    upsert_claims()
    yaml_path = Path("output/yaml/claims_cleanup.yaml")
    assert yaml_path.exists()
