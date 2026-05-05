import pytest
import os


@pytest.fixture(scope='module')
def source_data(db_connection):
    source_query = """
    SELECT * FROM users
    """
    return db_connection.get_data_sql(source_query)

BASE_DIR = os.path.dirname(os.path.dirname(__file__)) 

@pytest.fixture(scope='module')
def target_data(parquet_reader):
    target_path = os.path.join(BASE_DIR, "parquet_data")
    target_data = parquet_reader.read_parquet(target_path)
    return target_data


@pytest.mark.parquet_data
def test_check_dataset_is_not_empty(target_data, data_quality_library):
    data_quality_library.check_dataset_is_not_empty(target_data)


@pytest.mark.parquet_data
def test_check_count(source_data, target_data, data_quality_library):
    data_quality_library.check_count(source_data, target_data)