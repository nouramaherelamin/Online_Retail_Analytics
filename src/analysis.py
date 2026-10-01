from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def load_data(): return pd.read_csv(ROOT/"data/raw/Online Retail.csv",encoding="ISO-8859-1")
def clean(df):
    df=df.drop_duplicates().copy(); df["InvoiceDate"]=pd.to_datetime(df["InvoiceDate"],errors="coerce"); df["Revenue"]=df["Quantity"]*df["UnitPrice"]; return df
