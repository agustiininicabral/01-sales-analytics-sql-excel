from __future__ import annotations

import csv
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_data import validate_directory  # noqa: E402


class SalesDataValidationTests(unittest.TestCase):
    def test_repository_dataset_passes_relational_and_numeric_checks(self) -> None:
        report = validate_directory(ROOT / "data")
        self.assertEqual(report["status"], "PASS", report["failures"][:10])
        self.assertEqual(report["row_counts"]["sales"], 7000)

    def test_duplicate_sale_id_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            for source in (ROOT / "data").glob("*.csv"):
                shutil.copy(source, folder / source.name)
            path = folder / "sales.csv"
            with path.open(newline="", encoding="utf-8") as stream:
                rows = list(csv.DictReader(stream))
            rows[1]["sale_id"] = rows[0]["sale_id"]
            with path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)

            report = validate_directory(folder)

        self.assertTrue(any("sales.sale_id contains blank or duplicate" in error for error in report["failures"]))

    def test_net_amount_mismatch_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            for source in (ROOT / "data").glob("*.csv"):
                shutil.copy(source, folder / source.name)
            path = folder / "sales.csv"
            with path.open(newline="", encoding="utf-8") as stream:
                rows = list(csv.DictReader(stream))
            rows[0]["net_amount"] = "0"
            with path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)

            report = validate_directory(folder)

        self.assertTrue(any("net amount does not reconcile" in error for error in report["failures"]))


if __name__ == "__main__":
    unittest.main()
