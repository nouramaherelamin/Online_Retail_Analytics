from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/"data/processed/clean_transactions.csv")
assert (df.Quantity>0).all()
assert (df.UnitPrice>0).all()
assert "Revenue" in df.columns
print("Pipeline smoke test passed.")
