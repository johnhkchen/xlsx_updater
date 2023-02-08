# File operation tests
import pytest
from lib.xlsx import ExcelFile


@pytest.fixture
def xlsx():
    return ExcelFile(
        "tests/input/xlsx/[No Kit] - Original American Cookies with Malt Extract.xlsx"
    )


def test_xlsx_interfaces(xlsx):
    assert xlsx.wb is not None
    assert xlsx.get
    assert xlsx.gets
    assert xlsx.set
