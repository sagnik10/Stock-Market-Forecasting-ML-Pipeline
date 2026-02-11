import pandas as pd
import numpy as np
from tqdm import tqdm
import time

start_time = time.time()

print("Loading data...")
df = pd.read_csv("stock_market_data_large.csv")

print("Normalizing column names...")
df.columns = df.columns.str.strip().str.lower()

time_cols = [c for c in df.columns if "date" in c or "time" in c]
ts_col = time_cols[0]

print("Parsing timestamps...")
df[ts_col] = pd.to_datetime(df[ts_col], errors="coerce")
df = df.dropna(subset=[ts_col])
df = df.sort_values(ts_col)
df = df.drop_duplicates(subset=[ts_col])

print("Converting numeric columns...")
for c in tqdm(df.columns):
    if c != ts_col:
        df[c] = pd.to_numeric(df[c], errors="coerce")

print("Handling missing values...")
df = df.ffill()
df = df.bfill()

if "close" in df.columns:
    print("Creating features...")
    df = df[df["close"] > 0]

    df["return"] = df["close"].pct_change()
    df["log_return"] = np.log(df["close"] / df["close"].shift(1))
    df["ma_5"] = df["close"].rolling(5).mean()
    df["ma_10"] = df["close"].rolling(10).mean()
    df["volatility"] = df["return"].rolling(10).std()

df = df.dropna()

print("Saving cleaned data...")
df.to_csv("clean_stock_market_data.csv", index=False)

end_time = time.time()

print(f"Cleaning completed successfully")
print(f"Rows after cleaning: {len(df)}")
print(f"Time taken: {end_time - start_time:.2f} seconds")