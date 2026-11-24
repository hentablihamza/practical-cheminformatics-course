"""Refresh the offline ChEMBL cache used by notebook 07.

Notebook 07 queries the live ChEMBL REST API. When the API is unreachable
(no internet, firewall, ChEMBL maintenance) it falls back to the CSV files
written by this script, so the lesson always runs.

Usage:
    python scripts/refresh_chembl_cache.py
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import pandas as pd
import requests

BASE = "https://www.ebi.ac.uk/chembl/api/data"
OUT = Path(__file__).resolve().parents[1] / "data" / "chembl_cache"

TARGET_QUERY = "acetylcholinesterase"
TARGET_ID = "CHEMBL220"  # human acetylcholinesterase
MAX_RECORDS = 1000
PAGE_SIZE = 500

ACTIVITY_FIELDS = [
    "activity_id", "molecule_chembl_id", "canonical_smiles", "standard_type",
    "standard_relation", "standard_value", "standard_units", "pchembl_value",
    "assay_chembl_id", "assay_type", "data_validity_comment",
    "document_chembl_id", "document_year", "target_chembl_id",
]


def get_json(url: str, params: dict | None = None, retries: int = 4) -> dict:
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, timeout=30)
            r.raise_for_status()
            return r.json()
        except requests.RequestException:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError("unreachable")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    status = get_json(f"{BASE}/status.json")

    targets = get_json(f"{BASE}/target/search.json",
                       {"q": TARGET_QUERY, "limit": 50})["targets"]
    tdf = pd.DataFrame([{
        "target_chembl_id": t["target_chembl_id"],
        "pref_name": t["pref_name"],
        "target_type": t["target_type"],
        "organism": t["organism"],
        "score": t.get("score"),
    } for t in targets])
    tdf.to_csv(OUT / "target_search_acetylcholinesterase.csv", index=False)

    rows, offset = [], 0
    while len(rows) < MAX_RECORDS:
        page = get_json(f"{BASE}/activity.json", {
            "target_chembl_id": TARGET_ID,
            "standard_type": "IC50",
            "assay_type": "B",
            "only": ",".join(ACTIVITY_FIELDS),
            "limit": PAGE_SIZE,
            "offset": offset,
            "order_by": "activity_id",
        })
        rows.extend(page["activities"])
        if not page["page_meta"]["next"]:
            break
        offset += PAGE_SIZE
    adf = pd.DataFrame(rows[:MAX_RECORDS])[ACTIVITY_FIELDS]
    adf.to_csv(OUT / "activities_CHEMBL220_IC50.csv", index=False)

    meta = {
        "chembl_db_version": status.get("chembl_db_version"),
        "chembl_release_date": status.get("chembl_release_date"),
        "retrieved": time.strftime("%Y-%m-%d"),
        "target_query": TARGET_QUERY,
        "target_chembl_id": TARGET_ID,
        "filters": {"standard_type": "IC50", "assay_type": "B"},
        "order_by": "activity_id",
        "records": len(adf),
    }
    (OUT / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
