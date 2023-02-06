import csv

CLAIMS_PATH = "tests/input/csv/claims_mapping.csv"


def upsert_claims(claims_path=CLAIMS_PATH) -> dict[str, str]:
    output = {}
    with open(claims_path, "r") as claims_csv:
        reader = csv.reader(claims_csv, delimiter=",")
        for _ in range(4):
            next(reader)
        for row in reader:
            key, value = row[1], row[2]
            if key == "" or value == "":
                continue
            output[key] = [s.strip() for s in value.split(",")]

        return output


if __name__ == "__main__":
    # from pprint import pprint

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
