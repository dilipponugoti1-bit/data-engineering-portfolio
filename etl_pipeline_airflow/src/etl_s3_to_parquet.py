#!/usr/bin/env python3
import argparse
import pandas as pd
from pathlib import Path

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns=lambda c: str(c).strip().lower().replace(' ', '_'))
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce').dt.date
    if 'amount' in df.columns:
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0.0)
    return df

def write_parquet(df: pd.DataFrame, out_dir: str):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    df.to_parquet(Path(out_dir)/'orders.parquet', index=False)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    df = pd.read_csv(args.input)
    df = standardize_columns(df)
    write_parquet(df, args.output)
    print("ETL complete")

if __name__ == '__main__':
    main()
