import pytest
import os


@pytest.fixture(scope='module')
def source_data(db_connection):

    source_tables = {
        "facilities": """
            SELECT * FROM src_generated_facilities
        """,

        "patients": """
            SELECT * FROM src_generated_patients
        """,

        "visits": """
            SELECT * FROM src_generated_visits
        """
    }

    source_dataframes = {}

    for table_name, query in source_tables.items():

        source_dataframes[table_name] = db_connection.get_data_sql(query)

    return source_dataframes

ENTITIES = ["facilities", "patients", "visits"]
BASE_DIR = os.path.dirname(os.path.dirname(__file__)) 

@pytest.fixture(scope='module')
def parquet_data(parquet_reader):
    target_path = os.path.join(BASE_DIR, "parquet_data")
    parquet_data = parquet_reader.read_parquet(target_path)
    return parquet_data


@pytest.mark.parametrize("entity", ENTITIES)
def test_row_count(source_data, parquet_data, entity):

    source_df = source_data[entity]
    parquet_df = parquet_data[entity]

    assert len(source_df) == len(parquet_df), (
        f"Row count mismatch for {entity}: "
        f"source={len(source_df)}, parquet={len(parquet_df)}"
    )
