# Parse all the formula documents in input/
# Generate a list of ingredients, along with documents referencing this ingredient
# Trade Name: str - key
# INCIs: str
# Formula Kit: [str]
# Hero Ingredient: bool
# Num Files: int
# Files: [str]
# File Paths: [str]

import pytest
from pathlib import Path

from analyze_formulas import analyze_formulas, IngredientReport
from lib.formula import FormulaAnnotation


@pytest.fixture
def null_report() -> IngredientReport:
    return analyze_formulas()


@pytest.fixture
def anno_dir() -> Path:
    return Path("tests/input/xlsx")


@pytest.fixture
def anno_paths() -> list[Path]:
    return [
        Path(
            "tests/input/xlsx/[No Kit] - Original American Cookies with Malt Extract.xlsx"  # noqa: E501
        ),
        Path(
            "tests/input/xlsx/[No Kit] - Savoury Biscuits with Malt Extract.xlsx"  # noqa: E501
        ),
    ]


def test_analyze_formulas_callable():
    assert callable(analyze_formulas)


def test_formula_report_has_to_table_method(null_report):
    assert callable(null_report.to_table)


def test_formula_report_shape(null_report):
    # Each row should have 7 items, including empty sets
    assert all([len(row) == 7 for row in null_report.to_table()])


def test_can_select_input_directory(anno_dir: Path):
    # analyze_formulas can accept a folder and it will read from the folder
    table = analyze_formulas(anno_dir).to_table()
    assert len(table) > 0


def test_can_supply_annotation_files(anno_paths: list[Path]):
    table = analyze_formulas(anno_paths).to_table()
    assert len(table) > 0


@pytest.fixture
def a_report(anno_dir) -> IngredientReport:
    return analyze_formulas(anno_dir)


def test_all_ingredients_seen(anno_paths):
    table = analyze_formulas(anno_paths).to_table()
    trade_names = set()
    for file in anno_paths:
        anno = FormulaAnnotation(file)
        for trade_name in anno.trade_names:
            trade_names.add(trade_name)
    assert len(table) == len(trade_names)


def test_all_inci_collected(anno_paths):
    table = analyze_formulas(anno_paths).to_table()
    captured_incis = set([row[1] for row in table])

    for file in anno_paths:
        anno = FormulaAnnotation(file)
        assert all([(inci in captured_incis) for inci in anno.inci_names])


def test_report_has_doc_paths_dict(a_report):
    # doc_paths returns a list of paths
    # given trade_name, inci arguments
    assert isinstance(a_report.doc_paths, dict)


def test_report_has_get_doc_paths_method(a_report):
    trade_name, inci = "Sugar", "NULL"
    expected_ans = [
        "FOOD/FORMULAS/Formulations_EMEA NA/000011251 Univar Food recipe A5 - meat alternatives - Q1 2019 final spreads V2.pdf",  # noqa: E501
        "UnivarFiles/FOOD/FORMULAS/Formulations_EMEA NA/000012063 Univar Food - Recipe Card - American Cookies with Malt - Q2 2020 Final.pdf",  # noqa: E501
    ]
    assert a_report.get_doc_paths(trade_name, inci) == expected_ans


def test_report_get_doc_names_method(a_report):
    expected_ans = [
        "000011251 Univar Food recipe A5 - meat alternatives - Q1 2019 final spreads V2.pdf",  # noqa: E501
        "000012063 Univar Food - Recipe Card - American Cookies with Malt - Q2 2020 Final.pdf",  # noqa: E501
    ]
    assert a_report.get_doc_names("Sugar", "NULL") == expected_ans


def test_report_has_doc_nums_property(a_report):
    assert a_report.get_num_docs("Sugar", "NULL") == 2
    assert a_report.get_num_docs("Salt", "NULL") == 3


def test_report_knows_hero_ingredients(a_report):
    assert a_report.is_hero("MEP-377D", "NULL")
    assert a_report.is_hero("MEP-FX", "NULL")
    assert not a_report.is_hero("Sugar", "NULL")


def test_report_knows_kits(a_report):
    assert a_report.kits("Large Eggs", "NULL") == []
    assert a_report.kits("Deflavoured Faba Bean Protein", "NULL") == [
        "Meat Alternatives"
    ]


def test_report_table_has_kits(a_report):
    table = a_report.to_table()
    for row in table:
        if row[0] == "Deflavoured Faba Bean Protein":
            assert row[2] == '["Meat Alternatives"]'
