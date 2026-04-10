import pandas as pd
import os

def save_to_csv(df, csv_path):
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df.to_csv(csv_path, index=False, mode='a', header=not os.path.exists(csv_path))
