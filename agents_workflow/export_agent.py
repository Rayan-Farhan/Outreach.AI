# agents/export_agent.py

import csv
import os
from typing import List, Dict
from datetime import datetime

def export_leads_to_csv(leads: List[Dict], export_dir: str = "exports") -> str:
    """
    Exports a list of lead dictionaries to a CSV file.
    Returns the path to the saved CSV file.
    """

    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"leads_{timestamp}.csv"
    filepath = os.path.join(export_dir, filename)

    if not leads:
        raise ValueError("No leads to export.")

    # Extract all unique keys across all leads to ensure consistent CSV header
    all_keys = set()
    for lead in leads:
        all_keys.update(lead.keys())

    all_keys = sorted(all_keys)  # optional: for consistent column order

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_keys)
        writer.writeheader()
        for lead in leads:
            writer.writerow(lead)

    return filepath
