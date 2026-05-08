import pandas as pd
import os


class ParquetReader:

    def read_parquet(self, base_path: str):

        parquet_data = {}

        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file.endswith(".parquet"):
                    full_path = os.path.join(root, file)
                    df = pd.read_parquet(full_path)
                    file_name = os.path.splitext(file)[0]
                    parquet_data[file_name] = df

        if not parquet_data:
            raise ValueError("No parquet files found")

        return parquet_data