import pandas as pd


class DataQualityLibrary:

    @staticmethod
    def check_duplicates(df, column_names=None):
        if column_names:
            duplicates = df.duplicated(subset=column_names)
        else:
            duplicates = df.duplicated()

        assert not duplicates.any(), "Duplicates found in dataset"

    @staticmethod
    def check_count(df1, df2):
        assert len(df1) == len(df2), "Row counts do not match"

    @staticmethod
    def check_data_full_data_set(df1, df2):
        assert df1.equals(df2), "Datasets are not identical"

    @staticmethod
    def check_dataset_is_not_empty(df):
        assert not df.empty, "Dataset is empty"

    @staticmethod
    def check_not_null_values(df, column_names=None):
        cols = column_names if column_names else df.columns
        for col in cols:
            assert df[col].notnull().all(), f"Null values found in column {col}"