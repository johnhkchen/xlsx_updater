import csv

from pprint import pprint
from collections import Counter

CLAIMS_PATH = "input/tsv/claims_mapping.tsv"


def upsert_claims(claims_path=CLAIMS_PATH) -> dict[str, str]:
    output = {}
    with open(claims_path, "r") as claims_csv:
        reader = csv.reader(claims_csv, delimiter="\t")

        for key, value in reader:
            if key == "" or value == "":
                continue
            output[key] = [s.strip() for s in value.split(",")]

        return output


def print_upsert_report():
    lookup_table = upsert_claims()
    report = {}
    for k, vs in lookup_table.items():
        for v in vs:
            if v not in report:
                report[v] = {k}
            report[v].add(k)

    for k, vs in report.items():
        report[k] = list(vs)

    num_trimmed_claims = len(report.keys())
    num_raw_claims = 0
    for _, vs in report.items():
        num_raw_claims += len(vs)

    print(f"Went from {num_raw_claims} to {num_trimmed_claims} claims.")
    print(f"Reduction: {100.0*num_trimmed_claims/num_raw_claims:.2f}%")

    # Note if any recursion hapens
    for k in lookup_table.keys():
        revisions = lookup_table[k]
        for revision in revisions:
            if revision in lookup_table:
                second_revision = lookup_table[revision][0]
                if revision != second_revision:
                    print(f"{k} -> {revision} -> {second_revision}")


def tally_claim_phrases():
    c = Counter()
    with open(CLAIMS_PATH, "r") as claims_csv:
        reader = csv.reader(claims_csv, delimiter="\t")

        for _, value in reader:
            for updated_claim in [s.strip() for s in value.split(",")]:
                c[updated_claim] += 1

        return c


if __name__ == "__main__":
    # print_upsert_report()
    count = tally_claim_phrases()
    del count[""]
    del count["REMOVE"]
    results = [(count, phrase) for phrase, count in count.items() if count >= 2]
    pprint(sorted(results, reverse=True))
