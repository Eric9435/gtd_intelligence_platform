import csv
from pathlib import Path


def load_csv_points(path: str) -> list[dict]:
    file_path = Path(path)
    if not file_path.exists():
        return []

    rows = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows
