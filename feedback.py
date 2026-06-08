import csv
import os
from datetime import datetime


def save_feedback(data: dict):
    path = "feedback.csv"
    exists = os.path.exists(path)
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["ts", "contact", "useful", "pay", "email"])
        if not exists:
            w.writeheader()
        w.writerow({"ts": datetime.utcnow().isoformat(), **data})
