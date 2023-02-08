from dataclasses import dataclass, field

import csv
import json
from pathlib import Path
from collections import defaultdict

from lib.formula import FormulaAnnotation

# Generate a list of ingredients, along with documents referencing this ingredient


@dataclass
class IngredientReport:
    trade_names: list[tuple[str, str]] = field(default_factory=lambda: [])
    doc_paths: defaultdict[tuple[str, str], str] = field(
        default_factory=lambda: defaultdict(lambda: [])
    )
    ingredient_kits: defaultdict[tuple[str, str], set] = field(
        default_factory=lambda: defaultdict(lambda: set())
    )
    hero_docs: set = field(default_factory=lambda: set())

    def to_table(self):
        return [
            (
                tn,  # Trade Name: str - key
                inci,  # INCIs: str - secondary key
                json.dumps(self.kits(tn, inci)),  # Formula Kit: [str]
                self.is_hero(tn, inci),  # Hero Ingredient: bool
                self.get_num_docs(tn, inci),  # Num Files: int
                json.dumps(self.get_doc_names(tn, inci)),  # Files: [str]
                json.dumps(self.get_doc_paths(tn, inci)),  # File Paths: [str]
            )
            for tn, inci in self.trade_names
        ]

    def get_doc_paths(self, trade_name, inci) -> str:
        return self.doc_paths[(trade_name, inci)]

    def get_doc_names(self, trade_name, inci) -> str:
        return [Path(docpath).name for docpath in self.get_doc_paths(trade_name, inci)]

    def get_num_docs(self, trade_name, inci) -> int:
        return len(self.get_doc_paths(trade_name, inci))

    def is_hero(self, trade_name, inci) -> bool:
        return (trade_name, inci) in self.hero_docs

    def kits(self, trade_name, inci) -> list[str]:
        return list(self.ingredient_kits[(trade_name, inci)])


def analyze_formulas(targets: None | Path | list[Path] = None):
    if isinstance(targets, Path):
        targets = targets.glob("*.xlsx")
    if not targets:
        return IngredientReport()
    report = IngredientReport()
    trade_names = set()

    # targets = itertools.islice(targets, 10)
    for file in targets:
        anno = FormulaAnnotation(file)
        formula_rows = zip(anno.trade_names, anno.inci_names)
        for trade_name, inci in formula_rows:
            trade_names.add((trade_name, inci))
            report.doc_paths[(trade_name, inci)].append(anno.link_to_doc)
            if anno.kit != "NULL":
                report.ingredient_kits[(trade_name, inci)].add(anno.kit)

        # Add hero ingredients
        hero_rows = zip(anno.hero_trade_names, anno.hero_inci_names)
        for trade_name, inci in hero_rows:
            report.hero_docs.add((trade_name, inci))

    report.trade_names = list(trade_names)
    return report


def export_tsv(report):
    output_path = Path("output/tsv/pharma_analysis.tsv")
    with open(output_path, "w", newline="") as tsvfile:
        writer = csv.writer(
            tsvfile, delimiter="\t", escapechar="|", quoting=csv.QUOTE_NONE
        )

        fieldnames = [
            "Trade Name",
            "INCIs",
            "Formula Kit",
            "Hero Ingredient",
            "Num Files",
            "Files",
            "File Paths",
        ]
        writer.writerow(fieldnames)
        writer.writerows(report.to_table())


if __name__ == "__main__":
    target_dir = Path("input/xlsx")
    report = analyze_formulas(target_dir)
    export_tsv(report)
