#!/usr/bin/env python3
import argparse
import requests
import pandas as pd
from pathlib import Path

BASE = "https://jsonplaceholder.typicode.com"

def fetch(endpoint: str):
    url = f"{BASE}/{endpoint}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()

def normalize_posts(data):
    df = pd.json_normalize(data)
    df.columns = [c.replace('.', '_') for c in df.columns]
    return df

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--endpoint', required=True, choices=['posts','comments','users'])
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    data = fetch(args.endpoint)
    df = normalize_posts(data)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)
    print(f"Wrote {len(df)} rows to {args.output}")

if __name__ == '__main__':
    main()
