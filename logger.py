import csv
from datetime import datetime


def log_ritual(success, escalation_level, log_file="ritual_log.csv"):
    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), success, escalation_level])
