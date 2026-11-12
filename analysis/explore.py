
import json
import pandas as pd
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "records.json"

with open(DATA_FILE, "r", encoding="utf-8") as file:
    records = json.load(file)

df = pd.DataFrame(records)

print("\n--- OWASPShield Data Analysis ---")

# Fact 1: Total records
print("\nFact 1: Total OWASP records:", len(df))

# Fact 2: Number of different cheat sheets
print("Fact 2: Different cheat sheets:", df["cheat_sheet"].nunique())

# Fact 3: Records in each OWASP category
print("\nFact 3: Records by OWASP category:")
print(df["owasp_top10_category"].value_counts().to_string())
