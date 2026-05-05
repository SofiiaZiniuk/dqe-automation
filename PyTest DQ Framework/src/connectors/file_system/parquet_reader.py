import pandas as pd
import os

class ParquetReader:

    def read_parquet(self, base_path: str):
        dataframes = []

        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file.endswith(".parquet"):
                    full_path = os.path.join(root, file)
                    df = pd.read_parquet(full_path)
                    dataframes.append(df)

        if not dataframes:
            raise ValueError("No parquet files found")

        return pd.concat(dataframes, ignore_index=True)