# Amend Annotation
# Expected Usage: python3 src/amend_anno.py
#
# Applies fixes to annotation files
#
# Input: Annotation File (xlsx)
# Input Path: 'input/xlsx'
#
# Output: Updated Annotation File (xlsx)
# Output Path: 'output/xlsx'


from lib.formula import FormulaAnnotation
from lib.utils import get_input_files


def add_market_column(xlsx: FormulaAnnotation):
    # Add Cells to Column J: text, Market, "FOOD"
    xlsx.wb["General Information"]["J1"] = "text"
    xlsx.wb["General Information"]["J2"] = "Market"
    xlsx.wb["General Information"]["J3"] = "FOOD"


def update_doc_path(xlsx: FormulaAnnotation):
    # Update the document path to the new location
    raw_text = xlsx.wb["General Information"]["I3"].value
    clean_path = raw_text.replace("D:\\Univar Files\\", "")
    clean_path = clean_path.replace("\\", "/")
    xlsx.wb["General Information"]["I3"] = clean_path


def replace_invalid_hero_inci(xlsx: FormulaAnnotation):
    # INCI should be "NULL"
    incis = xlsx.gets("Hero Ingredients", "B", [])[2:]
    incis = [s for s in incis if s is not None]
    for i, inci in enumerate(incis):
        if inci != "NULL":
            xlsx.wb["Hero Ingredients"][f"B{i+3}"] = "NULL"


def replace_invalid_formulation_inci(xlsx: FormulaAnnotation):
    # INCI should be "NULL"
    incis = xlsx.gets("Formulation", "C", [])[2:]
    incis = [s for s in incis if s is not None]
    for i, inci in enumerate(incis):
        if inci != "NULL":
            xlsx.wb["Formulation"][f"C{i+3}"] = "NULL"


def replace_invalid_inci(xlsx: FormulaAnnotation):
    replace_invalid_hero_inci(xlsx)
    replace_invalid_formulation_inci(xlsx)


def insert_property_headers(xlsx: FormulaAnnotation):
    ws = xlsx.wb["Properties"]
    ws["A1"] = "text"
    ws["A2"] = "Property"
    ws["B1"] = "text"
    ws["B2"] = "Value"


def insert_hero_headers(xlsx: FormulaAnnotation):
    ws = xlsx.wb["Hero Ingredients"]
    ws["A1"] = "text"
    ws["A2"] = "Trade Name"
    ws["B1"] = "text"
    ws["B2"] = "INCI"
    ws["C1"] = "comma_separated_list"
    ws["C2"] = "Claim"
    ws["D1"] = "text"
    ws["D2"] = "Description"
    ws["E1"] = "text"
    ws["E2"] = "Company"


def insert_missing_headers(xlsx: FormulaAnnotation):
    insert_property_headers(xlsx)
    insert_hero_headers(xlsx)


def amend_annotation(xlsx: FormulaAnnotation):
    xlsx.product_type = "food"
    add_market_column(xlsx)
    update_doc_path(xlsx)
    replace_invalid_inci(xlsx)
    insert_missing_headers(xlsx)
    xlsx.export_xlsx()


if __name__ == "__main__":
    for xlsx in get_input_files():
        amend_annotation(FormulaAnnotation(xlsx))
