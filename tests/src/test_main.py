import pytest
import yaml

from pathlib import Path

from main import main
from lib.formula import FormulaAnnotation


@pytest.fixture
def biscuit_xlsx():
    return Path("tests/input/[No Kit] Savoury Biscuits with Malt Extract.xlsx")


@pytest.fixture
def biscuit_doc():
    return "000012067 Univar Food - Recipe Card - Savoury Biscuits with Malt - Q2 2020.pdf"  # noqa: E501


@pytest.fixture
def cookies_xlsx():
    return Path("tests/input/[No Kit] Original American Cookies with Malt Extract.xlsx")


@pytest.fixture
def cookies_doc():
    return "000012063 Univar Food - Recipe Card - American Cookies with Malt - Q2 2020 Final.pdf"  # noqa: E501


@pytest.fixture
def cookies_yaml_path():
    return Path("output/yaml/original_american_cookies_with_malt_extract.yaml")


def test_main_can_update_xlsx(cookies_xlsx, cookies_yaml_path):
    main(cookies_xlsx)
    xlsx = FormulaAnnotation(cookies_xlsx)
    # A YAML file with updated information is also created
    with open(cookies_yaml_path, "r") as f:
        yaml_contents = yaml.safe_load(f)
        assert yaml_contents["document_name"] == xlsx.document_name
        assert yaml_contents["formula_name"] == xlsx.formula_name
        assert yaml_contents["location"] == "EMEA"
        assert yaml_contents["product_type"] == "food"
        # Changes are NOT made to the original XLSX file!
    assert xlsx.location != "EMEA"
    assert xlsx.product_type != "food"
    # 3: Output XLSX file has updated values
    new_filepath = f"output/xlsx/[No Kit] {xlsx.formula_name}.xlsx"
    new_xlsx = FormulaAnnotation(new_filepath)
    assert new_xlsx.location == "EMEA"
    assert new_xlsx.product_type == "food"
