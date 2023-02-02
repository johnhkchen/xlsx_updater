import json

from lib.formula import FormulaAnnotation
from lib.utils import get_input_files


def main(fp):
    xlsx = FormulaAnnotation(fp)
    xlsx.location = "EMEA"
    xlsx.product_type = "food"
    xlsx.export_yaml()
    xlsx.export_xlsx()


def report_null(xlsx: FormulaAnnotation) -> str:
    empties = []
    if not xlsx.claims or xlsx.description == "NULL":
        empties.append("description")
    if not xlsx.claims or xlsx.claims == "NULL":
        empties.append("claims")
    return json.dumps(empties)


def count_claims(xlsx: FormulaAnnotation) -> int:
    if not xlsx.claims or xlsx.claims == "NULL":
        return 0
    return len(xlsx.claims.split(","))


def count_description_length(xlsx: FormulaAnnotation) -> int:
    if not xlsx.description or xlsx.description == "NULL":
        return 0
    return len(xlsx.description)


if __name__ == "__main__":
    for xlsx in get_input_files():
        anno = FormulaAnnotation(xlsx)
        print(
            "{}\t{}\t{}\t{}".format(
                xlsx.name,
                report_null(anno),
                count_claims(anno),
                count_description_length(anno),
            )
        )
        # main(xlsx)
