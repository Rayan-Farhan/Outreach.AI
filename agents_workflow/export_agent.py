import os
import pandas as pd
from typing import List, Dict
from datetime import datetime

def export_leads_to_csv(leads: List[Dict], export_dir: str = "exports") -> str:
    if not leads:
        raise ValueError("No leads to export.")

    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"leads_{timestamp}.csv"
    filepath = os.path.join(export_dir, filename)

    df = pd.DataFrame(leads)
    df.to_csv(filepath, index=False, encoding="utf-8")

    return filepath