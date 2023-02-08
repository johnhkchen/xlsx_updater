import pytest

from pathlib import Path
from lib.formula import FormulaAnnotation


@pytest.fixture
def cookies_xlsx():
    return FormulaAnnotation(
        "tests/input/xlsx/[No Kit] - Original American Cookies with Malt Extract.xlsx"
    )


def test_formula_annotation():
    fa = FormulaAnnotation()
    assert fa.wb is not None
    assert fa.document_name == "NULL"


def test_biscuit_file():
    p = Path("tests/input/xlsx/[No Kit] - Savoury Biscuits with Malt Extract.xlsx")
    biscuit_xlsx = FormulaAnnotation(p)
    biscuit_doc_name = "000012067 Univar Food - Recipe Card - Savoury Biscuits with Malt - Q2 2020.pdf"  # noqa: E501
    assert biscuit_xlsx.document_name == biscuit_doc_name


def test_anno_has_document_name(cookies_xlsx):
    expected_name = "000012063 Univar Food - Recipe Card - American Cookies with Malt - Q2 2020 Final.pdf"  # noqa: E501
    assert cookies_xlsx.document_name == expected_name


def test_anno_has_weights(cookies_xlsx):
    my_weights = cookies_xlsx.weights
    expected_weights = [
        "100g",
        "550g",
        "5g",
        "2g",
        "250g",
        "180g",
        "2",
        "250g",
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


def test_anno_has_trade_names(cookies_xlsx):
    raw_cells = cookies_xlsx.wb["Formulation"]["B"]
    expected_trade_names = []
    for cell in raw_cells[2:]:
        if not cell.value:
            break
        expected_trade_names.append(cell.value)
    assert cookies_xlsx.trade_names == expected_trade_names


def test_anno_has_inci_names(cookies_xlsx):
    raw_cells = cookies_xlsx.wb["Formulation"]["C"]
    expected_incis = []
    for cell in raw_cells[2:]:
        if not cell.value:
            break
        expected_incis.append(cell.value)

    assert cookies_xlsx.inci_names == expected_incis


def test_anno_has_settable_formula_name(cookies_xlsx):
    assert cookies_xlsx.formula_name == "Original American Cookies with Malt Extract"
    cookies_xlsx.formula_name = "Hip Dutch Coffee-Cakes with Earthy Essence"
    assert cookies_xlsx.formula_name == "Hip Dutch Coffee-Cakes with Earthy Essence"


def test_anno_has_settable_location(cookies_xlsx):
    assert cookies_xlsx.location == "EMEA"
    cookies_xlsx.location = "US"
    assert cookies_xlsx.location == "US"


def test_anno_has_settable_product_type(cookies_xlsx):
    assert cookies_xlsx.product_type == "food"
    cookies_xlsx.product_type = "unknown"
    assert cookies_xlsx.product_type == "unknown"


def test_anno_has_hero_trade_names(cookies_xlsx):
    raw_cells = cookies_xlsx.wb["Hero Ingredients"]["A"]
    expected_trade_names = []
    for cell in raw_cells[2:]:
        if not cell.value:
            break
        expected_trade_names.append(cell.value)
    assert cookies_xlsx.hero_trade_names == expected_trade_names


def test_anno_has_hero_inci_names(cookies_xlsx):
    raw_cells = cookies_xlsx.wb["Hero Ingredients"]["B"]
    expected_incis = []
    for cell in raw_cells[2:]:
        if not cell.value:
            break
        expected_incis.append(cell.value)

    assert cookies_xlsx.hero_inci_names == expected_incis
