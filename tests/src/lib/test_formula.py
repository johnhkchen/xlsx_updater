import pytest

from pathlib import Path
from lib.formula import FormulaAnnotation


@pytest.fixture
def cookies_xlsx():
    return FormulaAnnotation(
        "tests/input/[No Kit] Original American Cookies with Malt Extract.xlsx"
    )


def test_formula_annotation():
    fa = FormulaAnnotation()
    assert fa.wb is not None
    assert fa.document_name == "NULL"


def test_biscuit_file():
    p = Path("tests/input/[No Kit] Savoury Biscuits with Malt Extract.xlsx")
    biscuit_xlsx = FormulaAnnotation(p)
    biscuit_doc_name = "000012067 Univar Food - Recipe Card - Savoury Biscuits with Malt - Q2 2020.pdf"  # noqa: E501
    assert biscuit_xlsx.document_name == biscuit_doc_name


def test_anno_has_document_name(cookies_xlsx):
    expected_name = "000012063 Univar Food - Recipe Card - American Cookies with Malt - Q2 2020 Final.pdf"  # noqa: E501
    assert cookies_xlsx.document_name == expected_name


def test_anno_has_weights(cookies_xlsx):
    my_weights = cookies_xlsx.weights
    expected_weights = [
        0.06901311249137336,
        0.3795721187025535,
        0.003450655624568668,
        0.0013802622498274672,
        0.1725327812284334,
        0.12422360248447205,
        0.07729468599033816,
        0.1725327812284334,
    ]
    assert my_weights == expected_weights


def test_weights_adjustable(cookies_xlsx):
    new_weights = [
        0.5,
        0.1,
        0.1,
        0.1,
        0.1,
        0.04,
        0.04,
        0.01,
    ]
    cookies_xlsx.weights = new_weights
    assert cookies_xlsx.weights == new_weights


def test_anno_has_settable_formula_name(cookies_xlsx):
    assert cookies_xlsx.formula_name == "Original American Cookies with Malt Extract"
    cookies_xlsx.formula_name = "Hip Dutch Coffee-Cakes with Earthy Essence"
    assert cookies_xlsx.formula_name == "Hip Dutch Coffee-Cakes with Earthy Essence"


def test_anno_has_settable_location(cookies_xlsx):
    assert cookies_xlsx.location == "US"
    cookies_xlsx.location = "EMEA"
    assert cookies_xlsx.location == "EMEA"


def test_anno_has_settable_product_type(cookies_xlsx):
    assert cookies_xlsx.product_type == "unknown"
    cookies_xlsx.product_type = "food"
    assert cookies_xlsx.product_type == "food"
