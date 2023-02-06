# File operation tests
import pytest
from lib.xlsx import ExcelFile


@pytest.fixture
def xlsx():
    return ExcelFile(
        "tests/input/xlsx/[No Kit] Original American Cookies with Malt Extract.xlsx"
    )


def test_excelfile_null(xlsx):
    assert xlsx.wb is not None


def test_xlsx_get(xlsx):
    assert xlsx.get


def test_xlsx_gets(xlsx):
    assert xlsx.gets


def test_xlsx_set(xlsx):
    assert xlsx.set
