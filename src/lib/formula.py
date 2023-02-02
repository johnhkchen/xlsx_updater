from lib.xlsx import ExcelFile
from lib.utils import export_yaml


class FormulaAnnotation(ExcelFile):
    # ----------------------------
    # General Information
    # ----------------------------
    # Column A: Document Name : text
    @property
    def document_name(self) -> str:
        return self.get("General Information", "A3", "NULL")

    @document_name.setter
    def document_name(self, value):
        self.set("General Information", "A3", value)

    # Column B: Formula Name : text
    @property
    def formula_name(self) -> str:
        return self.get("General Information", "B3", "NULL")

    @formula_name.setter
    def formula_name(self, value):
        self.set("General Information", "B3", value)

    # Column C: Univar Formula Kit : text
    @property
    def kit(self) -> str:
        return self.get("General Information", "C3", "NULL")

    @kit.setter
    def kit(self, value) -> None:
        self.set("General Information", "C3", value)

    # Column D: Product Type : comma_separated_list
    @property
    def product_type(self) -> str:
        return self.get("General Information", "D3", "NULL")

    @product_type.setter
    def product_type(self, value) -> None:
        self.set("General Information", "D3", value)

    # Column E: Description : text
    @property
    def description(self) -> str:
        return self.get("General Information", "E3", "NULL")

    @description.setter
    def description(self, value) -> None:
        self.set("General Information", "E3", value)

    # Column F: Location : text
    @property
    def location(self) -> str:
        return self.get("General Information", "F3", "NULL")

    @location.setter
    def location(self, value) -> None:
        self.set("General Information", "F3", value)

    # Column G: Formula Number : text
    @property
    def formula_number(self) -> str:
        return self.get("General Information", "G3", "NULL")

    @formula_number.setter
    def formula_number(self, value) -> None:
        self.set("General Information", "G3", value)

    # Column H: Claims : comma_separated_list
    @property
    def claims(self) -> str:
        return self.get("General Information", "H3", "NULL")

    @claims.setter
    def claims(self, value) -> None:
        self.set("General Information", "H3", value)

    # Column I: Link to doc : text
    @property
    def link_to_doc(self) -> str:
        return self.get("General Information", "I3", "NULL")

    @link_to_doc.setter
    def link_to_doc(self, value) -> None:
        self.set("General Information", "I3", value)

    # Column J: Market : text
    @property
    def market(self) -> str:
        return self.get("General Information", "J3", "NULL")

    @market.setter
    def market(self, value) -> None:
        self.set("General Information", "J3", value)

    # ----------------------------
    # Formulations Page
    # ----------------------------
    @property
    def weights(self):
        return self.gets("Formulation", "D", [])[2:]

    @weights.setter
    def weights(self, values):
        for i, value in enumerate(values):
            self.set("Formulation", f"D{i+3}", value)

        self.set("General Information", "B3", value)

    # Export Methods

    def export_yaml(self, output_dir="output/yaml/"):
        file_name = (
            self.formula_name.replace(" ", "_").replace("-", "_").lower() + ".yaml"
        )
        obj = {
            "document_name": self.document_name,
            "kit": self.kit,
            "weights": self.weights,
            "formula_name": self.formula_name,
            "location": self.location,
            "product_type": self.product_type,
        }
        export_yaml(file_name, obj, output_dir)

    def export_xlsx(self):
        kit_prefix = "[No Kit] " if self.kit == "NULL" else (self.kit + " - ")
        file_name = kit_prefix + self.formula_name + ".xlsx"
        self.wb.save("output/xlsx/" + file_name)
