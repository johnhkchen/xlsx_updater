from dataclasses import dataclass
from lib.xlsx import ExcelFile


@dataclass
class IFormulaAnnotation:
    document_name: str
    formula_name: str
    kit: str
    product_type: str
    description: str
    location: str
    formula_num: str
    claims: str
    doc_path: str
    market: str


class MetaAnnotation(ExcelFile, IFormulaAnnotation):
    tagged_keys = {}
    FIRST_COLUMN = "A"
    FIRST_ROW = 3

    def __init__(self, file_path=None) -> None:
        super().__init__(file_path)
        sheet_name = "General Information"
        sheet_columns = [
            "document_name",
            "formula_name",
            "kit",
            "product_type",
            "description",
            "location",
            "formula_num",
            "claims",
            "doc_path",
            "market",
        ]
        for i, column in enumerate(sheet_columns):
            column = str(ord(self.FIRST_COLUMN) + i)
            self.tagged_keys[column] = (
                sheet_name,
                f"{column}{self.FIRST_ROW}",
                "NULL",
            )
            super().__setattr__(column, "NULL")

    def get(self, name, fallback="NULL"):
        sheet_name, cell, fallback = self.tagged_keys[name]
        return super().get(sheet_name, cell, fallback)

    def set(self, name, value):
        sheet_name, cell = self.tagged_keys[name][:2]
        super().set(sheet_name, cell, value)

    def __getattribute__(self, name: str):
        if name == "tagged_keys" or name not in self.tagged_keys:
            return super().__getattribute__(name)
        else:
            return self.get(name)

    def __setattr__(self, name: str, value):
        if name == "tagged_keys" or name not in self.tagged_keys:
            super().__setattr__(name, value)
        else:
            self.set(name, value)
